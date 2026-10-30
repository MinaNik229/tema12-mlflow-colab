# Tema 15 - Contenerizar un modelo con Docker

Práctica lista para ejecutar en Windows/VS Code. Está inspirada en el material complementario de Tema 15, pero añade un modelo de fraude reproducible porque el PDF menciona `modelo_fraude.py` y `simular.py` sin incluir su código.

## Orden de ejecución

### 1. Crear y activar entorno

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Entrenar y guardar `model.pkl`

```powershell
python modelo_fraude.py
```

### 3. Probar inferencia local

```powershell
python simular.py
```

### 4. Levantar FastAPI

```powershell
uvicorn app:app --reload --port 8000
```

Abrir:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

Ejemplo JSON para `/predict`:

```json
{
  "monto": 18000,
  "intentos_24h": 6,
  "es_extranjero": 1,
  "hora": 2
}
```

### 5. Probar con un cliente Python

Con la API todavía ejecutándose, abrir otra terminal:

```powershell
python test_api.py
```

### 6. Contenerizar

Detener Uvicorn con `Ctrl+C`:

```powershell
docker build --no-cache -t modelo-fraude .
docker run --rm -p 8000:8000 --name modelo-fraude-api modelo-fraude
```

## Ejecución rápida para la demostración docente

```powershell
.\demo.ps1 prepare
.\demo.ps1 api
```

Con la API activa, en otra terminal:

```powershell
.\demo.ps1 test
```

Después detén Uvicorn con `Ctrl+C`:

```powershell
.\demo.ps1 build
.\demo.ps1 run
```

En otra terminal:

```powershell
.\demo.ps1 status
.\demo.ps1 stop
```
