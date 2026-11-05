# Prácticas de Gestión de Proyectos de Inteligencia Artificial

Repositorio didáctico de apoyo para las actividades del curso. Reúne ejercicios de preparación y calidad de datos, visualización, Git/GitHub, MLflow, APIs, Docker, despliegue y MLOps.

**Repositorio:** https://github.com/MinaNik229/tema12-mlflow-colab

---

## Mapa actualizado del repositorio

```text
tema12-mlflow-colab/
├── README.md
├── .gitignore
│
├── Fuentes/
│   ├── Tema11_EjemLimpieza.ipynb
│   └── subir_dataset.py
│
├── VisualizacionDatos/
│   ├── README.md
│   ├── Analisis_Visualizacion.ipynb
│   ├── analisis_visualizacion.py
│   └── recursos de análisis y visualización
│
├── versionado-datasets-github/
│   ├── data/ventas.csv
│   ├── CHANGELOG.md
│   └── README.md
│
├── practica_desde_cero/
│   ├── README.md
│   ├── versionado-datasets-github/
│   └── mlflow_project/
│
├── demostraciones_t15_t16/
│   ├── README.md
│   ├── tema15_contenedorizacion_fraude/
│   └── tema16_desercion_api_docker_nube/
│
├── demostraciones_t17_t18/
│   ├── README.md
│   └── tema17_versionado_artefactos_mlflow/
│
├── ia_project_dirty_dataset_6000.csv
├── ia_project_dirty_dataset_dictionary.md
├── ia_project_quality_report.md
├── Tema11_ConfigRamaLocal_ET.docx
└── Tema11_EjemLimpieza_ET.docx
```


---

# Ruta recomendada por tema

## Preparación y calidad de datos

Recursos principales:

- [Dataset sintético](ia_project_dirty_dataset_6000.csv)
- [Diccionario de datos](ia_project_dirty_dataset_dictionary.md)
- [Reporte de calidad](ia_project_quality_report.md)
- [Notebook de limpieza](Fuentes/Tema11_EjemLimpieza.ipynb)

Objetivo: practicar limpieza, validación, normalización, deduplicación y trazabilidad de datos.

---

## Análisis y visualización

Carpeta:

- [VisualizacionDatos](VisualizacionDatos/README.md)

Incluye notebook, script Python, dataset limpio, dashboard HTML y reportes de apoyo.

---

## Git y versionado de datasets

Práctica:

- [versionado-datasets-github](versionado-datasets-github/README.md)

Se utiliza para comprender:

```text
archivo
  ↓
cambio
  ↓
git status
  ↓
git add
  ↓
git commit
  ↓
tag / versión
  ↓
GitHub
```

---

## MLflow y seguimiento de experimentos

Para las prácticas anteriores de MLflow y ejecución en Colab:

- [practica_desde_cero](practica_desde_cero/README.md)

Conceptos centrales:

- experimentos;
- runs;
- parámetros;
- métricas;
- artefactos;
- comparación de configuraciones.

---

# Tema 15 - Contenerización de una solución de IA

Práctica actual:

- [Tema 15: contenerización de modelo de fraude](demostraciones_t15_t16/tema15_contenedorizacion_fraude/README.md)

El recorrido es:

```text
GitHub
  ↓
entorno virtual
  ↓
entrenamiento
  ↓
model.pkl
  ↓
FastAPI
  ↓
POST /predict
  ↓
Dockerfile
  ↓
docker build
  ↓
docker run
  ↓
API dentro de un contenedor
```

El README de la práctica contiene instrucciones separadas para:

- Windows / PowerShell;
- macOS / Linux / Bash-Zsh.

También incluye `demo.ps1` y `demo.sh` para realizar la demostración por etapas.

---

# Tema 16 - API, Docker, despliegue y documentación

Práctica actual:

- [Tema 16: deserción, API, Docker y simulación PaaS](demostraciones_t15_t16/tema16_desercion_api_docker_nube/README.md)

El recorrido amplía T15:

```text
modelo
  ↓
API
  ↓
consumo desde otro programa
  ↓
Docker
  ↓
estrategia PaaS
  ↓
documentación técnica
  ↓
Git / GitHub
```

Incluye:

- FastAPI;
- consumo mediante `SimulaConsumo.py`;
- Docker;
- `Procfile` como referencia de PaaS;
- plantilla y ejemplo de documentación técnica;
- instrucciones Windows y macOS/Linux.

Índice conjunto:

- [Demostraciones T15-T16](demostraciones_t15_t16/README.md)

---

# Tema 17 - Construcción y versionado de artefactos

Práctica actual:

- [Tema 17: construcción y versionado de artefactos con MLflow](demostraciones_t17_t18/tema17_versionado_artefactos_mlflow/README.md)

El laboratorio implementa:

```text
churn.csv
  ↓
validación y preprocesamiento
  ↓
Random Forest
  ↓
v1
  ├── model.pkl
  ├── metrics.json
  ├── metadata.json
  └── MLflow run
  ↓
cambio de hiperparámetro
  ↓
v2
  ├── model.pkl
  ├── metrics.json
  ├── metadata.json
  └── MLflow run
  ↓
comparación
  ↓
decisión de versión
```

Incluye:

- instrucciones desde `git clone`;
- Windows y macOS/Linux;
- MLflow;
- comparación v1/v2;
- selección documentada de versión;
- actualización del repositorio con Git.

Índice del Módulo 3:

- [Demostraciones T17-T18](demostraciones_t17_t18/README.md)

---

# Cómo obtener el repositorio

## Windows / PowerShell

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
code .
```

## macOS / Linux

```bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab
code .
```

Si ya tienes una copia local, **no vuelvas a clonar**.

Primero revisa:

```bash
git status
git status --short
```

Si el árbol está limpio:

```bash
git switch main
git pull origin main
```

---

# Entornos virtuales

## Windows

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cada práctica tiene su propio `requirements.txt` cuando necesita dependencias específicas.

---

# Git/GitHub y MLflow no versionan lo mismo

Una distinción importante durante el curso:

```text
Git / GitHub
→ cambios del código, configuración y documentación

MLflow
→ experimentos, parámetros, métricas y artefactos de modelos
```

En MLOps normalmente se utilizan juntos.

Ejemplo:

```text
commit Git
   ↓
código reproducible

MLflow run
   ↓
configuración + métrica + modelo

versión del modelo
   ↓
candidato a promoción/despliegue
```

---

# Archivos que normalmente no deben subirse

La configuración de `.gitignore` evita varios artefactos locales, por ejemplo:

```text
.venv/
__pycache__/
mlflow.db
mlruns/
mlartifacts/
```

Algunas prácticas didácticas pueden permitir pequeños `.pkl` versionados dentro de una carpeta específica para visualizar el concepto de versiones. Los modelos grandes o checkpoints de deep learning deberían almacenarse en un Model Registry o sistema de artefactos, no directamente en Git.

---

# Buenas prácticas

1. Ejecuta `git status` antes de agregar archivos.
2. No uses `git add .` automáticamente sin revisar qué vas a versionar.
3. No publiques contraseñas, tokens ni credenciales.
4. No sobrescribas una versión de modelo sin documentar por qué.
5. Una versión nueva no significa automáticamente una versión mejor.
6. Mantén README, código y estructura del repositorio sincronizados.
7. Antes de hacer `push`, integra cambios remotos cuando corresponda.
8. Conserva la trazabilidad entre código, datos, métricas y artefactos.

---

# Finalidad del repositorio

Este repositorio funciona como espacio didáctico para recorrer progresivamente:

```text
datos
 ↓
calidad
 ↓
visualización
 ↓
Git/GitHub
 ↓
MLflow
 ↓
modelo
 ↓
API
 ↓
Docker
 ↓
despliegue
 ↓
versionado de artefactos
 ↓
MLOps
```

La meta no es únicamente producir modelos, sino aprender a construir soluciones de IA que puedan **reproducirse, probarse, versionarse, desplegarse y mantenerse**.
