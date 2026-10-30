# Tema 16 - API, Docker, consumo y simulación de despliegue PaaS

Esta práctica sigue el ejemplo de deserción estudiantil del material de Tema 16 y añade ajustes de reproducibilidad (`random_state`, versiones y `/health`).

## 1. Preparar entorno

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Entrenar modelo

```powershell
python modelo_desercion.py
```

Se genera `modelo_desercion.pkl`.

## 3. Ejecutar API

```powershell
uvicorn main:app --reload --port 8000
```

Abrir:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

En `/predict`, probar:
- edad: 22
- promedio: 5.5
- asistencia: 60

## 4. Simular consumo externo

Con la API activa, en otra terminal:

```powershell
python SimulaConsumo.py
```

## 5. Docker

Detener Uvicorn con `Ctrl+C`.

```powershell
docker build --no-cache -t modelo-desercion .
docker run --rm -p 8000:80 --name modelo-desercion-api modelo-desercion
```

Volver a abrir `/docs` y repetir la predicción.

## 6. Simulación PaaS

El archivo `Procfile` contiene el comando de inicio descrito en el material:

```text
web: uvicorn main:app --host 0.0.0.0 --port 8080
```

La demostración local y Docker es obligatoria para comprender el flujo. El despliegue real en AWS/otro PaaS puede tratarse como extensión, ya que requiere cuenta, credenciales y configuración externa.

## 7. Documentación

En `docs/` se incluyen:
- `PLANTILLA_DOCUMENTACION_TECNICA.md`
- `EJEMPLO_DOCUMENTACION_TECNICA.md`

## Ejecución rápida para la demostración docente

```powershell
.\demo.ps1 prepare
.\demo.ps1 api
```

Con la API activa, en otra terminal:

```powershell
.\demo.ps1 consume
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
