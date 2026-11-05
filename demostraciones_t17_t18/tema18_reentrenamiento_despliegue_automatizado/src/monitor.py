import pandas as pd

from common import (
    DATA_DIR,
    FEATURES,
    MONITOR_RMSE_THRESHOLD,
    REPORTS_DIR,
    TARGET,
    load_alias_model,
    rmse,
    write_json,
)


def evaluate_monitoring_batch():
    batch_path = DATA_DIR / "production_batch.csv"
    if not batch_path.exists():
        raise FileNotFoundError("Falta data/production_batch.csv. Ejecuta data/generate_data.py")

    data = pd.read_csv(batch_path)
    champion = load_alias_model("champion")

    observed_rmse = rmse(data[TARGET], champion.predict(data[FEATURES]))
    triggered = observed_rmse > MONITOR_RMSE_THRESHOLD

    payload = {
        "metric": "rmse",
        "observed_rmse": observed_rmse,
        "threshold": MONITOR_RMSE_THRESHOLD,
        "triggered": triggered,
        "decision": "RETRAIN" if triggered else "KEEP_CHAMPION",
    }
    write_json(REPORTS_DIR / "monitor.json", payload)
    return payload


def main():
    payload = evaluate_monitoring_batch()

    print("\n=== MONITOREO DEL CHAMPION ===")
    print(f"RMSE observado: {payload['observed_rmse']:.4f}")
    print(f"Umbral:         {payload['threshold']:.4f}")
    print(f"Trigger:        {'SÍ' if payload['triggered'] else 'NO'}")
    print(f"Decisión:       {payload['decision']}")


if __name__ == "__main__":
    main()
