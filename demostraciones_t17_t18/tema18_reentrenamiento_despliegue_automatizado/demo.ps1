param(
    [ValidateSet("reset", "data", "bootstrap", "monitor", "retrain", "staging", "promote", "pipeline", "status", "ui")]
    [string]$Step = "pipeline"
)

$ErrorActionPreference = "Stop"
$PY = ".\.venv\Scripts\python.exe"

switch ($Step) {
    "reset" { & $PY src\reset_demo.py }
    "data" { & $PY data\generate_data.py }
    "bootstrap" { & $PY src\bootstrap.py }
    "monitor" { & $PY src\monitor.py }
    "retrain" { & $PY src\retrain.py }
    "staging" { & $PY src\staging_validate.py }
    "promote" { & $PY src\promote.py }
    "pipeline" { & $PY src\pipeline.py }
    "ui" { & $PY -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000 }
}
