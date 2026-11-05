import shutil
from pathlib import Path

from common import DATA_DIR, DB_PATH, REPORTS_DIR, ROOT


def remove(path: Path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main():
    remove(DB_PATH)
    remove(ROOT / "mlruns")
    remove(ROOT / "mlartifacts")

    for filename in ["train.csv", "production_batch.csv"]:
        remove(DATA_DIR / filename)

    if REPORTS_DIR.exists():
        for path in REPORTS_DIR.iterdir():
            if path.name != "README.md":
                remove(path)

    print("Demostración reiniciada. Los archivos fuente y README se conservaron.")


if __name__ == "__main__":
    main()
