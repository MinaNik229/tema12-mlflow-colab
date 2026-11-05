#!/usr/bin/env bash
set -euo pipefail

STEP="${1:-validate}"

case "$STEP" in
  validate) .venv/bin/python src/preprocess.py ;;
  v1) .venv/bin/python src/train.py --version v1 --n-estimators 100 ;;
  v2) .venv/bin/python src/train.py --version v2 --n-estimators 200 ;;
  compare) .venv/bin/python src/compare_versions.py ;;
  ui) .venv/bin/python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000 ;;
  *)
    echo "Uso: bash demo.sh {validate|v1|v2|compare|ui}"
    exit 1
    ;;
esac
