# Guía del estudiante - T15/T16

## De MLflow a FastAPI y Docker

Esta guía acompaña la práctica de `practica_windows_desde_cero/mlflow_project`. Su objetivo es que puedas seguirla sin depender de instrucciones verbales: en cada etapa debes entender **qué haces, para qué lo haces, qué resultado esperar y cómo reaccionar si falla**.

## Flujo

```text
data.csv
 -> train.py + MLflow
 -> model.pkl
 -> FastAPI
 -> /predict
 -> frontend
 -> Docker image
 -> Docker container
 -> evidencia para Fase II
```

## 1. Verifica el entorno

```powershell
python --version
git --version
docker --version
docker info
```

Si Docker está instalado pero no conecta, abre Docker Desktop y espera **Engine running**.

## 2. Entra al repositorio

Si no está clonado:

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
```

Si Git dice que la carpeta ya existe, no vuelvas a clonar.

```powershell
cd $HOME\Documents\tema12-mlflow-colab\practica_windows_desde_cero\mlflow_project
```

## 3. Crea y activa .venv

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install fastapi uvicorn joblib requests
```

**Qué estás haciendo:** aislando dependencias.

**Qué debes observar:** `(.venv)` al inicio del prompt.

## 4. Genera model.pkl

```powershell
python train.py --C 1.0 --max_iter 200
dir model.pkl
```

**Para qué:** la API necesita un modelo ya entrenado. No debe volver a entrenar cada vez que llega una solicitud.

## 5. Ejecuta la API

```powershell
uvicorn app:app --reload --port 8000
```

Abre:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/
```

En `/docs`, prueba `POST /predict` con:

```json
{
  "edad": 48,
  "ingreso": 65887,
  "compras": 6
}
```

**Qué ocurre:** navegador -> JSON -> FastAPI -> DataFrame -> model.pkl -> respuesta JSON.

## 6. Construye Docker

Detén Uvicorn con `Ctrl+C`.

```powershell
docker build --no-cache -t tema15-cliente-api .
```

Comprueba la versión crítica:

```powershell
docker run --rm tema15-cliente-api python -c "import sklearn; print(sklearn.__version__)"
```

Debe ser `1.9.1`.

Ejecuta el contenedor:

```powershell
docker run --rm -p 8000:8000 --name tema15-api tema15-cliente-api
```

Vuelve a probar los endpoints.

## 7. Error real y aprendizaje

En la práctica ocurrió:

```text
/health 200
/predict 500
```

El modelo se creó con scikit-learn 1.9.1, pero el contenedor había instalado 1.7.2. El servicio arrancaba, pero la inferencia fallaba.

Se corrigió con:

```text
requirements-deploy.txt -> scikit-learn==1.9.1
Dockerfile              -> python:3.12-slim
build                   -> --no-cache
```

**Aprendizaje:** reproducibilidad = código + artefactos + runtime + dependencias + versiones.

## 8. Errores frecuentes

| Error | Acción |
|---|---|
| Repo ya existe | Entra a la carpeta; no clones de nuevo. |
| PowerShell bloquea .venv | Policy temporal a nivel Process. |
| Falta módulo | Activa .venv e instala la dependencia. |
| Docker daemon no corre | Abre Docker Desktop. |
| Falta model.pkl | Ejecuta train.py. |
| Puerto 8000 ocupado | Detén el proceso o usa otro puerto. |
| /predict devuelve 500 | Lee el traceback y revisa versiones. |
| Warning de scikit-learn | Igualar versión y reconstruir sin caché. |

## 9. Evidencias que debes conservar

- build de Docker;
- contenedor activo;
- /health 200;
- /predict 200;
- frontend;
- casos de prueba;
- logs;
- Dockerfile;
- estructura del repositorio;
- análisis del error y corrección.

La meta de Fase II es una solución **ejecutable, comprobable y replicable**.
