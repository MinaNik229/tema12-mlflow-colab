# Tema 15 - Contenerizar un modelo con Docker

Práctica lista para ejecutar en **Windows, macOS o Linux** usando Visual Studio Code y una terminal.

El flujo completo es:

```text
GitHub
  ↓
clonar repositorio
  ↓
entrar a la práctica Tema 15
  ↓
crear entorno virtual
  ↓
entrenar modelo
  ↓
generar model.pkl
  ↓
probar inferencia local
  ↓
levantar FastAPI
  ↓
probar /predict
  ↓
construir imagen Docker
  ↓
ejecutar contenedor
  ↓
volver a probar la API
```

---

# Antes de comenzar

## Windows (PowerShell)

```powershell
python --version
git --version
docker --version
docker info
code --version
```

Si `docker info` no logra conectarse al motor, abre **Docker Desktop** y espera hasta que aparezca **Engine running**.

## macOS / Linux (Bash o Zsh)

```bash
python3 --version
git --version
docker --version
docker info
code --version
```

En **macOS**, normalmente debes abrir **Docker Desktop**.  
En **Linux**, Docker puede ejecutarse como Docker Engine o Docker Desktop.

Si en Linux `docker info` muestra un error de permisos, prueba primero:

```bash
sudo docker info
```

> No uses `sudo` automáticamente en todos los comandos. Solo úsalo si la instalación de Docker de tu equipo lo requiere.

---

# Orden de ejecución desde cero

## 1. Clonar el repositorio

### Windows

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
git status
git branch --show-current
git pull origin main
```

Si la carpeta ya existe:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
git status
git switch main
git pull origin main
```

### macOS / Linux

```bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab
git status
git branch --show-current
git pull origin main
```

Si la carpeta ya existe:

```bash
cd ~/Documents/tema12-mlflow-colab
git status
git switch main
git pull origin main
```

> Si tu sistema no tiene una carpeta `~/Documents`, puedes clonar el repositorio en cualquier carpeta de trabajo.

---

## 2. Entrar a la práctica del Tema 15

### Windows

```powershell
cd .\demostraciones_t15_t16\tema15_contenedorizacion_fraude
dir
code .
```

### macOS / Linux

```bash
cd demostraciones_t15_t16/tema15_contenedorizacion_fraude
ls -la
code .
```

Debes encontrar, entre otros:

```text
modelo_fraude.py
simular.py
app.py
test_api.py
requirements.txt
Dockerfile
.dockerignore
demo.ps1
demo.sh
README.md
```

> A partir de este punto todos los comandos deben ejecutarse desde esta carpeta.

---

## 3. Crear y activar el entorno virtual

### Windows

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Cuando el entorno esté activo, el prompt debe comenzar con:

```text
(.venv)
```

---

## 4. Entrenar el modelo y generar `model.pkl`

### Windows

```powershell
python modelo_fraude.py
dir model.pkl
```

### macOS / Linux

```bash
python3 modelo_fraude.py
ls -lh model.pkl
```

El script:

1. genera un conjunto de datos sintético;
2. entrena un modelo de clasificación;
3. evalúa el modelo;
4. guarda el modelo y el orden de sus variables en `model.pkl`.

---

## 5. Probar inferencia local

### Windows

```powershell
python simular.py
```

### macOS / Linux

```bash
python3 simular.py
```

Se mostrarán varias transacciones con su predicción y probabilidad de fraude.

---

## 6. Levantar FastAPI

Con el entorno virtual activo, el comando es igual en los tres sistemas:

```bash
uvicorn app:app --reload --port 8000
```

Si `uvicorn` no se reconoce, usa:

### Windows

```powershell
python -m uvicorn app:app --reload --port 8000
```

### macOS / Linux

```bash
python3 -m uvicorn app:app --reload --port 8000
```

Abre en el navegador:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

En `/docs`, busca **POST /predict**, selecciona **Try it out** y utiliza:

```json
{
  "monto": 18000,
  "intentos_24h": 6,
  "es_extranjero": 1,
  "hora": 2
}
```

Después selecciona **Execute**.

Una ejecución correcta debe responder con HTTP `200`.

---

## 7. Probar la API desde otro programa

Mantén Uvicorn ejecutándose y abre una segunda terminal.

### Windows

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python test_api.py
```

### macOS / Linux

```bash
source .venv/bin/activate
python3 test_api.py
```

Este script demuestra que la API puede ser consumida por otro programa y no solamente desde Swagger.

---

## 8. Detener la API local

En cualquier sistema:

```text
Ctrl + C
```

Esto libera el puerto 8000.

---

## 9. Construir la imagen Docker

El comando Docker es igual en Windows, macOS y Linux:

```bash
docker build --no-cache -t modelo-fraude .
docker images modelo-fraude
```

Si Linux requiere permisos elevados:

```bash
sudo docker build --no-cache -t modelo-fraude .
sudo docker images modelo-fraude
```

---

## 10. Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 --name modelo-fraude-api modelo-fraude
```

Vuelve a probar:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

La respuesta debe ser funcionalmente equivalente a la prueba local.

---

## 11. Revisar el contenedor y sus logs

```bash
docker ps
docker logs modelo-fraude-api
docker stop modelo-fraude-api
```

En Linux, si tu instalación lo requiere:

```bash
sudo docker ps
sudo docker logs modelo-fraude-api
sudo docker stop modelo-fraude-api
```

---

# Ejecución rápida para demostración docente

## Windows

Utiliza `demo.ps1`:

```powershell
.\demo.ps1 prepare
.\demo.ps1 api
```

En otra terminal:

```powershell
.\demo.ps1 test
```

Después de detener Uvicorn con `Ctrl+C`:

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

Utiliza `demo.sh`:

```bash
bash demo.sh prepare
bash demo.sh api
```

En otra terminal:

```bash
bash demo.sh test
```

Después de detener Uvicorn con `Ctrl+C`:

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

# ¿Qué debe quedar claro al finalizar?

```text
modelo_fraude.py
      ↓
entrenamiento
      ↓
model.pkl
      ↓
app.py / FastAPI
      ↓
POST /predict
      ↓
Dockerfile
      ↓
imagen modelo-fraude
      ↓
contenedor
      ↓
misma API ejecutándose en un entorno reproducible
```

Esta secuencia constituye una versión didáctica del proceso que cada estudiante deberá adaptar a su propio proyecto de la **Fase II**.
