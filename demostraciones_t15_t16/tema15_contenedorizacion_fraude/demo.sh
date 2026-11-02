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
    .venv/bin/python modelo_fraude.py
    .venv/bin/python simular.py
    ;;
  api)
    .venv/bin/python -m uvicorn app:app --reload --port 8000
    ;;
  test)
    .venv/bin/python test_api.py
    ;;
  build)
    docker build --no-cache -t modelo-fraude .
    ;;
  run)
    docker run --rm -p 8000:8000 --name modelo-fraude-api modelo-fraude
    ;;
  status)
    docker ps
    docker logs modelo-fraude-api
    ;;
  stop)
    docker stop modelo-fraude-api
    ;;
  *)
    echo "Uso: bash demo.sh {prepare|api|test|build|run|status|stop}"
    exit 1
    ;;
esac
