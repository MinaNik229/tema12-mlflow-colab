from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def build_dataframe(seed, n, shifted=False):
    rng = np.random.default_rng(seed)

    if not shifted:
        x1 = rng.normal(0.0, 1.0, n)
        x2 = rng.normal(0.0, 1.0, n)
        x3 = rng.normal(0.0, 1.0, n)
        y = 3.0 * x1 - 2.0 * x2 + 0.5 * x3 + rng.normal(0.0, 0.8, n)
    else:
        # Lote nuevo con cambios deliberados para observar degradación y activar el trigger.
        x1 = rng.normal(1.5, 1.2, n)
        x2 = rng.normal(-1.0, 1.0, n)
        x3 = rng.normal(0.7, 1.0, n)
        y = 3.8 * x1 - 1.2 * x2 + 1.1 * x3 + 5.0 + rng.normal(0.0, 0.8, n)

    return pd.DataFrame(
        {
            "signal_1": x1,
            "signal_2": x2,
            "signal_3": x3,
            "target": y,
        }
    )


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    train = build_dataframe(seed=42, n=300, shifted=False)
    production = build_dataframe(seed=123, n=160, shifted=True)

    train_path = DATA_DIR / "train.csv"
    production_path = DATA_DIR / "production_batch.csv"

    train.to_csv(train_path, index=False)
    production.to_csv(production_path, index=False)

    print("Datos generados:")
    print(f"- {train_path} ({len(train)} filas)")
    print(f"- {production_path} ({len(production)} filas)")
    print("\nEl segundo lote contiene un cambio deliberado para simular degradación del modelo.")


if __name__ == "__main__":
    main()
