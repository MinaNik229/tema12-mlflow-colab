# Tema 16 - API, consumo, Docker, documentación y simulación de despliegue PaaS

Esta práctica continúa lo trabajado en el **Tema 15** y puede ejecutarse en **Windows, macOS o Linux**.

En el Tema 16 avanzamos hacia:

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

> Importante: el dataset es pequeño y sintético. Esta práctica sirve para comprender integración y despliegue; no debe utilizarse para tomar decisiones reales sobre estudiantes.

---

# Antes de comenzar

## Windows

```powershell
python --version
git --version
docker --version
docker info
code --version
```

## macOS / Linux

```bash
python3 --version
git --version
docker --version
docker info
code --version
```

En macOS abre **Docker Desktop**.  
En Linux utiliza Docker Engine o Docker Desktop según tu instalación.

---

# Ruta A - Ya realizaste el Tema 15

Si ya clonaste el repositorio, **no vuelvas a ejecutar `git clone`**.

## Windows

```powershell
cd $HOME\Documents\tema12-mlflow-colab
git status
git status --short
```

Si no tienes cambios locales:

```powershell
git switch main
git pull origin main
```

Si modificaste Tema 15 y deseas conservarlo:

```powershell
git diff
git add demostraciones_t15_t16/tema15_contenedorizacion_fraude
git status
git commit -m "Actualiza practica Tema 15 despues de la ejecucion local"
git pull --rebase origin main
git push origin main
```

## macOS / Linux

```bash
cd ~/Documents/tema12-mlflow-colab
git status
git status --short
```

Si no tienes cambios locales:

```bash
git switch main
git pull origin main
```

Si modificaste Tema 15 y deseas conservarlo:

```bash
git diff
git add demostraciones_t15_t16/tema15_contenedorizacion_fraude
git status
git commit -m "Actualiza practica Tema 15 despues de la ejecucion local"
git pull --rebase origin main
git push origin main
```

---

# Ruta B - Primera vez en esta computadora

## Windows

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
git status
git branch --show-current
git pull origin main
```

## macOS / Linux

```bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab
git status
git branch --show-current
git pull origin main
```

---

# 1. Entrar a la práctica del Tema 16

## Windows

```powershell
cd .\demostraciones_t15_t16\tema16_desercion_api_docker_nube
dir
code .
```

## macOS / Linux

```bash
cd demostraciones_t15_t16/tema16_desercion_api_docker_nube
ls -la
code .
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
demo.sh
README.md
docs/
```

---

# 2. Crear y activar el entorno virtual

## Windows

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

El prompt debe comenzar con `(.venv)`.

---

# 3. Crear el modelo de clasificación

## Windows

```powershell
python modelo_desercion.py
dir modelo_desercion.pkl
```

## macOS / Linux

```bash
python3 modelo_desercion.py
ls -lh modelo_desercion.pkl
```

El script crea el dataset didáctico, entrena un `RandomForestClassifier` y guarda `modelo_desercion.pkl`.

---

# 4. Ejecutar la API

Con el entorno virtual activo:

```bash
uvicorn main:app --reload --port 8000
```

Si `uvicorn` no se reconoce:

### Windows

```powershell
python -m uvicorn main:app --reload --port 8000
```

### macOS / Linux

```bash
python3 -m uvicorn main:app --reload --port 8000
```

Abre:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

En `POST /predict` prueba:

- `edad = 22`
- `promedio = 5.5`
- `asistencia = 60`

---

# 5. Simular que otro sistema consume la API

Mantén Uvicorn ejecutándose.

## Windows

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python SimulaConsumo.py
```

## macOS / Linux

```bash
source .venv/bin/activate
python3 SimulaConsumo.py
```

Conceptualmente:

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

---

# 6. Detener la API local

```text
Ctrl + C
```

---

# 7. Revisar el Dockerfile

La imagen utiliza `python:3.12-slim`, instala dependencias y ejecuta Uvicorn dentro del contenedor.

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

---

# 8. Construir la imagen Docker

Windows, macOS y Linux:

```bash
docker build --no-cache -t modelo-desercion .
docker images modelo-desercion
```

En Linux, si tu instalación requiere privilegios:

```bash
sudo docker build --no-cache -t modelo-desercion .
sudo docker images modelo-desercion
```

---

# 9. Ejecutar el contenedor

```bash
docker run --rm -p 8000:80 --name modelo-desercion-api modelo-desercion
```

Vuelve a probar:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

---

# 10. Inspeccionar el contenedor

```bash
docker ps
docker logs modelo-desercion-api
docker stop modelo-desercion-api
```

En Linux puede ser necesario anteponer `sudo`.

---

# 11. Simulación de despliegue PaaS

El archivo `Procfile` incluye:

```text
web: uvicorn main:app --host 0.0.0.0 --port 8080
```

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

Esta parte es independiente del sistema operativo local.

---

# 12. Documentación técnica

Dentro de `docs/` se incluyen:

```text
PLANTILLA_DOCUMENTACION_TECNICA.md
EJEMPLO_DOCUMENTACION_TECNICA.md
```

La documentación debe describir arquitectura, datos, modelo, API, infraestructura, despliegue, pruebas, monitoreo, riesgos y trazabilidad.

---

# 13. Git y GitHub durante Tema 16

No debes volver a ejecutar `git init` ni `git remote add origin`.

## Windows

Desde la raíz del repositorio:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
git status
git diff
git add demostraciones_t15_t16/tema16_desercion_api_docker_nube
git status
git commit -m "Actualiza practica Tema 16"
git pull --rebase origin main
git push origin main
```

## macOS / Linux

```bash
cd ~/Documents/tema12-mlflow-colab
git status
git diff
git add demostraciones_t15_t16/tema16_desercion_api_docker_nube
git status
git commit -m "Actualiza practica Tema 16"
git pull --rebase origin main
git push origin main
```

---

# 14. Ejecución rápida para demostración docente

## Windows

```powershell
.\demo.ps1 prepare
.\demo.ps1 api
```

En otra terminal:

```powershell
.\demo.ps1 consume
```

Después de `Ctrl+C`:

```powershell
.\demo.ps1 build
.\demo.ps1 run
```

En otra terminal:

```powershell
.\demo.ps1 status
.\demo.ps1 stop
```

## macOS / Linux

```bash
bash demo.sh prepare
bash demo.sh api
```

En otra terminal:

```bash
bash demo.sh consume
```

Después de `Ctrl+C`:

```bash
bash demo.sh build
bash demo.sh run
```

En otra terminal:

```bash
bash demo.sh status
bash demo.sh stop
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

Esta secuencia conecta directamente con la **Fase II**, donde la solución debe poder integrarse, ejecutarse, probarse, documentarse y reproducirse.
