import json
import subprocess
import sys
from pathlib import Path

from common import REPORTS_DIR, get_alias_version
from monitor import evaluate_monitoring_batch

ROOT = Path(__file__).resolve().parents[1]


def run(script_name):
    script = ROOT / "src" / script_name
    print(f"\n>>> Ejecutando {script_name}")
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main():
    print("\n========================================")
    print("PIPELINE LOCAL TEMA 18")
    print("========================================")

    if get_alias_version("champion") is None:
        print("\nNo existe un champion inicial en el Model Registry.")
        print("Este pipeline parte de un modelo ya aprobado.")
        print("\nEjecuta primero:")
        print("  python data/generate_data.py")
        print("  python src/bootstrap.py")
        print("  python src/status.py")
        raise SystemExit(1)

    subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, check=True)

    monitor = evaluate_monitoring_batch()
    print(f"\nRMSE monitor: {monitor['observed_rmse']:.4f}")
    print(f"Umbral:       {monitor['threshold']:.4f}")

    if not monitor["triggered"]:
        print("\nNo se activó el trigger. El champion se conserva.")
        return

    print("\nTrigger activado: inicia reentrenamiento.")
    run("retrain.py")
    run("staging_validate.py")

    report = json.loads(
        (REPORTS_DIR / "staging_report.json").read_text(encoding="utf-8")
    )
    if report["passed"]:
        run("promote.py")
    else:
        print("\nEl challenger fue rechazado en staging. No se modifica champion.")

    print("\nPipeline finalizado.")


if __name__ == "__main__":
    main()
