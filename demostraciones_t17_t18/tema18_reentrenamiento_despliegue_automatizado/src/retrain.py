import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from common import (
    DATA_DIR,
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

    base = pd.read_csv(DATA_DIR / "train.csv")
    new_batch = pd.read_csv(DATA_DIR / "production_batch.csv")

    new_train, staging = train_test_split(
        new_batch, test_size=0.35, random_state=42
    )
    staging_path = REPORTS_DIR / "staging_batch.csv"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    staging.to_csv(staging_path, index=False)

    combined = pd.concat([base, new_train], ignore_index=True)
    X_train = combined[FEATURES]
    y_train = combined[TARGET]

    model = RandomForestRegressor(
        n_estimators=250,
        max_depth=8,
        random_state=42,
    )
    model.fit(X_train, y_train)

    staging_rmse = rmse(staging[TARGET], model.predict(staging[FEATURES]))
    signature = infer_signature(X_train, model.predict(X_train))

    with mlflow.start_run(run_name="retrain_challenger") as run:
        mlflow.log_param("role", "challenger")
        mlflow.log_param("n_estimators", 250)
        mlflow.log_param("max_depth", 8)
        mlflow.log_param("base_rows", len(base))
        mlflow.log_param("new_training_rows", len(new_train))
        mlflow.log_metric("staging_rmse_at_training", staging_rmse)

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
    c.set_registered_model_alias(MODEL_NAME, "challenger", version.version)
    c.set_model_version_tag(MODEL_NAME, version.version, "validation_status", "pending")
    c.set_model_version_tag(MODEL_NAME, version.version, "role", "challenger")

    payload = {
        "registered_version": str(version.version),
        "alias": "challenger",
        "staging_rmse_at_training": staging_rmse,
        "staging_rows": len(staging),
        "run_id": run.info.run_id,
    }
    write_json(REPORTS_DIR / "retrain.json", payload)

    print("\n=== CHALLENGER REGISTRADO ===")
    print(f"Versión: {version.version}")
    print("Alias: challenger")
    print(f"RMSE preliminar en staging: {staging_rmse:.4f}")
    print(f"Staging guardado en: {staging_path}")


if __name__ == "__main__":
    main()
