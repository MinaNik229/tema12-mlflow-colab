# Tema 15 - Contenerizar un modelo con Docker

Práctica lista para ejecutar en Windows/VS Code. Está inspirada en el material complementario de Tema 15, pero añade un modelo de fraude reproducible porque el PDF menciona `modelo_fraude.py` y `simular.py` sin incluir su código.

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

## Antes de comenzar

Verifica que estén disponibles:

```powershell
python --version
git --version
docker --version
docker info
code --version
```

Si `docker info` no logra conectarse al motor, abre **Docker Desktop** y espera hasta que aparezca **Engine running**.

---

# Orden de ejecución desde cero

## 1. Clonar el repositorio

Abre **PowerShell** y ve a la carpeta donde guardarás el proyecto. Por ejemplo:

```powershell
cd $HOME\Documents
```

Clona el repositorio:

```powershell
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
```

Entra al repositorio:

```powershell
cd .\tema12-mlflow-colab
```

Comprueba que estás en la rama principal y que la copia está actualizada:

```powershell
git status
git branch --show-current
git pull origin main
```

### Si Git indica que la carpeta ya existe

Si aparece:

```text
fatal: destination path 'tema12-mlflow-colab' already exists and is not an empty directory.
```

**No vuelvas a clonar el repositorio.** Entra a la copia que ya existe:

```powershell
cd $HOME\Documents\tema12-mlflow-colab
git status
git switch main
git pull origin main
```

---

## 2. Entrar a la práctica del Tema 15

Desde la raíz del repositorio:

```powershell
cd .\demostraciones_t15_t16\tema15_contenedorizacion_fraude
```

Comprueba los archivos:

```powershell
dir
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
README.md
```

Abre esta carpeta directamente en Visual Studio Code:

```powershell
code .
```

> A partir de este punto todos los comandos deben ejecutarse desde esta carpeta.

---

## 3. Crear y activar el entorno virtual

En la terminal integrada de VS Code:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Cuando el entorno esté activo, el prompt debe comenzar con:

```text
(.venv)
```

---

## 4. Entrenar el modelo y generar `model.pkl`

```powershell
python modelo_fraude.py
```

El script:

1. genera un conjunto de datos sintético para la demostración;
2. entrena un modelo de clasificación;
3. evalúa el modelo;
4. guarda el modelo y el orden de sus variables en `model.pkl`.

Comprueba que el archivo fue creado:

```powershell
dir model.pkl
```

---

## 5. Probar inferencia local

Antes de utilizar una API o Docker, comprobaremos que el modelo funciona directamente en Python:

```powershell
python simular.py
```

Se mostrarán varias transacciones con su predicción y probabilidad de fraude.

---

## 6. Levantar FastAPI

```powershell
uvicorn app:app --reload --port 8000
```

La terminal quedará ocupada mientras el servidor esté activo. Es normal.

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

Una ejecución correcta debe responder con HTTP `200` y una predicción.

---

## 7. Probar la API desde otro programa

Mantén Uvicorn ejecutándose.

Abre una **segunda terminal** en VS Code, activa el entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Ejecuta:

```powershell
python test_api.py
```

Este script demuestra que la API puede ser consumida por otro programa y no solamente desde Swagger.

---

## 8. Detener la API local

Regresa a la terminal donde está Uvicorn y presiona:

```text
Ctrl + C
```

Esto libera el puerto 8000 para ejecutar el contenedor Docker.

---

## 9. Construir la imagen Docker

Verifica primero que Docker Desktop esté ejecutándose.

Después:

```powershell
docker build --no-cache -t modelo-fraude .
```

Comprueba que la imagen existe:

```powershell
docker images modelo-fraude
```

---

## 10. Ejecutar el contenedor

```powershell
docker run --rm -p 8000:8000 --name modelo-fraude-api modelo-fraude
```

Ahora la aplicación ya no se está ejecutando desde el entorno virtual de Windows: está ejecutándose dentro de Docker.

Vuelve a probar:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

La respuesta debe ser funcionalmente equivalente a la prueba local.

---

## 11. Revisar el contenedor y sus logs

En otra terminal:

```powershell
docker ps
docker logs modelo-fraude-api
```

Después puedes detenerlo con:

```powershell
docker stop modelo-fraude-api
```

Como el contenedor se creó con `--rm`, será eliminado automáticamente al detenerse. La imagen `modelo-fraude` permanece disponible.

---

# Ejecución rápida para la demostración docente

Cuando ya hayas probado la práctica completa y quieras impartirla sin reescribir todos los comandos, puedes utilizar `demo.ps1`.

## Preparar entorno, dependencias y modelo

```powershell
.\demo.ps1 prepare
```

## Levantar la API

```powershell
.\demo.ps1 api
```

Con la API activa, en otra terminal:

```powershell
.\demo.ps1 test
```

Después detén Uvicorn con `Ctrl+C`.

## Construir y ejecutar Docker

```powershell
.\demo.ps1 build
.\demo.ps1 run
```

En otra terminal:

```powershell
.\demo.ps1 status
.\demo.ps1 stop
```

---

# ¿Qué debe quedar claro al finalizar?

Al terminar la práctica debes poder explicar este flujo:

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
