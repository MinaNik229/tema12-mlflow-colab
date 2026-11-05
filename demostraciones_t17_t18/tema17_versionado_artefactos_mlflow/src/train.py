import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from preprocess import load_and_validate, prepare_xy

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
DB_PATH = ROOT / "mlflow.db"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Entrena y versiona un RandomForest para el laboratorio del Tema 17."
    )
    parser.add_argument("--version", default="v1", help="Versión del artefacto, por ejemplo v1 o v2.")
    parser.add_argument("--n-estimators", type=int, default=100, help="Número de árboles del Random Forest.")
    parser.add_argument("--test-size", type=float, default=0.20, help="Proporción reservada para test.")
    parser.add_argument("--random-state", type=int, default=42, help="Semilla reproducible.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Permite reemplazar una versión existente. Úsalo solo de forma deliberada.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    version_dir = MODELS_DIR / args.version
    model_path = version_dir / "model.pkl"
    metrics_path = version_dir / "metrics.json"
    metadata_path = version_dir / "metadata.json"

    if version_dir.exists() and any(version_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"La versión {args.version} ya contiene artefactos. "
            "Crea una nueva versión (por ejemplo --version v2) "
            "o usa --overwrite solo si realmente deseas reemplazarla."
        )

    version_dir.mkdir(parents=True, exist_ok=True)

    data = load_and_validate()
    X, y = prepare_xy(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    # Artefacto principal del modelo.
    joblib.dump(model, model_path)

    # MLflow local con SQLite para que la UI siempre encuentre los mismos runs.
    mlflow.set_tracking_uri(f"sqlite:///{DB_PATH.as_posix()}")
    mlflow.set_experiment("Tema17_Versionado_Artefactos")

    with mlflow.start_run(run_name=f"{args.version}_rf_{args.n_estimators}") as run:
        mlflow.log_param("version", args.version)
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_metric("accuracy", accuracy)

        # Equivalente actualizado al log_model mostrado en el PDF.
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
        )

        metrics = {
            "version": args.version,
            "accuracy": accuracy,
            "n_estimators": args.n_estimators,
            "run_id": run.info.run_id,
        }
        metadata = {
            "version": args.version,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "features": list(X.columns),
            "target": "churn",
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "random_state": args.random_state,
            "mlflow_run_id": run.info.run_id,
        }

        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        mlflow.log_artifact(str(metrics_path), artifact_path="version_metadata")
        mlflow.log_artifact(str(metadata_path), artifact_path="version_metadata")

    print("\n========================================")
    print("ENTRENAMIENTO FINALIZADO")
    print("========================================")
    print(f"Versión:       {args.version}")
    print(f"n_estimators:  {args.n_estimators}")
    print(f"Accuracy:      {accuracy:.4f}")
    print(f"Modelo:        {model_path}")
    print(f"Métricas:      {metrics_path}")
    print(f"Metadata:      {metadata_path}")
    print(f"MLflow run_id: {run.info.run_id}")
    print("========================================")


if __name__ == "__main__":
    main()
