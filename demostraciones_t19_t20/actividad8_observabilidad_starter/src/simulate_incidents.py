import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def parse_args():
    parser = argparse.ArgumentParser(description="Simula incidentes educativos para la Actividad 8.")
    parser.add_argument(
        "--scenario",
        choices=["normal", "drift", "latency", "degradation", "errors"],
        default="drift",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    baseline_path = DATA_DIR / "baseline.csv"
    if not baseline_path.exists():
        raise FileNotFoundError("Falta data/baseline.csv. Ejecuta primero data/generate_demo_data.py")

    base = pd.read_csv(baseline_path)
    current = base.sample(n=min(250, len(base)), random_state=7).reset_index(drop=True).copy()
    rng = np.random.default_rng(123)

    if args.scenario == "normal":
        pass
    elif args.scenario == "drift":
        current["feature_1"] = current["feature_1"] + 1.5
        current["feature_2"] = current["feature_2"] - 1.0
    elif args.scenario == "latency":
        current["latency_ms"] = np.clip(current["latency_ms"] * 2.8, 20, None)
    elif args.scenario == "degradation":
        current["quality_score"] = np.clip(current["quality_score"] - 0.20, 0, 1)
    elif args.scenario == "errors":
        current["is_error"] = rng.binomial(1, 0.15, len(current))

    current.to_csv(DATA_DIR / "current.csv", index=False)
    print(f"Incidente simulado: {args.scenario}")
    print(f"Archivo actualizado: {DATA_DIR / 'current.csv'}")
    print("Ejecuta ahora: python src/monitor.py")


if __name__ == "__main__":
    main()
