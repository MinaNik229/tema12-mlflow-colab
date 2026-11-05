import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
from mlflow import MlflowClient
from sklearn.metrics import mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
DB_PATH = ROOT / "mlflow.db"

MODEL_NAME = "Tema18_RandomForest_RMSE"
EXPERIMENT_NAME = "Tema18_Reentrenamiento_Automatizado"

MONITOR_RMSE_THRESHOLD = 4.0
MAX_STAGING_RMSE = 4.0
MIN_IMPROVEMENT = 0.20

FEATURES = ["signal_1", "signal_2", "signal_3"]
TARGET = "target"


def configure_mlflow():
    uri = f"sqlite:///{DB_PATH.resolve().as_posix()}"
    mlflow.set_tracking_uri(uri)
    mlflow.set_registry_uri(uri)
    mlflow.set_experiment(EXPERIMENT_NAME)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return uri


def client():
    configure_mlflow()
    return MlflowClient()


def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def load_alias_model(alias: str):
    configure_mlflow()
    uri = f"models:/{MODEL_NAME}@{alias}"
    return mlflow.sklearn.load_model(uri)


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
