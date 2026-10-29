# tema12-mlflow-colab
Ejemplo educativo de gestión de experimentos de Machine Learning con MLflow y Google Colab

Práctica completa en Google Colab
Git/GitHub + versionado de datasets + MLflow
Este notebook parte de un repositorio de GitHub que ya existe, pero crea desde cero dos prácticas nuevas dentro de él:
tema12-mlflow-colab/
└── practica_desde_cero/
    ├── versionado-datasets-github/
    │   ├── data/
    │   │   └── ventas.csv
    │   ├── CHANGELOG.md
    │   └── README.md
    │
    └── mlflow_project/
        ├── data.csv
        ├── train.py
        └── requirements.txt
La carpeta practica_desde_cero/ permite trabajar sin destruir las carpetas que ya existan en el repositorio.
Parte A — Versionado de dataset
Se reproducen las versiones:
- v1.0.0: dataset inicial.
- v1.1.0: se agrega una venta.
- v2.0.0: se agrega la columna categoria.
Parte B — MLflow
Se crea un proyecto desde cero, se generan datos sintéticos, se entrena una regresión logística y se registran varios experimentos con distintos valores de C.
Importante: /content/ es temporal. Los cambios importantes deben enviarse a GitHub con git push antes de terminar la sesión de Colab.



0. Variables de la práctica
Celda 2 de 67

0. Variables de la práctica
Solo cambia GITHUB_USER, REPO_NAME, GIT_NAME y GIT_EMAIL si otra persona utiliza el notebook.


Celda de código 3
Celda 3 de 67

GITHUB_USER = "MinaNik229"
REPO_NAME = "tema12-mlflow-colab"

# Datos que aparecerán como autor de los commits.
GIT_NAME = "TU NOMBRE"
GIT_EMAIL = "TU_CORREO_DE_GITHUB"

REPO_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}.git"

# Rutas de trabajo dentro de Colab.
REPO_DIR = f"/content/{REPO_NAME}"
PRACTICE_ROOT = f"{REPO_DIR}/practica_desde_cero"

VERSIONADO_DIR = f"{PRACTICE_ROOT}/versionado-datasets-github"
MLFLOW_DIR = f"{PRACTICE_ROOT}/mlflow_project"

print("Repositorio:", REPO_URL)
print("Ruta local:", REPO_DIR)

1. Verificar Python y Git
Celda 4 de 67

1. Verificar Python y Git
Google Colab ya incluye Python y Git. Solo comprobamos que estén disponibles.


Celda de código 5
Celda 5 de 67

!python --version
!git --version

2. Clonar o actualizar el repositorio
Celda 6 de 67

2. Clonar o actualizar el repositorio
Esta celda hace dos cosas posibles:
- Si el repositorio no existe en /content/, lo clona desde GitHub.
- Si ya fue clonado en esta sesión, ejecuta git pull --ff-only para traer los cambios más recientes.
Esto evita el error destination path already exists.


Celda de código 7
Celda 7 de 67

import os
import subprocess

os.chdir("/content")

if os.path.isdir(os.path.join(REPO_DIR, ".git")):
    print("El repositorio ya existe en esta sesión.")
    os.chdir(REPO_DIR)

    # Trae únicamente una actualización lineal.
    # Si hubiera conflictos, se detendrá en lugar de mezclarlos automáticamente.
    subprocess.run(
        ["git", "pull", "--ff-only", "origin", "main"],
        check=False
    )
else:
    print("Clonando repositorio...")
    subprocess.run(
        ["git", "clone", REPO_URL, REPO_DIR],
        check=True
    )
    os.chdir(REPO_DIR)

print("\nCarpeta actual:")
print(os.getcwd())

print("\nEstado del repositorio:")
subprocess.run(["git", "status"], check=False)

3. Verificar el repositorio remoto
Celda 8 de 67

3. Verificar el repositorio remoto
git remote -v permite comprobar a qué repositorio de GitHub se enviarán los cambios.


Celda de código 9
Celda 9 de 67

os.chdir(REPO_DIR)

!git remote -v
!git branch --show-current

4. Configurar la identidad de Git
Celda 10 de 67

4. Configurar la identidad de Git
Git necesita saber quién crea cada commit.
Utiliza el mismo correo asociado con GitHub si quieres que los commits se relacionen con tu cuenta.


Celda de código 11
Celda 11 de 67

os.chdir(REPO_DIR)

subprocess.run(["git", "config", "user.name", GIT_NAME], check=True)
subprocess.run(["git", "config", "user.email", GIT_EMAIL], check=True)

print("Nombre:", subprocess.check_output(
    ["git", "config", "user.name"],
    text=True
).strip())

print("Correo:", subprocess.check_output(
    ["git", "config", "user.email"],
    text=True
).strip())

5. Preparar autenticación segura para git push
Celda 12 de 67

5. Preparar autenticación segura para git push
Para leer un repositorio público no se necesita autenticación, pero para escribir en GitHub sí.
Antes de ejecutar esta celda
1. En GitHub crea un Personal Access Token (PAT) con acceso de escritura al contenido del repositorio.
2. En Google Colab abre el panel Secrets (icono de llave).
3. Crea un secreto llamado:
GITHUB_TOKEN
4. Pega el token y permite que el notebook acceda al secreto.
El token no se imprime ni se escribe dentro del notebook.


Celda de código 13
Celda 13 de 67

from google.colab import userdata
import os

GITHUB_TOKEN = userdata.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError(
        "No se encontró GITHUB_TOKEN en Colab Secrets."
    )

# Git puede pedir usuario y contraseña durante un push por HTTPS.
# Este pequeño script responde esas preguntas usando variables
# de entorno, sin mostrar el token.
askpass_script = '''#!/bin/sh
case "$1" in
    *Username*) echo "$GITHUB_USER" ;;
    *Password*) echo "$GITHUB_TOKEN" ;;
esac
'''

with open("/tmp/git-askpass.sh", "w") as f:
    f.write(askpass_script)

os.chmod("/tmp/git-askpass.sh", 0o700)

os.environ["GITHUB_USER"] = GITHUB_USER
os.environ["GITHUB_TOKEN"] = GITHUB_TOKEN

print("Autenticación preparada para esta sesión.")

6. Crear desde cero el espacio de las dos prácticas
Celda 14 de 67

6. Crear desde cero el espacio de las dos prácticas
Aunque el repositorio ya exista, queremos que las prácticas de versionado y MLflow comiencen desde cero.
Para no borrar otros materiales del repositorio, todo se creará dentro de:
practica_desde_cero/
Si esta carpeta ya existe en la sesión actual, se elimina y se vuelve a crear.
Esta celda no borra el repositorio completo. Solo elimina practica_desde_cero/.



Celda de código 15
Celda 15 de 67

import shutil
import os

os.chdir(REPO_DIR)

if os.path.exists(PRACTICE_ROOT):
    print("Eliminando práctica anterior en:")
    print(PRACTICE_ROOT)
    shutil.rmtree(PRACTICE_ROOT)

os.makedirs(VERSIONADO_DIR, exist_ok=True)
os.makedirs(os.path.join(VERSIONADO_DIR, "data"), exist_ok=True)
os.makedirs(MLFLOW_DIR, exist_ok=True)

print("Estructura limpia creada:\n")
for root, dirs, files in os.walk(PRACTICE_ROOT):
    nivel = root.replace(PRACTICE_ROOT, "").count(os.sep)
    sangria = "  " * nivel
    print(f"{sangria}{os.path.basename(root)}/")

7. Preparar .gitignore
Celda 16 de 67

7. Preparar .gitignore
Los resultados internos de MLflow, como mlflow.db, mlruns/ y mlartifacts/, no deben almacenarse normalmente en Git.
La celda agrega reglas al .gitignore del repositorio sin borrar reglas existentes.


Celda de código 17
Celda 17 de 67

gitignore_path = os.path.join(REPO_DIR, ".gitignore")

reglas = [
    "",
    "# --- MLflow / práctica Colab ---",
    "**/mlflow.db",
    "**/mlruns/",
    "**/mlartifacts/",
    "**/__pycache__/",
    "*.pyc",
    ".ipynb_checkpoints/",
]

contenido_actual = ""
if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        contenido_actual = f.read()

with open(gitignore_path, "a", encoding="utf-8") as f:
    for regla in reglas:
        if regla and regla in contenido_actual:
            continue
        f.write(regla + "\n")

print("Archivo .gitignore actualizado.")

PARTE A — VERSIONADO DE UN DATASET CON GIT Y GITHUB
Celda 18 de 67

PARTE A — VERSIONADO DE UN DATASET CON GIT Y GITHUB
8. Crear la versión inicial v1.0.0
La primera versión tendrá tres ventas y cuatro columnas:
id_venta, fecha, producto, monto
También se crean CHANGELOG.md y README.md.


Celda de código 19
Celda 19 de 67

from pathlib import Path

os.makedirs(os.path.join(VERSIONADO_DIR, "data"), exist_ok=True)

ventas_v1 = '''id_venta,fecha,producto,monto
1,2025-01-01,Laptop,15000
2,2025-01-02,Mouse,350
3,2025-01-03,Teclado,800
'''

changelog_v1 = '''# Changelog

## v1.0.0 - 2025-01-10
- Dataset inicial con 3 registros de ventas.
'''

readme_versionado = '''# Versionado del dataset

Este ejemplo utiliza versionado semántico para ilustrar
cómo cambia un dataset a lo largo del tiempo.

- v1.x: estructura básica.
- v2.x: cambios estructurales.

Las versiones se identifican mediante tags de Git.
'''

Path(os.path.join(VERSIONADO_DIR, "data", "ventas.csv")).write_text(
    ventas_v1,
    encoding="utf-8"
)

Path(os.path.join(VERSIONADO_DIR, "CHANGELOG.md")).write_text(
    changelog_v1,
    encoding="utf-8"
)

Path(os.path.join(VERSIONADO_DIR, "README.md")).write_text(
    readme_versionado,
    encoding="utf-8"
)

print("Versión inicial creada.")

9. Revisar el contenido antes del primer commit
Celda 20 de 67

9. Revisar el contenido antes del primer commit


Celda de código 21
Celda 21 de 67

import pandas as pd

display(
    pd.read_csv(
        os.path.join(VERSIONADO_DIR, "data", "ventas.csv")
    )
)

print("\nCHANGELOG.md:\n")
print(
    Path(os.path.join(VERSIONADO_DIR, "CHANGELOG.md"))
    .read_text(encoding="utf-8")
)

10. Crear el commit y el tag v1.0.0
Celda 22 de 67

10. Crear el commit y el tag v1.0.0
Un commit registra el estado de los archivos.
Un tag asigna un nombre legible a un commit específico.
En esta práctica el tag v1.0.0 representa la primera versión oficial del dataset.


Celda de código 23
Celda 23 de 67

os.chdir(REPO_DIR)

# Agregamos únicamente los archivos de esta práctica y .gitignore.
subprocess.run(
    ["git", "add", ".gitignore", "practica_desde_cero/versionado-datasets-github"],
    check=True
)

subprocess.run(["git", "status", "--short"], check=False)

# Crear commit.
resultado = subprocess.run(
    ["git", "commit", "-m", "Add initial sales dataset v1.0.0"],
    text=True
)

# Crear el tag solo si todavía no existe localmente.
tags_locales = subprocess.check_output(
    ["git", "tag"],
    text=True
).split()

if "v1.0.0" not in tags_locales:
    subprocess.run(["git", "tag", "v1.0.0"], check=True)
    print("Tag v1.0.0 creado.")
else:
    print("El tag v1.0.0 ya existía; no se volvió a crear.")

11. Enviar v1.0.0 a GitHub
Celda 24 de 67

11. Enviar v1.0.0 a GitHub
Primero se envía la rama actual y después el tag.


Celda de código 25
Celda 25 de 67

os.chdir(REPO_DIR)

env_git = os.environ.copy()
env_git["GIT_ASKPASS"] = "/tmp/git-askpass.sh"
env_git["GIT_TERMINAL_PROMPT"] = "0"

subprocess.run(
    ["git", "push", "origin", "HEAD"],
    env=env_git,
    check=True
)

subprocess.run(
    ["git", "push", "origin", "v1.0.0"],
    env=env_git,
    check=True
)

print("v1.0.0 enviada a GitHub.")

12. Crear la versión v1.1.0
Celda 26 de 67

12. Crear la versión v1.1.0
Ahora agregamos una nueva venta:
4, 2025-01-04, Monitor, 4200
La estructura del CSV no cambia, por eso sigue siendo una versión 1.x.


Celda de código 27
Celda 27 de 67

ventas_v11 = '''id_venta,fecha,producto,monto
1,2025-01-01,Laptop,15000
2,2025-01-02,Mouse,350
3,2025-01-03,Teclado,800
4,2025-01-04,Monitor,4200
'''

changelog_v11 = '''# Changelog

## v1.1.0 - 2025-01-15
- Se agrega registro de venta de Monitor.
- Validación de consistencia en columna monto.

## v1.0.0 - 2025-01-10
- Dataset inicial con 3 registros de ventas.
'''

Path(os.path.join(VERSIONADO_DIR, "data", "ventas.csv")).write_text(
    ventas_v11,
    encoding="utf-8"
)

Path(os.path.join(VERSIONADO_DIR, "CHANGELOG.md")).write_text(
    changelog_v11,
    encoding="utf-8"
)

display(pd.read_csv(os.path.join(VERSIONADO_DIR, "data", "ventas.csv")))

13. Guardar y publicar v1.1.0
Celda 28 de 67

13. Guardar y publicar v1.1.0


Celda de código 29
Celda 29 de 67

os.chdir(REPO_DIR)

subprocess.run(
    ["git", "add", "practica_desde_cero/versionado-datasets-github"],
    check=True
)

subprocess.run(
    ["git", "commit", "-m", "Add new record to sales dataset v1.1.0"],
    check=True
)

tags_locales = subprocess.check_output(
    ["git", "tag"],
    text=True
).split()

if "v1.1.0" not in tags_locales:
    subprocess.run(["git", "tag", "v1.1.0"], check=True)

subprocess.run(
    ["git", "push", "origin", "HEAD"],
    env=env_git,
    check=True
)

subprocess.run(
    ["git", "push", "origin", "v1.1.0"],
    env=env_git,
    check=True
)

print("v1.1.0 enviada a GitHub.")

14. Crear la versión v2.0.0
Celda 30 de 67

14. Crear la versión v2.0.0
En esta versión hay un cambio estructural: se agrega la columna categoria.
Por ese motivo se considera una versión mayor (2.0.0).


Celda de código 31
Celda 31 de 67

ventas_v2 = '''id_venta,fecha,producto,categoria,monto
1,2025-01-01,Laptop,Computo,15000
2,2025-01-02,Mouse,Accesorios,350
3,2025-01-03,Teclado,Accesorios,800
4,2025-01-04,Monitor,Computo,4200
'''

changelog_v2 = '''# Changelog

## v2.0.0 - 2025-01-20
- Cambio estructural del dataset.
- Se agrega columna categoria.
- Versión no compatible con v1.x.

## v1.1.0 - 2025-01-15
- Se agrega registro de venta de Monitor.
- Validación de consistencia en columna monto.

## v1.0.0 - 2025-01-10
- Dataset inicial con 3 registros de ventas.
'''

Path(os.path.join(VERSIONADO_DIR, "data", "ventas.csv")).write_text(
    ventas_v2,
    encoding="utf-8"
)

Path(os.path.join(VERSIONADO_DIR, "CHANGELOG.md")).write_text(
    changelog_v2,
    encoding="utf-8"
)

display(pd.read_csv(os.path.join(VERSIONADO_DIR, "data", "ventas.csv")))

15. Guardar y publicar v2.0.0
Celda 32 de 67

15. Guardar y publicar v2.0.0


Celda de código 33
Celda 33 de 67

os.chdir(REPO_DIR)

subprocess.run(
    ["git", "add", "practica_desde_cero/versionado-datasets-github"],
    check=True
)

subprocess.run(
    ["git", "commit", "-m", "Add categoria column to dataset v2.0.0"],
    check=True
)

tags_locales = subprocess.check_output(
    ["git", "tag"],
    text=True
).split()

if "v2.0.0" not in tags_locales:
    subprocess.run(["git", "tag", "v2.0.0"], check=True)

subprocess.run(
    ["git", "push", "origin", "HEAD"],
    env=env_git,
    check=True
)

subprocess.run(
    ["git", "push", "origin", "v2.0.0"],
    env=env_git,
    check=True
)

print("v2.0.0 enviada a GitHub.")

16. Comparar las versiones v1.1.0 y v2.0.0
Celda 34 de 67

16. Comparar las versiones v1.1.0 y v2.0.0
git diff permite ver exactamente qué cambió entre dos versiones.
Se limita la comparación a la carpeta del ejercicio.


Celda de código 35
Celda 35 de 67

os.chdir(REPO_DIR)

!git diff v1.1.0 v2.0.0 -- practica_desde_cero/versionado-datasets-github

17. Mostrar los tags y el historial
Celda 36 de 67

17. Mostrar los tags y el historial
Esto permite observar la relación entre commits y versiones.


Celda de código 37
Celda 37 de 67

os.chdir(REPO_DIR)

print("Tags:")
!git tag --list

print("\nHistorial resumido:")
!git --no-pager log --oneline --decorate -10

18. URL para comparar versiones en GitHub
Celda 38 de 67

18. URL para comparar versiones en GitHub
GitHub también puede mostrar las diferencias entre tags.


Celda de código 39
Celda 39 de 67

COMPARE_URL = (
    f"https://github.com/{GITHUB_USER}/{REPO_NAME}"
    "/compare/v1.1.0...v2.0.0"
)

print(COMPARE_URL)

PARTE B — CREAR DESDE CERO EL PROYECTO MLFLOW
Celda 40 de 67

PARTE B — CREAR DESDE CERO EL PROYECTO MLFLOW
19. Instalar las librerías
El material original utiliza:
- mlflow
- pandas
- scikit-learn
Aquí también instalamos numpy porque generaremos un dataset sintético reproducible directamente desde Colab.


Celda de código 41
Celda 41 de 67

!pip install -q mlflow pandas scikit-learn numpy

import mlflow
print("Versión de MLflow:", mlflow.__version__)

20. Crear requirements.txt
Celda 42 de 67

20. Crear requirements.txt
Este archivo documenta las dependencias necesarias para reproducir el proyecto.


Celda de código 43
Celda 43 de 67

Path(os.path.join(MLFLOW_DIR, "requirements.txt")).write_text(
    "mlflow\npandas\nscikit-learn\nnumpy\n",
    encoding="utf-8"
)

print(
    Path(os.path.join(MLFLOW_DIR, "requirements.txt"))
    .read_text(encoding="utf-8")
)

21. Crear data.csv desde cero
Celda 44 de 67

21. Crear data.csv desde cero
El material original proporciona un CSV sintético.
Para que esta adaptación sea completamente reproducible en Colab, aquí generamos un dataset sintético con:
- edad
- ingreso
- compras
- target
Se fija una semilla para que los mismos datos puedan reproducirse.


Celda de código 45
Celda 45 de 67

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 200

edad = rng.integers(22, 56, size=n)
ingreso = rng.integers(25000, 70001, size=n)
compras = rng.integers(1, 8, size=n)

# Regla sencilla para generar la variable objetivo.
# No utiliza etiquetas humanas: es un dataset sintético para la práctica.
target = ((ingreso > 45000) & (compras > 4)).astype(int)

data_mlflow = pd.DataFrame({
    "edad": edad,
    "ingreso": ingreso,
    "compras": compras,
    "target": target
})

MLFLOW_DATA_PATH = os.path.join(MLFLOW_DIR, "data.csv")
data_mlflow.to_csv(MLFLOW_DATA_PATH, index=False)

print("Dataset creado:", MLFLOW_DATA_PATH)
print("Registros:", len(data_mlflow))

display(data_mlflow.head())
print("\nDistribución de target:")
display(data_mlflow["target"].value_counts())

22. Crear train.py
Celda 46 de 67

22. Crear train.py
El programa:
1. recibe C y max_iter;
2. carga data.csv;
3. divide los datos 80/20;
4. entrena una regresión logística;
5. calcula accuracy;
6. registra en MLflow:
   - C;
   - max_iter;
   - accuracy;
   - el modelo.
Se utiliza explícitamente sqlite:///mlflow.db para que el entrenamiento y la interfaz gráfica consulten la misma base de datos.


Celda de código 47
Celda 47 de 67

train_code = r'''
import argparse
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# ------------------------------------------------------------
# 1. HIPERPARÁMETROS
# ------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument(
    "--C",
    type=float,
    default=1.0,
    help="Inverso de la intensidad de regularización."
)

parser.add_argument(
    "--max_iter",
    type=int,
    default=200,
    help="Número máximo de iteraciones."
)

args = parser.parse_args()

C = args.C
max_iter = args.max_iter


# ------------------------------------------------------------
# 2. CONFIGURACIÓN DE MLFLOW
# ------------------------------------------------------------
# La base mlflow.db se creará en la carpeta actual.
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Clasificacion_Clientes")


# ------------------------------------------------------------
# 3. CARGAR DATOS
# ------------------------------------------------------------
data = pd.read_csv("data.csv")

X = data.drop("target", axis=1)
y = data["target"]


# ------------------------------------------------------------
# 4. DIVIDIR DATOS
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ------------------------------------------------------------
# 5. ENTRENAR Y REGISTRAR EL RUN
# ------------------------------------------------------------
with mlflow.start_run():

    mlflow.log_param("C", C)
    mlflow.log_param("max_iter", max_iter)

    model = LogisticRegression(
        C=C,
        max_iter=max_iter
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="modelo"
    )

    print("--------------------------------")
    print("C:", C)
    print("max_iter:", max_iter)
    print("Accuracy:", accuracy)
    print("--------------------------------")
'''

Path(os.path.join(MLFLOW_DIR, "train.py")).write_text(
    train_code,
    encoding="utf-8"
)

print("train.py creado.")

23. Verificar la estructura del proyecto MLflow
Celda 48 de 67

23. Verificar la estructura del proyecto MLflow


Celda de código 49
Celda 49 de 67

for nombre in sorted(os.listdir(MLFLOW_DIR)):
    print(nombre)

24. Ejecutar el primer experimento
Celda 50 de 67

24. Ejecutar el primer experimento
Cada ejecución de train.py crea un run independiente.


Celda de código 51
Celda 51 de 67

os.chdir(MLFLOW_DIR)

!python train.py --C 1.0 --max_iter 200

25. Ejecutar varias configuraciones de C
Celda 52 de 67

25. Ejecutar varias configuraciones de C
Esto reproduce el objetivo del tuning del material original sin editar manualmente train.py entre cada prueba.


Celda de código 53
Celda 53 de 67

os.chdir(MLFLOW_DIR)

!python train.py --C 0.01
!python train.py --C 0.1
!python train.py --C 1
!python train.py --C 10

26. Consultar los runs desde Python
Celda 54 de 67

26. Consultar los runs desde Python
Antes de abrir la interfaz gráfica podemos revisar la tabla de resultados.


Celda de código 55
Celda 55 de 67

import mlflow
import pandas as pd

os.chdir(MLFLOW_DIR)

mlflow.set_tracking_uri("sqlite:///mlflow.db")

runs = mlflow.search_runs(
    experiment_names=["Clasificacion_Clientes"]
)

columnas = [
    "run_id",
    "params.C",
    "params.max_iter",
    "metrics.accuracy"
]

resultados = runs[columnas].copy()
resultados = resultados.sort_values(
    by="metrics.accuracy",
    ascending=False
)

display(resultados)

27. Iniciar el servidor MLflow en Colab
Celda 56 de 67

27. Iniciar el servidor MLflow en Colab
En una computadora local se abriría http://localhost:5000.
En Colab el entorno es remoto. Por eso:
1. iniciamos MLflow en el puerto 5000;
2. esperamos hasta que el puerto esté disponible;
3. en la siguiente celda usamos el proxy interno de Colab.
--workers 1 reduce el consumo de recursos.
--disable-security-middleware se utiliza solo para esta práctica temporal dentro de Colab.


Celda de código 57
Celda 57 de 67

import subprocess
import socket
import time
import os

os.chdir(MLFLOW_DIR)

# Cerrar un servidor anterior que pudiera estar usando el puerto 5000.
os.system("fuser -k 5000/tcp >/dev/null 2>&1")

log_file = open("/tmp/mlflow.log", "w")

mlflow_process = subprocess.Popen(
    [
        "mlflow",
        "server",
        "--backend-store-uri", "sqlite:///mlflow.db",
        "--host", "127.0.0.1",
        "--port", "5000",
        "--workers", "1",
        "--disable-security-middleware"
    ],
    stdout=log_file,
    stderr=subprocess.STDOUT,
    cwd=MLFLOW_DIR
)

servidor_listo = False

for intento in range(1, 61):
    try:
        with socket.create_connection(
            ("127.0.0.1", 5000),
            timeout=1
        ):
            print(
                f"✓ Servidor MLflow listo "
                f"(intento {intento})."
            )
            servidor_listo = True
            break
    except OSError:
        time.sleep(1)

if not servidor_listo:
    print("✗ MLflow no abrió el puerto 5000.")
    print("Revisa el log con:")
    print("!cat /tmp/mlflow.log")

28. Mostrar la interfaz de MLflow dentro de Colab
Celda 58 de 67

28. Mostrar la interfaz de MLflow dentro de Colab
Este método sustituye a abrir manualmente localhost:5000.


Celda de código 59
Celda 59 de 67

from google.colab.output import serve_kernel_port_as_iframe

serve_kernel_port_as_iframe(
    5000,
    width="100%",
    height="800"
)

29. Qué observar en MLflow
Celda 60 de 67

29. Qué observar en MLflow
En:
Experiments
└── Clasificacion_Clientes
    └── Training runs
activa en Columns:
- params.C
- params.max_iter
- metrics.accuracy
Cada fila es un run diferente.
Run
├── Parámetros
│   ├── C
│   └── max_iter
├── Métrica
│   └── accuracy
└── Artefacto
    └── modelo


30. Guardar el proyecto MLflow en Git
Celda 61 de 67

30. Guardar el proyecto MLflow en Git
Solo se versionarán:
- data.csv
- train.py
- requirements.txt
Los archivos internos de MLflow quedan excluidos mediante .gitignore.


Celda de código 62
Celda 62 de 67

os.chdir(REPO_DIR)

subprocess.run(
    ["git", "add",
     ".gitignore",
     "practica_desde_cero/mlflow_project/data.csv",
     "practica_desde_cero/mlflow_project/train.py",
     "practica_desde_cero/mlflow_project/requirements.txt"],
    check=True
)

print("Archivos preparados para commit:")
subprocess.run(["git", "status", "--short"], check=False)

31. Crear el commit del proyecto MLflow y enviarlo a GitHub
Celda 63 de 67

31. Crear el commit del proyecto MLflow y enviarlo a GitHub


Celda de código 64
Celda 64 de 67

os.chdir(REPO_DIR)

# Si no hay cambios, git commit devolverá un código distinto de 0.
# Por eso no usamos check=True en el commit.
subprocess.run(
    ["git", "commit", "-m",
     "Add MLflow experiment configured for Google Colab"],
    check=False
)

subprocess.run(
    ["git", "push", "origin", "HEAD"],
    env=env_git,
    check=True
)

print("Proyecto MLflow enviado a GitHub.")

32. Verificación final del repositorio
Celda 65 de 67

32. Verificación final del repositorio
Al finalizar deberías tener en GitHub:
tema12-mlflow-colab/
├── practica_desde_cero/
│   ├── versionado-datasets-github/
│   │   ├── data/
│   │   │   └── ventas.csv
│   │   ├── CHANGELOG.md
│   │   └── README.md
│   │
│   └── mlflow_project/
│       ├── data.csv
│       ├── train.py
│       └── requirements.txt
│
└── .gitignore
Y los tags:
v1.0.0
v1.1.0
v2.0.0


Celda de código 66
Celda 66 de 67

os.chdir(REPO_DIR)

print("Estado final:")
!git status

print("\nTags:")
!git tag --list

print("\nÚltimos commits:")
!git --no-pager log --oneline --decorate -10

33. Antes de cerrar Colab
Celda 67 de 67

33. Antes de cerrar Colab
Recuerda que /content/ es temporal.
Antes de terminar la sesión:
1. verifica git status;
2. confirma que los commits estén en GitHub;
3. confirma que los tags aparezcan en GitHub;
4. guarda también el notebook si lo deseas mediante:
Archivo → Guardar una copia en GitHub.
Nota sobre los tags
Los tags de Git pertenecen al repositorio completo, no únicamente a la carpeta versionado-datasets-github.
En esta práctica representan los commits en los que se publicaron las versiones del dataset.


---

## T15-T16: FastAPI y Docker

La continuación para despliegue local, API, frontend mínimo, Docker y preparación de **Proyecto Final Fase II** está documentada en:

- [README de la práctica T15-T16](practica_windows_desde_cero/mlflow_project/README.md)
- [Guía del estudiante](practica_windows_desde_cero/mlflow_project/docs/GUIA_ESTUDIANTE_T15_T16.md)
- [Guía docente](practica_windows_desde_cero/mlflow_project/docs/GUIA_DOCENTE_T15_T16.md)

La práctica reutiliza el modelo de MLflow, genera `model.pkl`, lo expone mediante FastAPI y valida su ejecución dentro de Docker.
