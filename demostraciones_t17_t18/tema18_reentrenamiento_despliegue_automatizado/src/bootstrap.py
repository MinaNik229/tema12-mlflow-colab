import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from common import (
    DATA_DIR,
    EXPERIMENT_NAME,
    FEATURES,
    MODEL_NAME,
    REPORTS_DIR,
    TARGET,
    client,
    configure_mlflow,
    rmse,
    write_json,
)


def main():
    configure_mlflow()

    data_path = DATA_DIR / "train.csv"
    if not data_path.exists():
        raise FileNotFoundError("Falta data/train.csv. Ejecuta primero data/generate_data.py")

    data = pd.read_csv(data_path)
    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=5,
        random_state=42,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    test_rmse = rmse(y_test, predictions)

    signature = infer_signature(X_train, model.predict(X_train))

    with mlflow.start_run(run_name="bootstrap_champion") as run:
        mlflow.log_param("role", "initial_champion")
        mlflow.log_param("n_estimators", 150)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("test_rmse", test_rmse)

        info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            signature=signature,
            input_example=X_train.head(3),
        )

        version = mlflow.register_model(
            model_uri=info.model_uri,
            name=MODEL_NAME,
        )

    c = client()
    c.set_registered_model_alias(MODEL_NAME, "champion", version.version)
    c.set_model_version_tag(MODEL_NAME, version.version, "validation_status", "approved")
    c.set_model_version_tag(MODEL_NAME, version.version, "role", "champion")

    payload = {
        "experiment": EXPERIMENT_NAME,
        "model_name": MODEL_NAME,
        "registered_version": str(version.version),
        "alias": "champion",
        "test_rmse": test_rmse,
        "run_id": run.info.run_id,
    }
    write_json(REPORTS_DIR / "bootstrap.json", payload)

    print("\n=== CHAMPION INICIAL REGISTRADO ===")
    print(f"Modelo: {MODEL_NAME}")
    print(f"Versión: {version.version}")
    print("Alias: champion")
    print(f"RMSE de test: {test_rmse:.4f}")


if __name__ == "__main__":
    main()
