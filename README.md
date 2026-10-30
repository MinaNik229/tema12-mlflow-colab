# Prácticas de gestión de datos, Git/GitHub y MLflow

**Repositorio de apoyo para ejercicios de limpieza, análisis y visualización de datos, control de versiones y seguimiento de experimentos de Machine Learning.**

Los materiales incluyen notebooks, scripts Python, datasets sintéticos, documentación y prácticas ejecutables tanto en **Google Colab** como en **Windows con Visual Studio Code**.

**Repositorio:** [MinaNik229/tema12-mlflow-colab](https://github.com/MinaNik229/tema12-mlflow-colab)

## Contenido

1. [Mapa del repositorio](#mapa-del-repositorio)
2. [Qué se aprende](#qué-se-aprende)
3. [Requisitos y preparación](#requisitos-y-preparación)
4. [Práctica de limpieza y calidad de datos](#1-limpieza-y-calidad-de-datos)
5. [Análisis y visualización](#2-análisis-y-visualización-de-datos)
6. [Versionado de datasets](#3-versionado-de-datasets-con-git-y-github)
7. [Seguimiento de experimentos con MLflow](#4-seguimiento-de-experimentos-con-mlflow)
8. [Google Colab](#ejecución-desde-google-colab)
9. [Windows y VS Code](#ejecución-local-en-windows-y-vs-code)
10. [Buenas prácticas y notas](#buenas-prácticas-y-notas)

## Mapa del repositorio

```text
tema12-mlflow-colab/
├── README.md                              # Guía general (este archivo)
├── .gitignore                            # Exclusiones de Git
│
├── Fuentes/
│   ├── Tema11_EjemLimpieza.ipynb         # Notebook de limpieza y deduplicación
│   └── subir_dataset.py                  # Ejemplo de automatización de Git con GitPython
│
├── ia_project_dirty_dataset_6000.csv    # Datos sintéticos para limpieza
├── ia_project_dirty_dataset_dictionary.md
├── ia_project_quality_report.md
│
├── VisualizacionDatos/
│   ├── README.md                          # Documentación detallada de visualización
│   ├── 00_INICIO_AQUI.txt
│   ├── Analisis_Visualizacion.ipynb
│   ├── analisis_visualizacion.py
│   ├── ia_project_golden_clean.csv
│   ├── dashboard_interactivo.html
│   ├── index.html
│   ├── RESUMEN_VISUAL.md
│   ├── ANALISIS_VISUAL_ASCII.txt
│   ├── REPORTE_ANALISIS_COMPLETO.txt
│   └── otros resúmenes e instrucciones
│
├── versionado-datasets-github/          # Material previo de versionado
│   ├── data/ventas.csv
│   ├── CHANGELOG.md
│   └── README.md
│
├── practica_desde_cero/                 # Adaptación para Google Colab
│   ├── README.md                        # Guía detallada y vínculo al notebook de Colab
│   ├── versionado-datasets-github/
│   │   ├── data/ventas.csv
│   │   ├── CHANGELOG.md
│   │   └── README.md
│   └── mlflow_project/
│       ├── data.csv
│       ├── train.py
│       └── requirements.txt
│
├── practica_windows_desde_cero/         # Práctica para Windows y VS Code
│   ├── versionado-datasets-github/
│   │   ├── data/ventas.csv
│   │   ├── CHANGELOG.md
│   │   └── README.md
│   └── mlflow_project/
│       ├── generate_data.py
│       ├── data.csv
│       ├── train.py
│       └── requirements.txt
│
├── Tema11_ConfigRamaLocal_ET.docx       # Material de apoyo para Git
└── Tema11_EjemLimpieza_ET.docx          # Material de apoyo para limpieza
```

> **Importante:** las carpetas `versionado-datasets-github/`, `practica_desde_cero/` y `practica_windows_desde_cero/` contienen **ejercicios o adaptaciones diferentes**. No son tres repositorios Git independientes: todos forman parte de este mismo repositorio.

## Qué se aprende

| Área | Actividad | Herramientas |
|---|---|---|
| Preparación y calidad | Estandarizar, validar y deduplicar registros | Python, pandas, NumPy |
| Análisis exploratorio | Examinar distribuciones, correlaciones y perfiles | pandas, Matplotlib, Seaborn |
| Visualización | Generar gráficos y explorar un dashboard HTML | Python, HTML, Plotly.js |
| Control de versiones | Registrar cambios, comparar commits y crear tags | Git, GitHub |
| Machine Learning | Entrenar una regresión logística y medir `accuracy` | scikit-learn |
| Seguimiento experimental | Guardar hiperparámetros, métricas y modelos | MLflow |

**Distinción clave:** Git/GitHub responde **qué cambió en los archivos**; MLflow registra **qué configuración se ejecutó y qué resultados produjo**. Son herramientas complementarias, no sustitutas.

## Requisitos y preparación

- [Python](https://www.python.org/downloads/) y **Git** para ejecutar los scripts y versionar archivos.
- [Visual Studio Code](https://code.visualstudio.com/) para el trabajo local en Windows (recomendado).
- Una cuenta de [GitHub](https://github.com/) con permisos de escritura si se realizarán operaciones `push`.
- Como alternativa, una cuenta de Google para usar **Google Colab**.

En **PowerShell (Windows)**, revisa las instalaciones antes de descargar nada:

```powershell
winget --version
git --version
py --version
code --version
```

Si falta algún programa y `winget` está disponible:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id Python.Python.3.12 -e
```

Cierra y vuelve a abrir la terminal después de instalar. Si `py` no está disponible, comprueba `python --version`.

### Clonar el repositorio

En una terminal de VS Code o PowerShell:

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
code .
```

Si la carpeta **ya existe**, no vuelvas a clonarla. Entra en ella y, si el árbol de trabajo está limpio, actualiza:

```powershell
git status
git pull --ff-only origin main
```

### Crear un entorno virtual (Windows)

Desde la raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Si PowerShell bloquea la activación del entorno, en esa misma sesión puedes ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

En VS Code selecciona el intérprete `.venv` mediante **Python: Select Interpreter**. La carpeta `.venv/` se excluye del control de versiones.

## 1. Limpieza y calidad de datos

**Archivos principales:**

- [`ia_project_dirty_dataset_6000.csv`](ia_project_dirty_dataset_6000.csv): dataset sintético de entrada para realizar ejercicios de calidad.
- [`ia_project_dirty_dataset_dictionary.md`](ia_project_dirty_dataset_dictionary.md): diccionario de variables y ejemplos de problemas de calidad.
- [`Fuentes/Tema11_EjemLimpieza.ipynb`](Fuentes/Tema11_EjemLimpieza.ipynb): pipeline de limpieza, normalización, deduplicación y verificaciones de consistencia.
- [`ia_project_quality_report.md`](ia_project_quality_report.md): reporte de calidad **antes/después** generado para un procesamiento concreto.
- [`Fuentes/subir_dataset.py`](Fuentes/subir_dataset.py): ejemplo de automatización de commits y envío a GitHub usando **GitPython**.

El dataset de entrada contiene **6,000 registros sintéticos** diseñados para practicar formatos heterogéneos, valores faltantes, duplicados, fechas, correos electrónicos, categorías, monedas y unidades de medida.

### Ejecución sugerida

1. Abre [`Fuentes/Tema11_EjemLimpieza.ipynb`](Fuentes/Tema11_EjemLimpieza.ipynb) en Colab o en VS Code con Jupyter.
2. Coloca `ia_project_dirty_dataset_6000.csv` en la ubicación esperada por el notebook, o ajusta `SRC_CSV`.
3. Ejecuta las celdas de normalización, deduplicación y validación.
4. Examina el CSV y el reporte de calidad resultantes **antes de incorporarlos a Git**.

**Nota:** `Fuentes/subir_dataset.py` contiene rutas y URL de ejemplo que deben configurarse antes de usarse; requiere instalar `GitPython` (`python -m pip install GitPython`). No es necesario ejecutarlo si ya se utiliza Git directamente desde la terminal.

## 2. Análisis y visualización de datos

La carpeta [`VisualizacionDatos/`](VisualizacionDatos/) reúne un dataset limpio para análisis y distintos formatos de presentación de resultados.

**Puntos de entrada recomendados:**

| Recurso | Para qué sirve |
|---|---|
| [`VisualizacionDatos/README.md`](VisualizacionDatos/README.md) | Guía detallada de los recursos |
| [`VisualizacionDatos/00_INICIO_AQUI.txt`](VisualizacionDatos/00_INICIO_AQUI.txt) | Orientación inicial |
| [`VisualizacionDatos/RESUMEN_VISUAL.md`](VisualizacionDatos/RESUMEN_VISUAL.md) | Resumen en tablas y hallazgos |
| [`VisualizacionDatos/ia_project_golden_clean.csv`](VisualizacionDatos/ia_project_golden_clean.csv) | Dataset empleado en esta sección |
| [`VisualizacionDatos/Analisis_Visualizacion.ipynb`](VisualizacionDatos/Analisis_Visualizacion.ipynb) | Análisis paso a paso en notebook |
| [`VisualizacionDatos/analisis_visualizacion.py`](VisualizacionDatos/analisis_visualizacion.py) | Script para estadísticas y gráficos |
| [`VisualizacionDatos/dashboard_interactivo.html`](VisualizacionDatos/dashboard_interactivo.html) | Dashboard web para explorar desde un navegador |
| [`VisualizacionDatos/REPORTE_ANALISIS_COMPLETO.txt`](VisualizacionDatos/REPORTE_ANALISIS_COMPLETO.txt) | Resultados técnicos y análisis detallado |

Para ejecutar el script desde Windows:

```powershell
python -m pip install pandas numpy matplotlib seaborn
cd .\VisualizacionDatos
python .\analisis_visualizacion.py
```

El script lee `ia_project_golden_clean.csv` desde la carpeta de trabajo. El dashboard HTML también puede abrirse con el navegador; algunas librerías visuales pueden requerir conexión a Internet según su configuración.

**Precaución sobre versiones de datos:** el reporte de calidad de la raíz y los documentos de `VisualizacionDatos/` presentan recuentos distintos en algunos apartados. Trátalos como resultados de artefactos o ejecuciones diferentes hasta verificar sus criterios de limpieza y procedencia; no asumas automáticamente que describen exactamente la misma versión del dataset.

## 3. Versionado de datasets con Git y GitHub

Las carpetas [`practica_windows_desde_cero/versionado-datasets-github/`](practica_windows_desde_cero/versionado-datasets-github/) y [`practica_desde_cero/versionado-datasets-github/`](practica_desde_cero/versionado-datasets-github/) contienen el ejercicio de **evolución de un CSV de ventas**. También existe un ejemplo anterior en [`versionado-datasets-github/`](versionado-datasets-github/).

### Versiones didácticas

| Versión | Cambio | Estructura del CSV |
|---|---|---|
| `1.0.0` | Dataset inicial con tres ventas | `id_venta,fecha,producto,monto` |
| `1.1.0` | Se incorpora una venta de Monitor | Misma estructura |
| `2.0.0` | Se incorpora el campo `categoria` | Cambia el esquema |

Los cambios se documentan en `CHANGELOG.md`. Un **commit** registra un estado; un **tag** identifica el commit que representa una versión. Los tags pertenecen al repositorio completo, no exclusivamente a una subcarpeta.

### Ejemplo de flujo en PowerShell

Ejecuta estos comandos desde la raíz del repositorio, después de crear o modificar los archivos del dataset:

```powershell
# Ver qué cambió
git status

# Preparar solo los archivos de la práctica de Windows
git add .\practica_windows_desde_cero\versionado-datasets-github

# Guardar la primera versión
git commit -m "Add initial sales dataset v1.0.0"

# Crear un tag con prefijo para evitar confusiones con otros ejercicios
git tag dataset-v1.0.0

# Subir el commit y el tag a GitHub
git push origin main
git push origin dataset-v1.0.0
```

Repite el procedimiento para `dataset-v1.1.0` y `dataset-v2.0.0` **solo después** de realizar los cambios correspondientes. Si un tag ya existe, revísalo antes de intentar reutilizarlo o reemplazarlo.

Para comparar versiones, cuando existan ambos tags:

```powershell
git diff dataset-v1.1.0 dataset-v2.0.0 -- .\practica_windows_desde_cero\versionado-datasets-github
```

> La práctica para Colab puede usar los nombres `v1.0.0`, `v1.1.0` y `v2.0.0`, mientras que el ejemplo de Windows utiliza el prefijo `dataset-`. Consulta los tags existentes mediante `git tag` y usa los nombres correspondientes a tu ejecución.

## 4. Seguimiento de experimentos con MLflow

Hay dos implementaciones del ejercicio de clasificación:

- [`practica_windows_desde_cero/mlflow_project/`](practica_windows_desde_cero/mlflow_project/): para Windows + VS Code; incluye el generador `generate_data.py`.
- [`practica_desde_cero/mlflow_project/`](practica_desde_cero/mlflow_project/): adaptada a Colab; incluye `data.csv`, `train.py` y `requirements.txt`.

Ambas usan una **regresión logística de scikit-learn** para clasificar registros sintéticos. El proyecto utiliza `edad`, `ingreso` y `compras` como variables de entrada, y `target` como objetivo.

En cada ejecución, MLflow registra:

- **Parámetros:** `C` y `max_iter`.
- **Métrica:** `accuracy`.
- **Modelo:** artefacto registrado como `modelo`.

Cada ejecución constituye un **run** dentro del experimento `Clasificacion_Clientes`.

### Ejecución local en Windows

Desde la raíz del repositorio, con `.venv` activo:

```powershell
cd .\practica_windows_desde_cero\mlflow_project
python -m pip install -r requirements.txt

# Generar data.csv nuevamente, si se desea
python .\generate_data.py

# Entrenar con distintos valores del hiperparámetro C
python .\train.py --C 0.01
python .\train.py --C 0.1
python .\train.py --C 1
python .\train.py --C 10
```

A continuación, **sin salir de `mlflow_project`**, inicia el servidor en una terminal:

```powershell
python -m mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000 --workers 1
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador. La terminal permanecerá ocupada mientras MLflow siga ejecutándose; usa una segunda terminal para otros comandos y presiona `Ctrl+C` para detener el servidor.

En la interfaz de MLflow abre **Experiments → Clasificacion_Clientes** y muestra las columnas `params.C`, `params.max_iter` y `metrics.accuracy` para comparar runs.

## Ejecución desde Google Colab

La guía de [`practica_desde_cero/README.md`](practica_desde_cero/README.md) explica cómo adaptar Git/GitHub y MLflow a Colab y contiene un vínculo al notebook externo de la práctica.

Para abrir la interfaz en Colab, primero debe ejecutarse MLflow dentro de la sesión y quedar escuchando en el puerto 5000. Después se utiliza el proxy interno:

```python
from google.colab.output import serve_kernel_port_as_iframe

serve_kernel_port_as_iframe(5000, width="100%", height="800")
```

Esto **no** equivale a abrir `localhost:5000` desde el navegador de tu equipo: el servidor está en la máquina remota de Colab.

Para enviar cambios a GitHub desde Colab puede emplearse un token de acceso de alcance limitado guardado en **Colab Secrets**; nunca se debe incrustar un token en las celdas ni en la URL del repositorio.

## Ejecución local en Windows y VS Code

Una ruta sugerida para quienes comienzan es:

1. Verifica Python, Git y VS Code; instala únicamente las herramientas faltantes.
2. Clona el repositorio y crea un entorno virtual `.venv`.
3. Revisa los materiales de limpieza y visualización, o ejecuta directamente las prácticas de Git/MLflow.
4. Para versionado, modifica el CSV por etapas y registra cada versión mediante `git add`, `git commit` y `git tag`.
5. Para MLflow, ejecuta `train.py` desde su carpeta y abre la interfaz local en el puerto 5000.
6. Antes de terminar, revisa `git status` y envía tus cambios a GitHub con `git push`.

No vuelvas a ejecutar `git clone` sobre una carpeta existente: utiliza `git pull --ff-only` cuando sea apropiado y no tengas cambios locales sin resolver.

## Buenas prácticas y notas

- **Trabaja desde la carpeta correcta:** `data.csv` y `mlflow.db` se resuelven desde el directorio de ejecución de los scripts; ejecutar desde otra ruta puede causar errores o crear una base distinta.
- **No publiques artefactos transitorios:** `.venv/`, `mlflow.db`, `mlruns/` y `mlartifacts/` están contemplados en `.gitignore`.
- **Conserva el origen de los resultados:** el código fuente y los CSV se versionan con Git; los detalles de cada entrenamiento se registran con MLflow. La base local de MLflow no queda preservada automáticamente en GitHub.
- **Protege credenciales:** utiliza Git Credential Manager en Windows o Secrets de Colab; no publiques contraseñas ni tokens.
- **No ejecutes todos los commits de versionado de una sola vez sin revisar:** cada versión debe existir como estado verificable antes de avanzar a la siguiente.
- **Revisa consistencia de reportes:** si cambian los criterios de deduplicación o la versión del dataset, las métricas y cantidades pueden cambiar; documenta estas diferencias.
- **Reproducibilidad:** las dependencias están declaradas en archivos `requirements.txt`, pero no todas las versiones están fijadas. Para ejecuciones estrictamente reproducibles conviene documentar también las versiones exactas del entorno.

## Documentación adicional

- [Guía general de la práctica en Colab](practica_desde_cero/README.md)
- [Guía de visualización de datos](VisualizacionDatos/README.md)
- [Diccionario del dataset para limpieza](ia_project_dirty_dataset_dictionary.md)
- [Reporte de calidad de datos](ia_project_quality_report.md)
- [Material de configuración de ramas de Git](Tema11_ConfigRamaLocal_ET.docx)
- [Material de limpieza de datos](Tema11_EjemLimpieza_ET.docx)

---

**Finalidad del repositorio:** servir como espacio didáctico para practicar trazabilidad, control de versiones, preparación de datos, análisis exploratorio y administración de experimentos de Machine Learning.



---

## T15-T16: FastAPI y Docker

La continuación para despliegue local, API, frontend mínimo, Docker y preparación de **Proyecto Final Fase II** está documentada en:

- [README de la práctica T15-T16](practica_windows_desde_cero/mlflow_project/README.md)
- [Guía del estudiante](practica_windows_desde_cero/mlflow_project/docs/GUIA_ESTUDIANTE_T15_T16.md)
- [Guía docente](practica_windows_desde_cero/mlflow_project/docs/GUIA_DOCENTE_T15_T16.md)

La práctica reutiliza el modelo de MLflow, genera `model.pkl`, lo expone mediante FastAPI y valida su ejecución dentro de Docker.


---

## Demostraciones T15-T16 listas para clase

Se añadieron prácticas ejecutables para acompañar los temas de contenerización, API, Docker, despliegue y documentación técnica:

- [Índice de demostraciones T15-T16](demostraciones_t15_t16/README.md)
- [Tema 15 - Contenerización de modelo de fraude](demostraciones_t15_t16/tema15_contenedorizacion_fraude/README.md)
- [Tema 16 - Deserción, API, Docker y simulación PaaS](demostraciones_t15_t16/tema16_desercion_api_docker_nube/README.md)

Cada ejemplo incluye un `demo.ps1` para ejecutar la demostración por etapas durante la clase.
