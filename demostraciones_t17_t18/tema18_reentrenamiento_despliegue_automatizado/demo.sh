#!/usr/bin/env bash
set -euo pipefail

STEP="${1:-pipeline}"
PY=".venv/bin/python"

case "$STEP" in
  reset) "$PY" src/reset_demo.py ;;
  data) "$PY" data/generate_data.py ;;
  bootstrap) "$PY" src/bootstrap.py ;;
  monitor) "$PY" src/monitor.py ;;
  retrain) "$PY" src/retrain.py ;;
  staging) "$PY" src/staging_validate.py ;;
  promote) "$PY" src/promote.py ;;
  pipeline) "$PY" src/pipeline.py ;;\n  status) "$PY" src/status.py ;;
  ui) "$PY" -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000 ;;
  *)
    echo "Uso: bash demo.sh {reset|data|bootstrap|monitor|retrain|staging|promote|pipeline|status|ui}"
    exit 1
    ;;
esac
