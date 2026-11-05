param(
    [ValidateSet("validate", "v1", "v2", "compare", "ui")]
    [string]$Step = "validate"
)

$ErrorActionPreference = "Stop"

switch ($Step) {
    "validate" { .\.venv\Scripts\python.exe src\preprocess.py }
    "v1" { .\.venv\Scripts\python.exe src\train.py --version v1 --n-estimators 100 }
    "v2" { .\.venv\Scripts\python.exe src\train.py --version v2 --n-estimators 200 }
    "compare" { .\.venv\Scripts\python.exe src\compare_versions.py }
    "ui" { .\.venv\Scripts\python.exe -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000 }
}
