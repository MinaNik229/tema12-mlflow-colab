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
    parser.add_argument(
        "--version",
        default="v1",
        help="Versión del artefacto, por ejemplo v1 o v2.",
    )
    parser.add_argument(
        "--n-estimators",
        type=int,
        default=100,
        help="Número de árboles que formarán el Random Forest.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.20,
        help="Proporción reservada para test.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Semilla para obtener resultados reproducibles.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Permite reemplazar una versión existente. Úsalo solo de forma deliberada.",
    )
    return parser.parse_args()


def save_json(path: Path, payload: dict):
    """Guarda JSON de forma legible para que el alumno pueda inspeccionarlo en VS Code."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


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

    # ============================================================
    # 1. CARGAR Y PREPARAR DATOS
    # ============================================================
    data = load_and_validate()
    X, y = prepare_xy(data)

    # ============================================================
    # 2. DIVIDIR TRAIN / TEST
    # ============================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    # ============================================================
    # 3. CREAR Y ENTRENAR RANDOM FOREST
    # ============================================================
    # n_estimators = número de árboles de decisión que componen el bosque.
    # v1 utilizará 100 y v2 utilizará 200 para comparar dos configuraciones.
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state,
    )
    model.fit(X_train, y_train)

    # ============================================================
    # 4. EVALUAR
    # ============================================================
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    # ============================================================
    # 5. CREAR ARTEFACTOS LOCALES
    # ============================================================
    # IMPORTANTE:
    # Se crean ANTES de MLflow. Así, aunque MLflow tenga un problema,
    # model.pkl, metrics.json y metadata.json quedan disponibles.
    joblib.dump(model, model_path)

    metrics = {
        "version": args.version,
        "accuracy": accuracy,
        "n_estimators": args.n_estimators,
        "test_size": args.test_size,
        "random_state": args.random_state,
        "mlflow_run_id": None,
    }

    metadata = {
        "version": args.version,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "features": list(X.columns),
        "target": "churn",
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "random_state": args.random_state,
        "n_estimators": args.n_estimators,
        "mlflow_status": "pending",
        "mlflow_run_id": None,
    }

    save_json(metrics_path, metrics)
    save_json(metadata_path, metadata)

    print("\nArtefactos locales creados:")
    print(f"- {model_path}")
    print(f"- {metrics_path}")
    print(f"- {metadata_path}")

    # ============================================================
    # 6. REGISTRAR EL EXPERIMENTO EN MLFLOW
    # ============================================================
    mlflow_run_id = None
    mlflow_status = "not_logged"

    try:
        mlflow.set_tracking_uri(f"sqlite:///{DB_PATH.as_posix()}")
        mlflow.set_experiment("Tema17_Versionado_Artefactos")

        with mlflow.start_run(
            run_name=f"{args.version}_rf_{args.n_estimators}"
        ) as run:
            mlflow_run_id = run.info.run_id

            mlflow.log_param("version", args.version)
            mlflow.log_param("n_estimators", args.n_estimators)
            mlflow.log_param("test_size", args.test_size)
            mlflow.log_param("random_state", args.random_state)
            mlflow.log_metric("accuracy", accuracy)

            mlflow.sklearn.log_model(
                sk_model=model,
                name="model",
            )

            # Actualizamos los JSON con el run_id ya conocido.
            metrics["mlflow_run_id"] = mlflow_run_id
            metadata["mlflow_status"] = "logged"
            metadata["mlflow_run_id"] = mlflow_run_id

            save_json(metrics_path, metrics)
            save_json(metadata_path, metadata)

            mlflow.log_artifact(
                str(metrics_path),
                artifact_path="version_metadata",
            )
            mlflow.log_artifact(
                str(metadata_path),
                artifact_path="version_metadata",
            )

            mlflow_status = "logged"

    except Exception as exc:
        # Los artefactos locales ya existen. Dejamos evidencia de que
        # el problema ocurrió específicamente durante el tracking MLflow.
        metadata["mlflow_status"] = "failed"
        metadata["mlflow_error"] = str(exc)
        save_json(metadata_path, metadata)

        print("\nADVERTENCIA: los artefactos locales sí fueron creados,")
        print("pero el registro en MLflow no pudo completarse.")
        print(f"Detalle MLflow: {exc}")

    # ============================================================
    # 7. RESUMEN FINAL
    # ============================================================
    print("\n========================================")
    print("ENTRENAMIENTO FINALIZADO")
    print("========================================")
    print(f"Versión:        {args.version}")
    print(f"n_estimators:   {args.n_estimators}")
    print(f"Accuracy:       {accuracy:.4f}")
    print(f"Modelo:         {model_path}")
    print(f"Métricas JSON:  {metrics_path}")
    print(f"Metadata JSON:  {metadata_path}")
    print(f"MLflow status:  {mlflow_status}")
    print(f"MLflow run_id:  {mlflow_run_id or 'No disponible'}")
    print("========================================")


if __name__ == "__main__":
    main()
