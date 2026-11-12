param(
    [ValidateSet("data", "monitor", "dashboard", "drift", "latency", "degradation", "errors", "ui")]
    [string]$Step = "monitor"
)

$ErrorActionPreference = "Stop"
$PY = ".\.venv\Scripts\python.exe"

switch ($Step) {
    "data" { & $PY data\generate_demo_data.py }
    "monitor" { & $PY src\monitor.py }
    "dashboard" { & $PY src\dashboard.py }
    "drift" { & $PY src\simulate_incidents.py --scenario drift }
    "latency" { & $PY src\simulate_incidents.py --scenario latency }
    "degradation" { & $PY src\simulate_incidents.py --scenario degradation }
    "errors" { & $PY src\simulate_incidents.py --scenario errors }
    "ui" { & $PY -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000 }
}
