# Práctica: Git, GitHub, versionado de datasets y MLflow en Google Colab

https://colab.research.google.com/drive/17Q4GbCtioqjnHi-26Q_CHwSTDbPnN282?usp=sharing

Este repositorio contiene una práctica guiada para trabajar con **Git, GitHub y MLflow desde Google Colab**.

El objetivo es comprender dos aspectos diferentes de la reproducibilidad en proyectos de Machine Learning:

1. **Versionado de archivos y datasets con Git/GitHub.**
2. **Seguimiento de experimentos de Machine Learning con MLflow.**

La práctica se ejecuta principalmente desde el notebook:

`Practica_Git_Versionado_MLflow_Colab_DESDE_CERO.ipynb`

---

## Objetivos de aprendizaje

Al finalizar la práctica se podrá:

- Clonar un repositorio de GitHub desde Google Colab.
- Configurar Git dentro de Colab.
- Modificar archivos desde un notebook.
- Crear commits y tags.
- Enviar cambios desde Colab hacia GitHub.
- Aplicar versionado semántico a un dataset.
- Comparar diferentes versiones de un dataset.
- Crear un proyecto de Machine Learning reproducible.
- Registrar hiperparámetros, métricas y modelos con MLflow.
- Ejecutar diferentes configuraciones experimentales.
- Comparar los resultados de varios experimentos.
- Visualizar MLflow directamente dentro de Google Colab.

---

# Arquitectura general de la práctica

La práctica permite observar la diferencia entre **versionado del proyecto** y **seguimiento experimental**.

```text
                   PROYECTO DE MACHINE LEARNING
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             Git/GitHub                  MLflow
                 │                         │
        Versionado de archivos     Tracking experimental
                 │                         │
        ┌────────┼────────┐       ┌────────┼────────┐
        ▼        ▼        ▼       ▼        ▼        ▼
      Código   Dataset   Docs   Parámetros Métricas Modelo
```

En términos sencillos:

**Git/GitHub responde:**

> ¿Qué cambió en mis archivos?

**MLflow responde:**

> ¿Qué ocurrió cuando ejecuté mi modelo?

---

# Estructura generada por la práctica

El notebook utiliza el repositorio existente, pero crea las prácticas dentro de una carpeta independiente:

```text
tema12-mlflow-colab/
│
├── practica_desde_cero/
│   │
│   ├── versionado-datasets-github/
│   │   │
│   │   ├── data/
│   │   │   └── ventas.csv
│   │   │
│   │   ├── CHANGELOG.md
│   │   └── README.md
│   │
│   └── mlflow_project/
│       │
│       ├── data.csv
│       ├── train.py
│       └── requirements.txt
│
├── .gitignore
│
└── Practica_Git_Versionado_MLflow_Colab_DESDE_CERO.ipynb
```

Los archivos generados internamente por MLflow no se almacenan en GitHub:

```text
mlflow.db
mlruns/
mlartifacts/
```

Estos elementos se excluyen mediante `.gitignore`.

---

# Parte A. Versionado de datasets con Git y GitHub

En esta sección se simula la evolución de un dataset de ventas.

El archivo principal es:

```text
practica_desde_cero/versionado-datasets-github/data/ventas.csv
```

Se utilizan tres versiones.

---

## Versión 1.0.0

Dataset inicial con tres registros:

```csv
id_venta,fecha,producto,monto
1,2025-01-01,Laptop,15000
2,2025-01-02,Mouse,350
3,2025-01-03,Teclado,800
```

Esta versión se registra mediante:

```bash
git add .
git commit -m "Add initial sales dataset v1.0.0"
git tag v1.0.0
```

La versión representa el estado inicial del dataset.

---

## Versión 1.1.0

Se agrega un nuevo registro:

```csv
4,2025-01-04,Monitor,4200
```

El dataset queda:

```csv
id_venta,fecha,producto,monto
1,2025-01-01,Laptop,15000
2,2025-01-02,Mouse,350
3,2025-01-03,Teclado,800
4,2025-01-04,Monitor,4200
```

Se registra con:

```bash
git add .
git commit -m "Add new record to sales dataset v1.1.0"
git tag v1.1.0
```

La estructura del dataset no cambia, por lo que se mantiene dentro de la familia `v1.x`.

---

## Versión 2.0.0

Se realiza un cambio estructural agregando la columna:

```text
categoria
```

El dataset queda:

```csv
id_venta,fecha,producto,categoria,monto
1,2025-01-01,Laptop,Computo,15000
2,2025-01-02,Mouse,Accesorios,350
3,2025-01-03,Teclado,Accesorios,800
4,2025-01-04,Monitor,Computo,4200
```

Este cambio modifica el esquema del dataset y se considera una nueva versión mayor:

```bash
git add .
git commit -m "Add categoria column to dataset v2.0.0"
git tag v2.0.0
```

---

# Versionado semántico utilizado

La práctica utiliza una adaptación sencilla de **Semantic Versioning**:

```text
MAJOR.MINOR.PATCH
```

Ejemplo:

```text
v1.0.0
v1.1.0
v2.0.0
```

Interpretación en esta práctica:

| Versión | Significado |
|---|---|
| `v1.0.0` | Dataset inicial |
| `v1.1.0` | Se agregan registros sin modificar la estructura |
| `v2.0.0` | Cambio estructural del dataset |

---

# CHANGELOG

Cada modificación del dataset también se documenta en:

```text
CHANGELOG.md
```

Ejemplo:

```markdown
# Changelog

## v2.0.0 - 2025-01-20
- Cambio estructural del dataset.
- Se agrega columna categoria.
- Versión no compatible con v1.x.

## v1.1.0 - 2025-01-15
- Se agrega registro de venta de Monitor.
- Validación de consistencia en columna monto.

## v1.0.0 - 2025-01-10
- Dataset inicial con 3 registros de ventas.
```

Esto permite conocer no solamente **qué versión existe**, sino también **qué cambió en cada versión**.

---

# Comparar versiones

Git permite observar exactamente qué cambió entre dos versiones.

Por ejemplo:

```bash
git diff v1.1.0 v2.0.0
```

En la práctica se limita la comparación a la carpeta correspondiente al dataset.

También pueden consultarse las diferencias directamente desde GitHub utilizando:

```text
https://github.com/MinaNik229/tema12-mlflow-colab/compare/v1.1.0...v2.0.0
```

---

# Parte B. Gestión de experimentos con MLflow

La segunda parte crea desde cero un pequeño proyecto de Machine Learning.

La estructura es:

```text
mlflow_project/
│
├── data.csv
├── train.py
└── requirements.txt
```

---

## Dataset

Para que la práctica sea completamente reproducible desde Colab, el notebook genera automáticamente un dataset sintético.

Las variables son:

| Variable | Descripción |
|---|---|
| `edad` | Edad simulada del cliente |
| `ingreso` | Ingreso simulado |
| `compras` | Número de compras |
| `target` | Variable objetivo de clasificación |

Se utiliza una semilla fija para permitir que los datos puedan reproducirse.

---

# Modelo utilizado

Se utiliza:

```text
LogisticRegression
```

de `scikit-learn`.

La división utilizada es:

```text
80 % entrenamiento
20 % prueba
```

La métrica principal es:

```text
Accuracy
```

---

# ¿Qué registra MLflow?

Cada ejecución del modelo crea un **run** independiente.

MLflow registra:

### Parámetros

```text
C
max_iter
```

### Métrica

```text
accuracy
```

### Artefacto

```text
modelo
```

Conceptualmente:

```text
Run
│
├── Parameters
│   ├── C
│   └── max_iter
│
├── Metrics
│   └── accuracy
│
└── Artifacts
    └── modelo
```

---

# Experimentos realizados

La práctica ejecuta diferentes valores del hiperparámetro `C`:

```text
C = 0.01
C = 0.1
C = 1
C = 10
```

Cada ejecución se almacena como un run diferente dentro del experimento:

```text
Clasificacion_Clientes
```

Esto permite comparar:

```text
hiperparámetro
      ↓
entrenamiento
      ↓
métrica
      ↓
resultado
```

---

# Ejecución del modelo

Ejemplo:

```bash
python train.py --C 0.01
python train.py --C 0.1
python train.py --C 1
python train.py --C 10
```

De esta forma no es necesario modificar manualmente `train.py` para probar cada configuración.

---

# MLflow en Google Colab

En una computadora local normalmente se abriría MLflow mediante:

```text
http://localhost:5000
```

Sin embargo, Google Colab ejecuta Python en una máquina remota.

Por esta razón la práctica utiliza el proxy interno de Colab:

```python
from google.colab.output import serve_kernel_port_as_iframe

serve_kernel_port_as_iframe(
    5000,
    width="100%",
    height="800"
)
```

Esto permite visualizar la interfaz de MLflow directamente dentro del notebook.

---

# Flujo de MLflow

```text
data.csv
   │
   ▼
train.py
   │
   ├── C
   └── max_iter
   │
   ▼
LogisticRegression
   │
   ▼
Accuracy
   │
   ▼
MLflow
   │
   ├── Parameters
   ├── Metrics
   └── Model
```

---

# Git y GitHub desde Google Colab

Google Colab incluye Git, por lo que se pueden utilizar directamente comandos como:

```bash
git clone
git status
git diff
git add
git commit
git tag
git pull
git push
```

El flujo utilizado es:

```text
GitHub
   │
   │ git clone / git pull
   ▼
Google Colab
   │
   │ modificar archivos
   ▼
git add
   │
git commit
   │
git push
   ▼
GitHub
```

---

# Autenticación con GitHub

Para clonar un repositorio público no se requiere autenticación.

Sin embargo, para ejecutar:

```bash
git push
```

es necesario autenticarse.

La práctica utiliza un **Personal Access Token (PAT)** almacenado mediante los **Secrets de Google Colab**.

En Colab se debe crear:

```text
GITHUB_TOKEN
```

desde el panel de Secrets.

> No escribas el token directamente dentro del notebook ni lo publiques en GitHub.

---

# Requisitos

La práctica está diseñada para ejecutarse en:

- Google Colab
- Python 3
- Git
- GitHub

Librerías principales:

```text
mlflow
pandas
scikit-learn
numpy
```

Se instalan automáticamente desde el notebook.

---

# Ejecución

## 1. Abrir el notebook

Abre:

```text
Practica_Git_Versionado_MLflow_Colab_DESDE_CERO.ipynb
```

en Google Colab.

---

## 2. Configurar los datos personales

Al inicio del notebook modifica:

```python
GITHUB_USER = "MinaNik229"
REPO_NAME = "tema12-mlflow-colab"

GIT_NAME = "TU NOMBRE"
GIT_EMAIL = "TU_CORREO_DE_GITHUB"
```

---

## 3. Crear el secreto de GitHub

En Google Colab:

```text
Secrets
   ↓
GITHUB_TOKEN
```

Agrega tu Personal Access Token y permite el acceso del notebook.

---

## 4. Ejecutar las celdas en orden

Se recomienda:

```text
Entorno de ejecución
↓
Ejecutar todo
```

o ejecutar las celdas secuencialmente para observar cada etapa del proceso.

---

# Importante sobre Google Colab

El directorio:

```text
/content/
```

es temporal.

Cuando la sesión de Colab termina, los archivos locales pueden desaparecer.

Por ello, antes de finalizar una sesión se recomienda ejecutar:

```bash
git status
git add .
git commit -m "mensaje"
git push
```

y verificar que los cambios aparezcan correctamente en GitHub.

---

# Resultado esperado

Al finalizar la práctica se habrá trabajado con dos mecanismos complementarios:

| Herramienta | Función |
|---|---|
| Git | Control de versiones local |
| GitHub | Repositorio remoto y colaboración |
| Git tags | Identificación de versiones |
| CHANGELOG | Documentación de cambios |
| MLflow | Seguimiento de experimentos |
| Colab | Entorno de ejecución |

El resultado conceptual es:

```text
                    PROYECTO
                       │
          ┌────────────┴────────────┐
          │                         │
      Git/GitHub                  MLflow
          │                         │
     Versiones                  Experimentos
          │                         │
   v1.0 → v1.1 → v2.0       Run1 → Run2 → Run3
          │                         │
     ¿qué cambió?          ¿qué configuración funcionó?
```

---

# Conceptos clave

### Git
Sistema de control de versiones que registra cambios realizados en archivos.

### GitHub
Plataforma remota que permite almacenar y compartir repositorios Git.

### Commit
Registro de un conjunto de cambios dentro del historial del proyecto.

### Tag
Etiqueta asociada a un commit específico, utilizada para identificar versiones.

### Versionado semántico
Convención para identificar versiones mediante:

```text
MAJOR.MINOR.PATCH
```

### MLflow
Plataforma para administrar y comparar experimentos de Machine Learning.

### Run
Una ejecución individual de un experimento.

### Parámetro
Valor configurado antes de entrenar un modelo.

Ejemplo:

```text
C = 0.1
```

### Métrica
Valor utilizado para evaluar el desempeño del modelo.

Ejemplo:

```text
accuracy
```

### Artefacto
Archivo producido durante un experimento.

Ejemplo:

```text
modelo entrenado
```

---

# Idea principal de la práctica

Git/GitHub y MLflow resuelven problemas diferentes pero complementarios.

```text
Git/GitHub
    │
    └── ¿Qué versión del proyecto produjo el resultado?

MLflow
    │
    └── ¿Qué configuración experimental produjo el resultado?
```

Juntos permiten mejorar la **trazabilidad, reproducibilidad y organización de proyectos de Machine Learning**.
