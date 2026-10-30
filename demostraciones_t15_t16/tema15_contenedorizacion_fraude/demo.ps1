param(
    [ValidateSet("prepare", "api", "test", "build", "run", "status", "stop")]
    [string]$Step = "prepare"
)

$ErrorActionPreference = "Stop"

switch ($Step) {
    "prepare" {
        if (-not (Test-Path ".venv")) { python -m venv .venv }
        .\.venv\Scripts\python.exe -m pip install --upgrade pip
        .\.venv\Scripts\python.exe -m pip install -r requirements.txt
        .\.venv\Scripts\python.exe modelo_fraude.py
        .\.venv\Scripts\python.exe simular.py
    }
    "api" { .\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8000 }
    "test" { .\.venv\Scripts\python.exe test_api.py }
    "build" { docker build --no-cache -t modelo-fraude . }
    "run" { docker run --rm -p 8000:8000 --name modelo-fraude-api modelo-fraude }
    "status" { docker ps; docker logs modelo-fraude-api }
    "stop" { docker stop modelo-fraude-api }
}
