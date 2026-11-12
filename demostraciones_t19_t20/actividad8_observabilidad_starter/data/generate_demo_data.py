from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def make_batch(seed: int, n: int, shifted: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    if shifted:
        f1 = rng.normal(1.1, 1.15, n)
        f2 = rng.normal(-0.8, 1.0, n)
        f3 = rng.normal(0.6, 1.2, n)
        quality = np.clip(rng.normal(0.72, 0.06, n), 0, 1)
        latency = np.clip(rng.normal(430, 90, n), 20, None)
        is_error = rng.binomial(1, 0.09, n)
    else:
        f1 = rng.normal(0.0, 1.0, n)
        f2 = rng.normal(0.0, 1.0, n)
        f3 = rng.normal(0.0, 1.0, n)
        quality = np.clip(rng.normal(0.90, 0.03, n), 0, 1)
        latency = np.clip(rng.normal(180, 40, n), 20, None)
        is_error = rng.binomial(1, 0.02, n)

    return pd.DataFrame(
        {
            "feature_1": f1,
            "feature_2": f2,
            "feature_3": f3,
            "quality_score": quality,
            "latency_ms": latency,
            "is_error": is_error,
        }
    )


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    baseline = make_batch(seed=42, n=500, shifted=False)
    current = make_batch(seed=43, n=250, shifted=False)

    baseline.to_csv(DATA_DIR / "baseline.csv", index=False)
    current.to_csv(DATA_DIR / "current.csv", index=False)

    print("Datos demo generados:")
    print(f"- {DATA_DIR / 'baseline.csv'}")
    print(f"- {DATA_DIR / 'current.csv'}")
    print("\nEl lote current comienza en estado normal. Usa simulate_incidents.py para degradarlo.")


if __name__ == "__main__":
    main()
