# Temas 15 y 16 - De MLflow a una API contenerizada con Docker

Esta práctica continúa el proyecto de **MLflow** y lo transforma en una solución que puede ejecutarse localmente, consumirse mediante una API y empaquetarse con Docker.

El objetivo no es entrenar un modelo nuevo, sino recorrer este flujo:

```text
modelo evaluado
  -> artefacto serializado
  -> API
  -> frontend mínimo
  -> imagen Docker
  -> contenedor
  -> evidencia reproducible para Fase II
```

> Entorno de referencia de la práctica: Windows, Visual Studio Code, PowerShell, Python 3.12 y Docker Desktop.

## Relación con la Fase II

Esta práctica produce evidencia para los cuatro criterios de la entrega:

- contenerización y despliegue local;
- integración API / frontend / backend;
- pruebas y validación;
- documentación y repositorio reproducible.

## Archivos

```text
mlflow_project/
├── .dockerignore
├── app.py
├── data.csv
├── Dockerfile
├── generate_data.py
├── model.pkl                 # se genera ejecutando train.py
├── requirements-deploy.txt
├── requirements.txt
└── train.py
```

| Archivo | Función |
|---|---|
| `train.py` | Entrena LogisticRegression, registra MLflow y genera `model.pkl`. |
| `model.pkl` | Artefacto del modelo para inferencia. |
| `app.py` | FastAPI, endpoints y frontend mínimo. |
| `requirements-deploy.txt` | Dependencias del contenedor. |
| `Dockerfile` | Receta para construir la imagen. |
| `.dockerignore` | Excluye archivos locales innecesarios del build. |

# 1. Verificar la computadora

```powershell
python --version
git --version
docker --version
docker info
code --version
```

Si `docker --version` funciona pero `docker info` no conecta con `docker_engine`, abre Docker Desktop y espera **Engine running**.

Prueba:

```powershell
docker run hello-world
```

Es normal que `hello-world` termine inmediatamente después de imprimir el mensaje.

# 2. Obtener el repositorio

Si todavía no lo tienes:

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
```

Si aparece:

```text
fatal: destination path 'tema12-mlflow-colab' already exists and is not an empty directory.
```

**No clones otra vez.** Entra a la carpeta existente:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
git status
git remote -v
cd .\practica_windows_desde_cero\mlflow_project
```

# 3. Crear y activar el entorno virtual

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install fastapi uvicorn joblib requests
```

El prompt debe comenzar con `(.venv)`.

# 4. Entrenar y generar model.pkl

```powershell
python train.py --C 1.0 --max_iter 200
dir model.pkl
```

`train.py` registra el experimento en MLflow y guarda un artefacto local:

```python
artifact = {
    "model": model,
    "features": list(X.columns)
}

joblib.dump(artifact, "model.pkl")
```

La API cargará este archivo para hacer inferencia sin volver a entrenar.

# 5. Revisar MLflow

```powershell
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Abre:

```text
http://localhost:5000
```

Busca el experimento `Clasificacion_Clientes`.

# 6. Ejecutar FastAPI localmente

```powershell
uvicorn app:app --reload --port 8000
```

Endpoints:

| Ruta | Método | Uso |
|---|---|---|
| `/health` | GET | Verificar servicio y modelo cargado. |
| `/predict` | POST | Enviar variables y obtener predicción. |
| `/` | GET | Frontend HTML mínimo. |

Prueba:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/
```

En Swagger, usa:

```json
{
  "edad": 48,
  "ingreso": 65887,
  "compras": 6
}
```

Un resultado correcto debe regresar **HTTP 200** con `prediccion` y `probabilidad_clase_1`.

# 7. Preparar Docker

Detén primero Uvicorn con `Ctrl+C`.

## requirements-deploy.txt

```text
fastapi
uvicorn
scikit-learn==1.9.1
pandas
joblib
numpy
```

## .dockerignore

```text
.venv
__pycache__
.git
mlflow.db
mlruns
*.pyc
.ipynb_checkpoints
```

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY app.py .
COPY model.pkl .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

# 8. Construir y ejecutar

Construir sin caché:

```powershell
docker build --no-cache -t tema15-cliente-api .
```

Comprobar la versión de scikit-learn dentro de la imagen:

```powershell
docker run --rm tema15-cliente-api python -c "import sklearn; print(sklearn.__version__)"
```

Debe imprimir:

```text
1.9.1
```

Ejecutar:

```powershell
docker run --rm -p 8000:8000 --name tema15-api tema15-cliente-api
```

En otra terminal:

```powershell
docker ps
docker logs tema15-api
docker stop tema15-api
```

Vuelve a probar `/health`, `/docs`, `/predict` y `/`.

# 9. Error real de la práctica: /health funciona pero /predict devuelve 500

Durante la ejecución real se observó:

```text
/health  -> 200 OK
/        -> 200 OK
/predict -> 500 Internal Server Error
```

El log mostró:

```text
InconsistentVersionWarning:
Trying to unpickle estimator LogisticRegression
from version 1.9.1 when using version 1.7.2
```

y después:

```text
AttributeError: 'LogisticRegression' object has no attribute 'multi_class'
```

## Diagnóstico

- el contenedor sí arrancaba;
- FastAPI sí respondía;
- `model.pkl` sí podía cargarse;
- el fallo aparecía al ejecutar la inferencia;
- el modelo había sido serializado con scikit-learn 1.9.1;
- Docker estaba utilizando 1.7.2.

## Corrección

1. fijar `scikit-learn==1.9.1`;
2. usar `python:3.12-slim`;
3. reconstruir con `--no-cache`;
4. verificar la versión dentro de la imagen antes de probar `/predict`.

**Aprendizaje:** reproducibilidad significa controlar código, artefacto, runtime, dependencias y versiones.

# 10. Troubleshooting

| Síntoma | Acción |
|---|---|
| El repositorio ya existe | No clones de nuevo; entra a la carpeta y usa `git status`. |
| PowerShell bloquea `Activate.ps1` | Usa `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| `ModuleNotFoundError` | Activa `.venv` e instala la dependencia faltante. |
| `docker` no se reconoce | Instala Docker Desktop y abre una terminal nueva. |
| No conecta a `docker_engine` | Abre Docker Desktop y espera Engine running. |
| Falta `model.pkl` | Ejecuta nuevamente `train.py`. |
| Puerto 8000 ocupado | Detén el proceso o publica `8001:8000`. |
| `/health` 200 pero `/predict` 500 | Revisa traceback y versiones de scikit-learn. |
| Docker conserva dependencias antiguas | Reconstruye con `--no-cache`. |
| La rama ya existe | Usa `git switch nombre-rama`, no `git switch -c`. |

# 11. Evidencias para Fase II

Conserva evidencia de:

- `model.pkl` generado;
- build exitoso;
- `docker ps` con contenedor activo;
- `/health` con 200;
- `/predict` con 200;
- frontend consumiendo la API;
- casos normales y extremos;
- logs del servicio;
- Dockerfile y dependencias;
- explicación del error encontrado y su solución.

La meta no es acumular archivos: es entregar un sistema **ejecutable, comprobable y replicable**.

## Guías complementarias

- [Guía del estudiante](docs/GUIA_ESTUDIANTE_T15_T16.md)
- [Guía docente](docs/GUIA_DOCENTE_T15_T16.md)
