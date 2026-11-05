import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


parser = argparse.ArgumentParser(
    description="Documenta qué versión fue seleccionada como candidata a producción."
)
parser.add_argument("--version", required=True, help="Versión seleccionada, por ejemplo v1 o v2.")
parser.add_argument("--reason", required=True, help="Justificación breve de la decisión.")
args = parser.parse_args()

version_dir = MODELS_DIR / args.version
metrics_path = version_dir / "metrics.json"
model_path = version_dir / "model.pkl"

if not metrics_path.exists() or not model_path.exists():
    raise FileNotFoundError(
        f"No se encontraron model.pkl y metrics.json para {args.version}."
    )

metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

selection = {
    "selected_version": args.version,
    "selected_at_utc": datetime.now(timezone.utc).isoformat(),
    "reason": args.reason,
    "metrics": metrics,
}

output = MODELS_DIR / "production.json"
output.write_text(json.dumps(selection, indent=2), encoding="utf-8")

print(f"Versión seleccionada: {args.version}")
print(f"Accuracy registrada: {metrics['accuracy']:.4f}")
print(f"Decisión documentada en: {output}")
