param(
    [ValidateSet("prepare", "api", "consume", "build", "run", "status", "stop")]
    [string]$Step = "prepare"
)

$ErrorActionPreference = "Stop"

switch ($Step) {
    "prepare" {
        if (-not (Test-Path ".venv")) { python -m venv .venv }
        .\.venv\Scripts\python.exe -m pip install --upgrade pip
        .\.venv\Scripts\python.exe -m pip install -r requirements.txt
        .\.venv\Scripts\python.exe modelo_desercion.py
    }
    "api" { .\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000 }
    "consume" { .\.venv\Scripts\python.exe SimulaConsumo.py }
    "build" { docker build --no-cache -t modelo-desercion . }
    "run" { docker run --rm -p 8000:80 --name modelo-desercion-api modelo-desercion }
    "status" { docker ps; docker logs modelo-desercion-api }
    "stop" { docker stop modelo-desercion-api }
}
