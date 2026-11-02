#!/usr/bin/env bash
set -euo pipefail

STEP="${1:-prepare}"

case "$STEP" in
  prepare)
    if [ ! -d ".venv" ]; then
      python3 -m venv .venv
    fi
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python modelo_desercion.py
    ;;
  api)
    .venv/bin/python -m uvicorn main:app --reload --port 8000
    ;;
  consume)
    .venv/bin/python SimulaConsumo.py
    ;;
  build)
    docker build --no-cache -t modelo-desercion .
    ;;
  run)
    docker run --rm -p 8000:80 --name modelo-desercion-api modelo-desercion
    ;;
  status)
    docker ps
    docker logs modelo-desercion-api
    ;;
  stop)
    docker stop modelo-desercion-api
    ;;
  *)
    echo "Uso: bash demo.sh {prepare|api|consume|build|run|status|stop}"
    exit 1
    ;;
esac
