# Guía docente - Demostración T15/T16

## Propósito

Demostrar cómo el proyecto de MLflow se transforma en un servicio FastAPI y después en un contenedor Docker, conectándolo directamente con Proyecto Final Fase II.

## Apertura sugerida

> Hasta T14 preguntamos si el modelo aprende, se evalúa y generaliza. Hoy cambia la pregunta: ¿otra persona o sistema puede utilizarlo sin abrir nuestro notebook ni reconstruir manualmente nuestro entorno?

## Secuencia

### 1. Proyecto

```powershell
cd $HOME\Documents\tema12-mlflow-colab\practica_windows_desde_cero\mlflow_project
code .
```

**Explicar:** no empezamos otro proyecto; ensamblamos componentes anteriores.

### 2. Entorno

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Explicar:** entorno local y entorno Docker son distintos.

### 3. Artefacto

```powershell
python train.py --C 1.0 --max_iter 200
```

**Pregunta:** ¿por qué /predict no debe entrenar el modelo en cada solicitud?

### 4. MLflow breve

```powershell
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

**Mensaje:** MLflow conserva la procedencia del modelo; ahora lo operacionalizamos.

### 5. FastAPI

```powershell
uvicorn app:app --reload --port 8000
```

Mostrar:

- /health;
- /docs;
- POST /predict;
- /.

**Mensaje:** la API es el contrato entre el modelo y otros sistemas.

### 6. Docker

Detener Uvicorn y ejecutar:

```powershell
docker build --no-cache -t tema15-cliente-api .
docker run --rm tema15-cliente-api python -c "import sklearn; print(sklearn.__version__)"
docker run --rm -p 8000:8000 --name tema15-api tema15-cliente-api
```

**Explicar:** imagen = plantilla; contenedor = instancia; `-p` publica el puerto.

### 7. Validar nuevamente

Repetir /health, /predict y frontend.

**Mensaje:** si el contrato no cambia, el consumidor no necesita saber si la API corre directamente en Python o dentro de Docker.

## Caso didáctico del error real

Patrón observado:

```text
/health 200
/predict 500
```

El traceback mostró incompatibilidad de scikit-learn 1.9.1 vs 1.7.2.

Preguntas:

1. ¿Docker está roto? No.
2. ¿FastAPI está roto? No.
3. ¿Dónde falla? En inferencia.
4. ¿Qué pista da el warning? Versiones distintas.
5. ¿Cómo se corrige? Versión compatible + Python 3.12 + rebuild sin caché.

**Mensaje clave:** reproducibilidad = código + runtime + versiones + configuración + artefactos.

## Recuperación rápida

| Problema | Acción |
|---|---|
| Repo ya existe | Entrar a la carpeta; no volver a clonar. |
| .venv bloqueado | Policy temporal Process. |
| Docker daemon detenido | Abrir Docker Desktop. |
| Puerto ocupado | Detener proceso o usar puerto alterno. |
| model.pkl ausente | Ejecutar train.py. |
| /predict 500 | Leer traceback; revisar versión. |
| Docker usa capa antigua | Build --no-cache. |
| Push falla | Conservar commit local y continuar. |

## Cierre con Fase II

Preguntar:

- ¿Otra persona puede construir y ejecutar tu contenedor siguiendo tu README?
- ¿Puedes demostrar frontend -> API -> modelo?
- ¿Qué casos de prueba conservas?
- ¿Tu documentación permite reproducir la ejecución sin preguntarte por mensaje?

> Las actividades anteriores son módulos. Fase II pide integrarlos y darles forma de solución técnica demostrable.
