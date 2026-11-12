import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
SUMMARY = OUTPUT_DIR / "monitoring_summary.json"


def main() -> None:
    if not SUMMARY.exists():
        raise FileNotFoundError("Falta outputs/monitoring_summary.json. Ejecuta primero src/monitor.py")

    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", {})
    names = list(metrics.keys())
    values = [metrics[n] for n in names]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(names, values)
    ax.set_title(f"Dashboard educativo · Estado: {payload.get('status', 'unknown').upper()}")
    ax.set_ylabel("Valor observado")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "dashboard.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)

    print(f"Dashboard generado: {out}")
    print("Úsalo como evidencia y reemplázalo/adáptalo con las métricas reales de tu proyecto.")


if __name__ == "__main__":
    main()
