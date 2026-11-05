import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def version_key(name: str):
    match = re.fullmatch(r"v(\d+)", name)
    return int(match.group(1)) if match else 10**9


records = []
for version_dir in sorted(
    [p for p in MODELS_DIR.iterdir() if p.is_dir() and p.name.startswith("v")],
    key=lambda p: version_key(p.name),
):
    metrics_path = version_dir / "metrics.json"
    if metrics_path.exists():
        records.append(json.loads(metrics_path.read_text(encoding="utf-8")))

if not records:
    raise SystemExit("No se encontraron versiones con metrics.json. Entrena v1 y v2 primero.")

df = pd.DataFrame(records)
columns = [c for c in ["version", "n_estimators", "accuracy", "run_id"] if c in df.columns]

print("\n=== Comparación de versiones ===")
print(df[columns].to_string(index=False))

best_accuracy = df["accuracy"].max()
best = df[df["accuracy"] == best_accuracy]

if len(best) == 1:
    row = best.iloc[0]
    print(
        f"\nMejor accuracy observado: {row['version']} "
        f"({row['accuracy']:.4f})."
    )
else:
    versions = ", ".join(best["version"].astype(str))
    print(
        f"\nEmpate en accuracy ({best_accuracy:.4f}) entre: {versions}."
    )

print(
    "\nLa promoción a producción no debe decidirse solo por el número de versión. "
    "Justifica la decisión con métricas, estabilidad, costo y contexto del proyecto."
)
