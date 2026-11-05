import numpy as np
import pandas as pd

from common import (
    FEATURES,
    MAX_STAGING_RMSE,
    MIN_IMPROVEMENT,
    MODEL_NAME,
    REPORTS_DIR,
    TARGET,
    client,
    load_alias_model,
    rmse,
    write_json,
)


def main():
    staging_path = REPORTS_DIR / "staging_batch.csv"
    if not staging_path.exists():
        raise FileNotFoundError("Falta reports/staging_batch.csv. Ejecuta primero src/retrain.py")

    data = pd.read_csv(staging_path)
    champion = load_alias_model("champion")
    challenger = load_alias_model("challenger")

    champion_pred = champion.predict(data[FEATURES])
    challenger_pred = challenger.predict(data[FEATURES])

    champion_rmse = rmse(data[TARGET], champion_pred)
    challenger_rmse = rmse(data[TARGET], challenger_pred)
    improvement = champion_rmse - challenger_rmse

    smoke_test = len(challenger_pred) == len(data)
    finite_test = bool(np.isfinite(challenger_pred).all())
    quality_test = challenger_rmse <= MAX_STAGING_RMSE
    improvement_test = improvement >= MIN_IMPROVEMENT

    passed = all([smoke_test, finite_test, quality_test, improvement_test])

    payload = {
        "champion_rmse": champion_rmse,
        "challenger_rmse": challenger_rmse,
        "improvement": improvement,
        "criteria": {
            "max_staging_rmse": MAX_STAGING_RMSE,
            "min_improvement": MIN_IMPROVEMENT,
        },
        "tests": {
            "smoke_test": smoke_test,
            "finite_predictions": finite_test,
            "quality_threshold": quality_test,
            "minimum_improvement": improvement_test,
        },
        "passed": passed,
        "decision": "PROMOTE" if passed else "REJECT",
    }
    write_json(REPORTS_DIR / "staging_report.json", payload)

    c = client()
    challenger_version = c.get_model_version_by_alias(MODEL_NAME, "challenger")
    c.set_model_version_tag(
        MODEL_NAME,
        challenger_version.version,
        "validation_status",
        "passed" if passed else "failed",
    )

    print("\n=== VALIDACIÓN EN STAGING ===")
    print(f"Champion RMSE:   {champion_rmse:.4f}")
    print(f"Challenger RMSE: {challenger_rmse:.4f}")
    print(f"Mejora:          {improvement:.4f}")
    print(f"Smoke test:      {'PASS' if smoke_test else 'FAIL'}")
    print(f"Predicciones:    {'PASS' if finite_test else 'FAIL'}")
    print(f"Calidad:         {'PASS' if quality_test else 'FAIL'}")
    print(f"Mejora mínima:   {'PASS' if improvement_test else 'FAIL'}")
    print(f"Decisión:        {payload['decision']}")


if __name__ == "__main__":
    main()
