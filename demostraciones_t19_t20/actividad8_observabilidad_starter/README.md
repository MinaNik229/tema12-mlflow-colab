# Actividad 8 - Starter de monitorización, observabilidad e incidentes

Este código base **no es una solución única ni obligatoria**. Su objetivo es ofrecer una estructura mínima para que adaptes la Actividad 8 a tu propio proyecto, independientemente de si trabajas con:

- machine learning clásico;
- deep learning;
- datos tabulares o numéricos;
- texto / NLP;
- imágenes;
- señales;
- audio;
- video;
- APIs o servicios de inferencia.

La idea central es convertir el comportamiento de tu proyecto en **indicadores observables** y conectar esos indicadores con **SLO, alertas, runbooks e incidentes simulados**.

---

## 1. Qué cubre este starter

El flujo educativo es:

```text
baseline
   ↓
lote / ejecución actual
   ↓
métricas + logs + trazas simplificadas
   ↓
data drift (demo tabular con PSI)
   ↓
comparación con SLO / umbrales
   ↓
alertas
   ↓
runbook
   ↓
incidente simulado
   ↓
respuesta / rollback / retraining / escalamiento
   ↓
evidencia
```

El código genera:

- métricas operativas;
- una medida didáctica de drift para variables numéricas;
- logs JSONL;
- trazas simplificadas por etapas;
- alertas con severidad;
- cálculo simple de consumo de error budget del servicio;
- registro opcional en MLflow;
- una gráfica tipo dashboard;
- escenarios de incidente simulados.

---

# 2. Lo que este starter NO hace

No intenta resolver automáticamente todos los proyectos.

Por ejemplo:

- no calcula Dice para una segmentación si tú no le proporcionas esa métrica;
- no interpreta imágenes o videos crudos de forma universal;
- no conoce el significado clínico, financiero o industrial de tus variables;
- no decide qué SLO es correcto para tu proyecto;
- no sustituye la justificación técnica del documento de la actividad.

**Tú debes adaptar qué indicadores observar y por qué.**

---

# 3. Cómo adaptar diferentes modalidades

La idea es transformar cada modalidad en indicadores numéricos que puedan ser monitoreados.

| Proyecto | Ejemplos de calidad | Ejemplos de operación | Ejemplos de drift / entrada |
|---|---|---|---|
| Clasificación | F1, recall, AUC | latencia, error rate | features, clases, confianza |
| Regresión | RMSE, MAE | latencia, error rate | features, residuales, predicción |
| Imagen | Dice, IoU, F1 | latencia, GPU | brillo, contraste, resolución, embeddings |
| Texto/NLP | F1, ROUGE, score propio | latencia, errores | longitud, idioma, embeddings, confianza |
| Señales | F1, RMSE, score propio | latencia, missing rate | RMS, media, std, bandas de frecuencia |
| Video | mAP, F1, IoU | FPS, latencia, GPU | resolución, brillo, movimiento, embeddings |

Consulta `config/examples/` para ideas y `src/project_adapter_template.py` para una plantilla de adaptación.

---

# 4. Primera vez: clonar el repositorio

## Windows / PowerShell

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab\demostraciones_t19_t20\actividad8_observabilidad_starter
code .
```

## macOS / Linux

```bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab/demostraciones_t19_t20/actividad8_observabilidad_starter
code .
```

Si ya tienes el repositorio:

```bash
git status
git switch main
git pull origin main
```

Haz `pull` solo después de revisar que no tengas cambios locales sin guardar.

---

# 5. Crear el entorno virtual

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
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# 6. Ejecutar la demostración base

## Paso 1. Generar datos normales

### Windows

```powershell
python data\generate_demo_data.py
```

### macOS / Linux

```bash
python data/generate_demo_data.py
```

Se crean localmente:

```text
data/baseline.csv
data/current.csv
```

El baseline representa el comportamiento de referencia y `current.csv` una ventana actual inicialmente normal.

## Paso 2. Ejecutar monitorización

### Windows

```powershell
python src\monitor.py
```

### macOS / Linux

```bash
python src/monitor.py
```

El monitor calcula, cuando las columnas existen:

```text
quality
latency_p95_ms
error_rate
drift_psi
service_success_rate
error_budget_consumed_pct
```

También crea:

```text
outputs/monitoring_summary.json
outputs/alerts.json
outputs/monitoring_log.jsonl
outputs/traces.jsonl
```

### ¿Qué representa cada archivo?

- `monitoring_summary.json`: estado general de la ejecución.
- `alerts.json`: reglas que cruzaron warning o critical.
- `monitoring_log.jsonl`: eventos registrados como logs.
- `traces.jsonl`: duración simplificada de etapas del pipeline.

Las trazas de este starter son **educativas**; no sustituyen OpenTelemetry en un sistema distribuido real.

## Paso 3. Crear dashboard

```bash
python src/dashboard.py
```

Genera:

```text
outputs/dashboard.png
```

No tienes que conservar este diseño. Úsalo como punto de partida y reemplázalo por un dashboard apropiado para tu proyecto.

---

# 7. Simular los dos incidentes requeridos

La actividad solicita al menos dos incidentes simulados. Este starter incluye cuatro escenarios.

## Incidente A - Data drift

### Windows

```powershell
python src\simulate_incidents.py --scenario drift
python src\monitor.py
python src\dashboard.py
```

### macOS / Linux

```bash
python src/simulate_incidents.py --scenario drift
python src/monitor.py
python src/dashboard.py
```

## Incidente B - Latencia alta

```bash
python src/simulate_incidents.py --scenario latency
python src/monitor.py
python src/dashboard.py
```

## Otras opciones

```bash
python src/simulate_incidents.py --scenario degradation
python src/simulate_incidents.py --scenario errors
```

Después de cada simulación guarda evidencia de:

1. estado antes;
2. alerta activada;
3. runbook utilizado;
4. acción aplicada;
5. estado después.

---

# 8. Abrir MLflow

El monitor registra sus métricas en MLflow porque `config/monitoring_config.json` tiene:

```json
"mlflow": {
  "enabled": true,
  "experiment_name": "Actividad8_Observabilidad"
}
```

Ejecuta:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Abre:

```text
http://localhost:5000
```

Busca el experimento:

```text
Actividad8_Observabilidad
```

Toma capturas de parámetros, métricas y artefactos relevantes para tu evidencia.

---

# 9. SLO, alertas y error budget

El archivo `config/monitoring_config.json` contiene umbrales de ejemplo.

Ejemplo:

```json
"latency_p95_ms": {
  "direction": "max",
  "warning": 350,
  "critical": 500
}
```

Esto significa:

```text
latencia < 350 ms     → OK
350–499 ms            → warning
≥ 500 ms              → critical
```

Estos valores son didácticos. **No los copies sin justificar.** Cámbialos según el baseline y riesgo de tu proyecto.

El starter también utiliza un SLO de éxito del servicio. Si el objetivo es 95% de solicitudes exitosas, el error budget permitido es 5%. El script muestra cuánto de ese presupuesto se está consumiendo.

---

# 10. Cómo adaptar el código a tu proyecto real

## Opción A - Ya produces métricas numéricas

Adapta tu pipeline para crear columnas/indicadores equivalentes a:

```text
quality_score
latency_ms
is_error
```

y cambia sus nombres en `config/monitoring_config.json`.

## Opción B - Tu proyecto usa imágenes, texto, señales o video

No intentes pasar el dato crudo al monitor genérico.

Primero extrae indicadores, por ejemplo:

```text
imagen → brillo, resolución, embedding, Dice
texto → longitud, idioma, embedding, confianza
señal → RMS, media, std, banda de frecuencia
video → FPS, resolución, motion score, embedding
```

Después guarda esos indicadores en una tabla por observación o por lote.

Revisa:

```text
src/project_adapter_template.py
config/examples/
```

## Opción C - No tienes etiquetas en “producción”

Es normal que la métrica de calidad real no esté disponible inmediatamente.

Puedes monitorizar temporalmente:

- confianza del modelo;
- distribución de predicciones;
- data drift;
- calidad de entrada;
- tasa de errores;
- latencia;
- señales de negocio.

Cuando las etiquetas lleguen, incorpora la métrica real de desempeño.

---

# 11. Runbooks

Utiliza `runbooks/RUNBOOK_TEMPLATE.md`.

Crea al menos un runbook por tipo de incidente simulado o justifica cuándo un mismo runbook cubre varios escenarios.

Ejemplo:

```text
ALERTA: drift crítico
    ↓
validar que el cambio sea real
    ↓
revisar variables afectadas
    ↓
evaluar desempeño si existen etiquetas
    ↓
reentrenar / escalar / rechazar lote
    ↓
validar recuperación
```

---

# 12. Relación con los entregables de la Actividad 8

## Entregable 1 - Documento técnico

Puedes partir de `docs/ACTIVITY8_TECHNICAL_DOCUMENT_TEMPLATE.md`.

Incluye métricas, logs y trazas; alertas inteligentes; dashboards; runbooks; data drift y respuesta automatizada.

## Entregable 2 - Evidencia de implementación

Captura o exporta:

- MLflow / W&B;
- dashboard;
- alertas;
- logs;
- resultados de drift;
- estado antes/después.

## Entregable 3 - Simulación de incidentes

Registra al menos dos incidentes:

```text
incidente
→ detección
→ alerta
→ runbook
→ acción
→ recuperación
```

## Entregable 4 - Código/configuración

Incluye los scripts que realmente utilizaste o adaptaste. No es necesario entregar código que no forme parte de tu solución.

---

# 13. Estructura sugerida del ZIP final

```text
Actividad8_EquipoXX.zip
├── 01_documento_tecnico.pdf
├── 02_evidencia_implementacion.pdf
├── 03_incidentes_runbooks.pdf
└── 04_codigo/
    ├── monitor.py
    ├── dashboard.py
    ├── config/
    ├── runbooks/
    └── README.md
```

---

# 14. Qué se evalúa realmente

No se evalúa que todos utilicen el mismo stack. Se evalúa que exista coherencia entre:

```text
indicador
   ↓
objetivo / SLO
   ↓
alerta
   ↓
incidente
   ↓
runbook
   ↓
respuesta
   ↓
evidencia de recuperación
```

Un proyecto de deep learning puede tener una implementación muy distinta a uno tabular, pero ambos deben demostrar esa lógica operacional.

---

# 15. Atajos de ejecución

## Windows

```powershell
.\demo.ps1 data
.\demo.ps1 monitor
.\demo.ps1 drift
.\demo.ps1 monitor
.\demo.ps1 dashboard
.\demo.ps1 ui
```

## macOS / Linux

```bash
bash demo.sh data
bash demo.sh monitor
bash demo.sh drift
bash demo.sh monitor
bash demo.sh dashboard
bash demo.sh ui
```

---

# 16. Antes de subir cambios a Git

Los resultados de ejecución están ignorados para evitar que interfieran con otros alumnos.

Revisa siempre:

```bash
git status
git status --short
```

No uses `git add .` sin revisar qué archivos vas a versionar.

El starter es una **referencia adaptable**: conserva solo lo que realmente sea útil para tu proyecto y documenta las decisiones que tomaste.
