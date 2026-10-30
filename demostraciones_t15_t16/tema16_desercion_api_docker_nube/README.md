# Tema 16 - API, consumo, Docker, documentación y simulación de despliegue PaaS

Esta práctica continúa lo trabajado en el **Tema 15**. En el Tema 15 el objetivo fue comprender el flujo:

```text
modelo entrenado
  ↓
artefacto .pkl
  ↓
FastAPI
  ↓
Docker
  ↓
contenedor ejecutable
```

En el Tema 16 vamos un paso más adelante:

```text
modelo
  ↓
API
  ↓
consumo desde otro programa
  ↓
Docker
  ↓
estrategia de despliegue PaaS
  ↓
documentación técnica
  ↓
trazabilidad en Git/GitHub
```

La práctica utiliza un ejemplo didáctico de **predicción de riesgo de deserción estudiantil**.

> Importante: el dataset es pequeño y sintético. Esta práctica sirve para comprender el proceso técnico de integración y despliegue; no debe interpretarse como un modelo válido para tomar decisiones reales sobre estudiantes.

---

# Antes de comenzar

Verifica:

```powershell
python --version
git --version
docker --version
docker info
code --version
```

Docker Desktop debe mostrar:

```text
Engine running
```

---

# Ruta A - Ya realizaste el Tema 15

Si ya clonaste el repositorio durante Tema 15, **no vuelvas a ejecutar `git clone`**.

Ve a tu repositorio local:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
```

Revisa primero si hiciste modificaciones durante Tema 15:

```powershell
git status
git status --short
```

## Si no tienes cambios locales

Debe aparecer algo semejante a:

```text
nothing to commit, working tree clean
```

Entonces actualiza:

```powershell
git switch main
git pull origin main
```

## Si modificaste archivos del Tema 15 y quieres conservarlos

No hagas `git pull` todavía.

Revisa qué cambió:

```powershell
git diff
```

Agrega únicamente la carpeta del Tema 15:

```powershell
git add demostraciones_t15_t16/tema15_contenedorizacion_fraude
```

Comprueba qué quedará en el commit:

```powershell
git status
```

Crea el commit:

```powershell
git commit -m "Actualiza practica Tema 15 despues de la ejecucion local"
```

Después integra cualquier cambio reciente del remoto:

```powershell
git pull --rebase origin main
```

Si no hay conflictos, publica tus cambios:

```powershell
git push origin main
```

> Evitamos `git add .` para mantener control sobre qué archivos se están versionando.

---

# Ruta B - Primera vez en esta computadora

Si aún no tienes el repositorio:

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
git status
git branch --show-current
git pull origin main
```

Si Git indica que `tema12-mlflow-colab` ya existe, no vuelvas a clonarlo. Entra a la carpeta existente.

---

# 1. Entrar a la práctica del Tema 16

Desde la raíz del repositorio:

```powershell
cd .\demostraciones_t15_t16\tema16_desercion_api_docker_nube
```

Comprueba los archivos:

```powershell
dir
```

Debes encontrar:

```text
modelo_desercion.py
main.py
SimulaConsumo.py
requirements.txt
Dockerfile
.dockerignore
Procfile
demo.ps1
README.md
docs/
```

Abre esta carpeta en VS Code:

```powershell
code .
```

A partir de este punto, ejecuta los comandos desde esta carpeta.

---

# 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El prompt debe comenzar con:

```text
(.venv)
```

¿Qué estamos haciendo?

- `.venv` crea un entorno aislado.
- `requirements.txt` define las dependencias de esta demostración.
- Las versiones se fijan para reducir diferencias entre computadoras.

---

# 3. Crear el modelo de clasificación

Ejecuta:

```powershell
python modelo_desercion.py
```

El script:

1. crea un dataset didáctico;
2. separa variables de entrada y salida;
3. entrena un `RandomForestClassifier`;
4. evalúa de forma básica;
5. guarda el artefacto del modelo.

Se debe generar:

```text
modelo_desercion.pkl
```

Compruébalo:

```powershell
dir modelo_desercion.pkl
```

El flujo hasta ahora es:

```text
datos
  ↓
modelo_desercion.py
  ↓
Random Forest
  ↓
modelo_desercion.pkl
```

---

# 4. Ejecutar la API

Ejecuta:

```powershell
uvicorn main:app --reload --port 8000
```

La terminal quedará ocupada mientras Uvicorn esté ejecutándose.

Abre:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

En `/docs`, abre:

```text
POST /predict
```

Selecciona **Try it out**.

Prueba:

- `edad = 22`
- `promedio = 5.5`
- `asistencia = 60`

Después selecciona **Execute**.

La API regresará una estructura semejante a:

```json
{
  "prediccion": 1,
  "riesgo": "Alto riesgo de deserción",
  "probabilidad_desercion": 0.75
}
```

La probabilidad puede variar.

---

# 5. Simular que otro sistema consume la API

Hasta este punto utilizamos Swagger para probar manualmente.

Ahora vamos a demostrar que **otro programa puede consumir nuestra API**.

Mantén Uvicorn ejecutándose.

Abre una segunda terminal de VS Code y activa el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Ejecuta:

```powershell
python SimulaConsumo.py
```

El archivo envía una petición HTTP a:

```text
http://127.0.0.1:8000/predict
```

Este paso representa conceptualmente:

```text
Sistema externo
     ↓
request HTTP
     ↓
FastAPI
     ↓
modelo_desercion.pkl
     ↓
response JSON
```

Esta separación entre consumidor y modelo es fundamental para integrar frontend, backend o servicios externos.

---

# 6. Detener la API local

Regresa a la terminal donde se está ejecutando Uvicorn y presiona:

```text
Ctrl + C
```

Con esto liberamos el puerto para Docker.

---

# 7. Revisar el Dockerfile

El Dockerfile incluido utiliza:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY modelo_desercion.pkl .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

Aquí Docker empaqueta:

```text
Python
+ dependencias
+ main.py
+ modelo_desercion.pkl
+ comando de inicio
```

en una imagen reproducible.

---

# 8. Construir la imagen Docker

Confirma que Docker Desktop esté activo.

Ejecuta:

```powershell
docker build --no-cache -t modelo-desercion .
```

Comprueba:

```powershell
docker images modelo-desercion
```

---

# 9. Ejecutar el contenedor

```powershell
docker run --rm -p 8000:80 --name modelo-desercion-api modelo-desercion
```

Observa el mapeo:

```text
computadora : contenedor
8000        : 80
```

Ahora vuelve a probar:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

La API debe funcionar igual que antes, pero ahora se ejecuta dentro del contenedor.

---

# 10. Inspeccionar el contenedor

Abre otra terminal:

```powershell
docker ps
docker logs modelo-desercion-api
```

Los logs deben mostrar peticiones semejantes a:

```text
GET /health 200
GET /docs 200
POST /predict 200
```

Después:

```powershell
docker stop modelo-desercion-api
```

---

# 11. Simulación de despliegue PaaS

El material del Tema 16 lleva el ejemplo hacia una plataforma PaaS.

En esta práctica no necesitamos realizar un despliegue real para comprender el concepto.

El archivo:

```text
Procfile
```

incluye:

```text
web: uvicorn main:app --host 0.0.0.0 --port 8080
```

Esto representa el comando que un servicio PaaS puede utilizar para iniciar la aplicación.

Conceptualmente:

```text
GitHub
  ↓
plataforma PaaS
  ↓
instala requirements.txt
  ↓
ejecuta comando de inicio
  ↓
FastAPI
  ↓
URL pública
```

El material de Tema 16 utiliza AWS Elastic Beanstalk como ejemplo de esta estrategia. Para la actividad académica puede documentarse la estrategia sin requerir una cuenta o un despliegue real.

---

# 12. Documentación técnica

Dentro de:

```text
docs/
```

se incluyen:

```text
PLANTILLA_DOCUMENTACION_TECNICA.md
EJEMPLO_DOCUMENTACION_TECNICA.md
```

La documentación debe describir al menos:

1. información general;
2. propósito y alcance;
3. arquitectura;
4. datos;
5. modelo;
6. API / motor de inferencia;
7. infraestructura;
8. proceso de despliegue;
9. pruebas;
10. monitoreo y mantenimiento;
11. riesgos y limitaciones;
12. aspectos éticos;
13. trazabilidad y versionado.

La documentación no sustituye al código: explica cómo está construido, cómo funciona y cómo puede reproducirse.

---

# 13. Git y GitHub durante Tema 16

Como ya estamos dentro de un repositorio existente, **no debes ejecutar nuevamente**:

```text
git init
git remote add origin ...
```

El repositorio ya está conectado a GitHub.

Cuando hagas cambios durante esta práctica, vuelve a la raíz:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
```

Revisa:

```powershell
git status
git diff
```

Agrega únicamente la práctica del Tema 16:

```powershell
git add demostraciones_t15_t16/tema16_desercion_api_docker_nube
```

Comprueba:

```powershell
git status
```

Crea el commit:

```powershell
git commit -m "Actualiza practica Tema 16"
```

Antes de publicar, integra posibles cambios remotos:

```powershell
git pull --rebase origin main
```

Finalmente:

```powershell
git push origin main
```

---

# 14. Ejecución rápida para demostración docente

Una vez que ya hayas probado manualmente toda la práctica, puedes usar:

```powershell
.\demo.ps1 prepare
```

Después:

```powershell
.\demo.ps1 api
```

En otra terminal:

```powershell
.\demo.ps1 consume
```

Detén Uvicorn con `Ctrl+C`.

Construye Docker:

```powershell
.\demo.ps1 build
```

Ejecuta:

```powershell
.\demo.ps1 run
```

En otra terminal:

```powershell
.\demo.ps1 status
.\demo.ps1 stop
```

---

# ¿Qué debe quedar claro al terminar?

```text
modelo_desercion.py
       ↓
modelo_desercion.pkl
       ↓
main.py / FastAPI
       ↓
Swagger o SimulaConsumo.py
       ↓
Docker
       ↓
servicio reproducible
       ↓
estrategia PaaS
       ↓
documentación técnica
       ↓
Git / GitHub
```

Esta secuencia conecta directamente con la **Fase II**, donde el objetivo ya no es solo demostrar que existe un modelo, sino mostrar que la solución puede integrarse, ejecutarse, probarse, documentarse y reproducirse.
