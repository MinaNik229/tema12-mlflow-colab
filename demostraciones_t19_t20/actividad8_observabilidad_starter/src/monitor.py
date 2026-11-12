from __future__ import annotations

import argparse
import json
import logging
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
DATA_DIR = ROOT / "data"
DEFAULT_CONFIG = ROOT / "config" / "monitoring_config.json"


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor educativo genérico para la Actividad 8.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--baseline", default=str(DATA_DIR / "baseline.csv"))
    parser.add_argument("--current", default=str(DATA_DIR / "current.csv"))
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    """Population Stability Index sencillo para variables numéricas."""
    expected = pd.to_numeric(expected, errors="coerce").dropna().to_numpy()
    actual = pd.to_numeric(actual, errors="coerce").dropna().to_numpy()
    if len(expected) == 0 or len(actual) == 0:
        return float("nan")

    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.unique(np.quantile(expected, quantiles))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf

    exp_counts, _ = np.histogram(expected, bins=edges)
    act_counts, _ = np.histogram(actual, bins=edges)

    exp_pct = np.clip(exp_counts / max(exp_counts.sum(), 1), 1e-6, None)
    act_pct = np.clip(act_counts / max(act_counts.sum(), 1), 1e-6, None)
    return float(np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct)))


def evaluate_threshold(name: str, value: float, rule: dict) -> dict:
    direction = rule.get("direction", "max")
    warning = float(rule["warning"])
    critical = float(rule["critical"])

    if direction == "max":
        severity = "critical" if value >= critical else "warning" if value >= warning else "ok"
    elif direction == "min":
        severity = "critical" if value <= critical else "warning" if value <= warning else "ok"
    else:
        raise ValueError(f"direction inválida en {name}: {direction}")

    return {
        "metric": name,
        "value": value,
        "severity": severity,
        "warning_threshold": warning,
        "critical_threshold": critical,
        "direction": direction,
    }


def configure_logging() -> logging.Logger:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("actividad8_monitor")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(OUTPUT_DIR / "monitoring_log.jsonl", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger


def write_trace(trace_id: str, stage: str, duration_ms: float, status: str = "ok") -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "trace_id": trace_id,
        "stage": stage,
        "duration_ms": round(duration_ms, 3),
        "status": status,
        "timestamp": time.time(),
    }
    with (OUTPUT_DIR / "traces.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    baseline_path = Path(args.baseline)
    current_path = Path(args.current)

    for path in [config_path, baseline_path, current_path]:
        if not path.exists():
            raise FileNotFoundError(f"No existe: {path}")

    config = load_json(config_path)
    logger = configure_logging()
    trace_id = uuid.uuid4().hex[:12]

    t0 = time.perf_counter()
    baseline = pd.read_csv(baseline_path)
    current = pd.read_csv(current_path)
    write_trace(trace_id, "load_data", (time.perf_counter() - t0) * 1000)

    columns = config["columns"]
    metrics: dict[str, float] = {}

    t1 = time.perf_counter()
    quality_col = columns.get("quality")
    if quality_col and quality_col in current.columns:
        metrics["quality"] = float(current[quality_col].mean())

    latency_col = columns.get("latency_ms")
    if latency_col and latency_col in current.columns:
        metrics["latency_p95_ms"] = float(current[latency_col].quantile(0.95))

    error_col = columns.get("is_error")
    if error_col and error_col in current.columns:
        metrics["error_rate"] = float(current[error_col].mean())

    drift_values = {}
    for feature in config.get("drift_features", []):
        if feature in baseline.columns and feature in current.columns:
            drift_values[feature] = psi(baseline[feature], current[feature])

    if drift_values:
        metrics["drift_psi"] = float(max(drift_values.values()))

    write_trace(trace_id, "compute_metrics", (time.perf_counter() - t1) * 1000)

    t2 = time.perf_counter()
    alerts = []
    for name, rule in config.get("thresholds", {}).items():
        if name in metrics and np.isfinite(metrics[name]):
            result = evaluate_threshold(name, metrics[name], rule)
            if result["severity"] != "ok":
                alerts.append(result)

    success_target = float(config.get("service_slo", {}).get("success_rate_target", 0.95))
    if "error_rate" in metrics:
        allowed_error = max(1.0 - success_target, 1e-9)
        metrics["service_success_rate"] = 1.0 - metrics["error_rate"]
        metrics["error_budget_consumed_pct"] = float(
            min(999.0, 100.0 * metrics["error_rate"] / allowed_error)
        )

    write_trace(trace_id, "evaluate_alerts", (time.perf_counter() - t2) * 1000)

    status = "critical" if any(a["severity"] == "critical" for a in alerts) else "warning" if alerts else "ok"
    summary = {
        "project_name": config.get("project_name", "project"),
        "modality": config.get("modality", "custom"),
        "trace_id": trace_id,
        "status": status,
        "metrics": metrics,
        "drift_by_feature": drift_values,
        "alerts": alerts,
        "recommended_action": (
            "execute_runbook_and_review_rollback_or_retraining"
            if status == "critical"
            else "investigate_and_monitor_more_frequently"
            if status == "warning"
            else "keep_monitoring"
        ),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "monitoring_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "alerts.json").write_text(
        json.dumps(alerts, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info(json.dumps({"event": "monitoring_run", **summary}, ensure_ascii=False))

    mlflow_cfg = config.get("mlflow", {})
    if mlflow_cfg.get("enabled", False):
        try:
            import mlflow

            db_path = ROOT / "mlflow.db"
            mlflow.set_tracking_uri(f"sqlite:///{db_path.resolve().as_posix()}")
            mlflow.set_experiment(mlflow_cfg.get("experiment_name", "Actividad8_Observabilidad"))
            with mlflow.start_run(run_name=f"monitor_{trace_id}"):
                for name, value in metrics.items():
                    if np.isfinite(value):
                        mlflow.log_metric(name, float(value))
                mlflow.log_param("status", status)
                mlflow.log_param("modality", config.get("modality", "custom"))
                mlflow.log_artifact(str(OUTPUT_DIR / "monitoring_summary.json"), artifact_path="monitoring")
                mlflow.log_artifact(str(OUTPUT_DIR / "alerts.json"), artifact_path="monitoring")
        except ImportError:
            print("ADVERTENCIA: MLflow no está instalado; el monitoreo local sí se completó.")
            print("Instálalo con: python -m pip install -r requirements.txt")

    print("\n=== ACTIVIDAD 8 · MONITOREO ===")
    print(f"Proyecto: {summary['project_name']}")
    print(f"Trace ID: {trace_id}")
    print(f"Estado:   {status.upper()}")
    for name, value in metrics.items():
        print(f"- {name}: {value:.4f}")
    print(f"Alertas:  {len(alerts)}")
    for alert in alerts:
        print(f"  [{alert['severity'].upper()}] {alert['metric']} = {alert['value']:.4f}")
    print(f"Acción sugerida: {summary['recommended_action']}")
    print(f"Resumen: {OUTPUT_DIR / 'monitoring_summary.json'}")


if __name__ == "__main__":
    main()
