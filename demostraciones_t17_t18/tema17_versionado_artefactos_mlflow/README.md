# Tema 17 - Laboratorio: construcción y versionado de artefactos de modelo

Esta práctica implementa el laboratorio del Tema 17 para Windows, macOS y Linux.

El objetivo no es solamente entrenar un modelo. Al finalizar debes poder responder:

**¿Qué versión del modelo tengo, cómo fue generada, qué resultado obtuvo y por qué conservaría o reemplazaría esa versión?**

## Flujo de la actividad

~~~text
GitHub
  ↓
clonar / actualizar repositorio
  ↓
abrir la práctica en VS Code
  ↓
crear entorno virtual
  ↓
validar churn.csv
  ↓
entrenar Random Forest
  ↓
guardar artefactos
  ↓
v1 + MLflow
  ↓
cambiar hiperparámetro
  ↓
v2 + MLflow
  ↓
comparar
  ↓
seleccionar una versión
  ↓
registrar cambios con Git
~~~

---

# 0. Relación con el PDF del Tema 17

El laboratorio original propone:

1. cargar data/churn.csv;
2. revisar valores nulos y tipos de datos;
3. eliminar nulos y separar X / y;
4. realizar un split 80/20;
5. entrenar RandomForestClassifier con n_estimators=100;
6. calcular accuracy;
7. guardar model.pkl;
8. guardar metrics.json;
9. crear una versión v1;
10. registrar parámetros, métricas y modelo en MLflow;
11. cambiar n_estimators de 100 a 200;
12. repetir el proceso, comparar v1 y v2 y justificar cuál versión se conservaría.

Este repositorio conserva ese objetivo y agrega algunos elementos para que la práctica sea completamente ejecutable:

- data/churn.csv sintético y reproducible, ya que el PDF especifica el archivo pero no incluye sus datos;
- metadata.json para trazabilidad;
- compare_versions.py para comparar versiones;
- promote.py para documentar la versión seleccionada;
- protección contra sobrescribir una versión existente por accidente;
- instrucciones separadas para Windows y macOS/Linux.

La estructura de la práctica es:

~~~text
tema17_versionado_artefactos_mlflow/
├── data/
│   └── churn.csv
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── compare_versions.py
│   └── promote.py
├── models/
│   └── README.md
├── requirements.txt
├── demo.ps1
├── demo.sh
└── README.md
~~~

---

# 1. Requisitos previos

Necesitas:

- Python 3.8 o superior;
- Git;
- Visual Studio Code;
- terminal;
- conexión a Internet para instalar dependencias la primera vez.

Las bibliotecas se instalarán desde requirements.txt:

~~~text
pandas
scikit-learn
mlflow
joblib
~~~

## Windows

Abre PowerShell:

~~~powershell
python --version
git --version
code --version
~~~

## macOS / Linux

~~~bash
python3 --version
git --version
code --version
~~~

Si el comando code no funciona, abre VS Code manualmente.

---

# 2. Clonar el repositorio

## Primera vez - Windows

~~~powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
~~~

## Primera vez - macOS / Linux

~~~bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab
~~~

Si no existe la carpeta Documents en tu sistema, utiliza otra carpeta de trabajo.

## ¿Qué estamos haciendo?

git clone crea una copia local del repositorio:

~~~text
GitHub
  ↓ git clone
tu computadora
~~~

A partir de ahí tienes el historial del proyecto y todos los archivos necesarios.

---

# 3. Si ya habías clonado el repositorio

No vuelvas a ejecutar git clone.

## Windows

~~~powershell
cd $HOME\Documents\tema12-mlflow-colab
~~~

## macOS / Linux

~~~bash
cd ~/Documents/tema12-mlflow-colab
~~~

Revisa primero:

~~~bash
git status
git status --short
~~~

Si aparece:

~~~text
nothing to commit, working tree clean
~~~

actualiza:

~~~bash
git switch main
git pull origin main
~~~

## Si aparecen archivos modificados

Antes de hacer pull:

~~~bash
git diff
~~~

¿Por qué? Porque primero debes saber qué cambiaste localmente antes de mezclar esos cambios con una actualización remota.

---

# 4. Entrar a la práctica y abrir VS Code

Desde la raíz del repositorio.

## Windows

~~~powershell
cd .\demostraciones_t17_t18\tema17_versionado_artefactos_mlflow
dir
code .
~~~

## macOS / Linux

~~~bash
cd demostraciones_t17_t18/tema17_versionado_artefactos_mlflow
ls -la
code .
~~~

En el explorador de VS Code identifica data, src y models.

## ¿Por qué separar carpetas?

~~~text
data/   → datos
src/    → código
models/ → artefactos y versiones
~~~

Separar responsabilidades facilita reproducibilidad, mantenimiento y auditoría.

---

# 5. Crear un entorno virtual

## Windows

En la terminal integrada de VS Code:

~~~powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
~~~

## macOS / Linux

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

Debe aparecer:

~~~text
(.venv)
~~~

al inicio de la terminal.

## ¿Para qué sirve?

El entorno virtual aísla las dependencias de esta práctica del resto de tu computadora.

---

# 6. Instalar dependencias

## Windows

~~~powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
~~~

## macOS / Linux

~~~bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
~~~

Comprueba:

~~~bash
python -c "import pandas, sklearn, mlflow, joblib; print('Dependencias OK')"
~~~

Si en macOS/Linux python no funciona después de activar el entorno, utiliza python3.

---

# 7. Visualizar churn.csv

En VS Code abre:

~~~text
data/churn.csv
~~~

Las variables son:

~~~text
tenure_months
monthly_charges
support_calls
contract_months
auto_pay
churn
~~~

churn es la variable objetivo:

~~~text
0 = no churn
1 = churn
~~~

## ¿Por qué revisar los datos antes de entrenar?

Un pipeline no debería asumir que cualquier archivo recibido tiene la estructura correcta.

Primero verificamos la entrada; después entrenamos.

---

# 8. Validar datos

## Windows

~~~powershell
python src\preprocess.py
~~~

## macOS / Linux

~~~bash
python src/preprocess.py
~~~

El script muestra:

- primeras filas;
- valores nulos;
- tipos de datos;
- número de registros;
- variables de entrada;
- distribución de churn.

## ¿Para qué?

El PDF solicita revisar valores nulos y tipos de datos. Esta etapa representa una validación básica antes del entrenamiento.

---

# 9. Crear v1

La primera versión utiliza:

~~~text
RandomForestClassifier
n_estimators = 100
~~~

## Windows

~~~powershell
python src\train.py --version v1 --n-estimators 100
~~~

## macOS / Linux

~~~bash
python src/train.py --version v1 --n-estimators 100
~~~

El script realiza:

~~~text
churn.csv
  ↓
validación
  ↓
dropna()
  ↓
X / y
  ↓
train_test_split 80/20
  ↓
Random Forest
  ↓
predicciones
  ↓
accuracy
  ↓
artefactos + MLflow
~~~

---

# 10. Revisar los artefactos de v1

En VS Code abre:

~~~text
models/v1/
~~~

Debes encontrar:

~~~text
model.pkl
metrics.json
metadata.json
~~~

## model.pkl

Es el modelo entrenado serializado con Joblib.

## metrics.json

Guarda la métrica y la configuración principal de esa versión.

## metadata.json

Agrega información de trazabilidad: variables, número de registros, fecha, semilla y run ID de MLflow.

## ¿Por qué model.pkl no es suficiente?

Porque por sí solo no responde:

~~~text
¿qué versión es?
¿qué configuración usó?
¿qué resultado obtuvo?
¿de qué experimento proviene?
~~~

Un artefacto útil necesita contexto.

---

# 11. Abrir MLflow

Ejecuta:

~~~bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
~~~

Abre:

~~~text
http://localhost:5000
~~~

Busca el experimento:

~~~text
Tema17_Versionado_Artefactos
~~~

Dentro de v1 identifica:

~~~text
Parameters
  version = v1
  n_estimators = 100
  random_state = 42

Metrics
  accuracy = ...

Artifacts
  model
  version_metadata
~~~

## ¿Por qué MLflow si ya tenemos models/v1?

~~~text
models/v1/
  → versión manual y visible

MLflow
  → tracking estructurado del experimento
~~~

Son formas complementarias de trazabilidad.

Detén MLflow con Ctrl + C cuando termines de revisarlo.

---

# 12. Evitar sobrescribir v1

Si vuelves a ejecutar:

~~~bash
python src/train.py --version v1 --n-estimators 100
~~~

el script debe detenerse porque v1 ya existe.

## ¿Por qué?

Sobrescribir silenciosamente una versión destruye la trazabilidad.

~~~text
v1 debe seguir representando v1
~~~

Existe la opción --overwrite, pero no la uses en esta práctica salvo que realmente quieras reemplazar deliberadamente una versión.

Lo correcto para experimentar es crear una versión nueva.

---

# 13. Crear v2

El laboratorio propone cambiar:

~~~text
n_estimators: 100 → 200
~~~

## Windows

~~~powershell
python src\train.py --version v2 --n-estimators 200
~~~

## macOS / Linux

~~~bash
python src/train.py --version v2 --n-estimators 200
~~~

Ahora deberías tener:

~~~text
models/
├── v1/
│   ├── model.pkl
│   ├── metrics.json
│   └── metadata.json
└── v2/
    ├── model.pkl
    ├── metrics.json
    └── metadata.json
~~~

## Concepto clave

**v2 no significa automáticamente mejor.**

Una nueva versión es una nueva candidata que debe evaluarse.

---

# 14. Comparar v1 y v2

## Windows

~~~powershell
python src\compare_versions.py
~~~

## macOS / Linux

~~~bash
python src/compare_versions.py
~~~

Verás una tabla semejante a:

~~~text
version  n_estimators  accuracy
v1       100           ...
v2       200           ...
~~~

Debes analizar:

- accuracy;
- diferencia real entre versiones;
- estabilidad;
- complejidad;
- costo computacional;
- contexto del proyecto.

Es posible que v1 y v2 obtengan el mismo accuracy. Eso también es un resultado válido.

---

# 15. Comparar runs en MLflow

Vuelve a iniciar:

~~~bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
~~~

Ahora deberían existir:

~~~text
v1_rf_100
v2_rf_200
~~~

Selecciona ambos runs y compáralos.

## ¿Qué permite ver MLflow?

~~~text
parámetros
vs.
métricas
vs.
artefactos
~~~

en un solo lugar.

---

# 16. Documentar qué versión seleccionarías

El PDF pide decidir qué versión pasaría a producción y justificarla.

El repositorio agrega promote.py para registrar esa decisión sin realizar un despliegue real.

Ejemplo si decides conservar v2:

## Windows

~~~powershell
python src\promote.py --version v2 --reason "Se selecciona como candidata después de comparar desempeño y configuración"
~~~

## macOS / Linux

~~~bash
python src/promote.py --version v2 --reason "Se selecciona como candidata después de comparar desempeño y configuración"
~~~

Se genera:

~~~text
models/production.json
~~~

Ábrelo en VS Code.

## Importante

production.json no despliega el modelo. Documenta:

~~~text
qué versión elegiste
+
por qué
+
qué métrica tenía
~~~

---

# 17. Si v2 no mejora

No estás obligado a promover v2.

Puedes mantener v1:

~~~bash
python src/promote.py --version v1 --reason "v2 no aporta una mejora suficiente para justificar el cambio"
~~~

**Actualizar por evidencia es más importante que actualizar por número de versión.**

---

# 18. Resultado esperado

La carpeta terminará aproximadamente así:

~~~text
tema17_versionado_artefactos_mlflow/
├── data/
│   └── churn.csv
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── compare_versions.py
│   └── promote.py
├── models/
│   ├── README.md
│   ├── v1/
│   │   ├── model.pkl
│   │   ├── metrics.json
│   │   └── metadata.json
│   ├── v2/
│   │   ├── model.pkl
│   │   ├── metrics.json
│   │   └── metadata.json
│   └── production.json
├── mlflow.db
├── requirements.txt
└── README.md
~~~

mlflow.db permanece local.

---

# 19. Git: versión del proyecto vs versión del modelo

No confundas:

~~~text
Git commit
  → versión del código/proyecto

models/v1
  → versión del artefacto de ML

models/v2
  → otra versión del artefacto
~~~

En este laboratorio los modelos son pequeños y se permite versionarlos con Git con fines didácticos.

En proyectos reales, modelos grandes o checkpoints de deep learning normalmente deben ir a un Model Registry o almacén de artefactos.

---

# 20. Revisar cambios antes del commit

Regresa a la raíz del repositorio.

## Windows

~~~powershell
cd $HOME\Documents\tema12-mlflow-colab
~~~

## macOS / Linux

~~~bash
cd ~/Documents/tema12-mlflow-colab
~~~

Ejecuta:

~~~bash
git status
git status --short
git diff
~~~

## ¿Por qué?

Antes de versionar debes saber exactamente qué estás agregando.

No uses git add . automáticamente sin revisar.

---

# 21. Agregar solamente la práctica

~~~bash
git add demostraciones_t17_t18/tema17_versionado_artefactos_mlflow
git status
~~~

No deberían agregarse:

~~~text
.venv/
mlflow.db
mlruns/
__pycache__/
~~~

---

# 22. Crear un commit

~~~bash
git commit -m "Completa laboratorio Tema 17 y compara versiones del modelo"
~~~

Un commit crea un punto trazable en el historial del proyecto.

---

# 23. Actualizar antes de subir

Si tienes permiso de escritura en el repositorio:

~~~bash
git pull --rebase origin main
~~~

¿Por qué?

Porque el repositorio remoto pudo haber cambiado mientras trabajabas.

Si aparece un conflicto, resuélvelo antes de continuar.

---

# 24. Subir cambios a GitHub

Solo si tienes permiso:

~~~bash
git push origin main
git status
~~~

Idealmente debe finalizar con:

~~~text
nothing to commit, working tree clean
~~~

## Estudiantes sin permiso de escritura

No deben intentar modificar el repositorio docente.

Pueden:

1. realizar la práctica localmente;
2. crear commits locales;
3. trasladar la estructura a su propio proyecto;
4. versionar allí sus modelos, métricas y documentación.

---

# 25. ¿Qué significa actualizar versión?

Hay dos acciones diferentes.

## Actualizar el repositorio

~~~bash
git pull origin main
~~~

trae cambios recientes de GitHub.

## Crear una nueva versión del modelo

Por ejemplo:

~~~bash
python src/train.py --version v3 --n-estimators 300
~~~

genera un nuevo artefacto.

Solo crea v3 si existe una razón:

- cambio de hiperparámetro;
- nuevos datos;
- nueva preparación;
- nuevo algoritmo;
- corrección de un error;
- cambio de criterio de negocio.

Después repite:

~~~text
entrenar
→ evaluar
→ registrar
→ comparar
→ decidir
~~~

---

# 26. Ejecución rápida para demostración

Una vez comprendido el proceso manual:

## Windows

~~~powershell
.\demo.ps1 validate
.\demo.ps1 v1
.\demo.ps1 v2
.\demo.ps1 compare
.\demo.ps1 ui
~~~

## macOS / Linux

~~~bash
bash demo.sh validate
bash demo.sh v1
bash demo.sh v2
bash demo.sh compare
bash demo.sh ui
~~~

Estos scripts son atajos. La finalidad del laboratorio es comprender qué hace cada etapa.

---

# 27. Preguntas de cierre

Al terminar debes poder responder:

1. ¿Qué es un artefacto de modelo?
2. ¿Por qué model.pkl necesita métricas y metadatos?
3. ¿Qué diferencia existe entre v1 y v2?
4. ¿Por qué una nueva versión no implica necesariamente una mejora?
5. ¿Qué información registra MLflow?
6. ¿Qué diferencia existe entre versionar código con Git y versionar modelos?
7. ¿Qué evidencia usarías para decidir qué modelo promover?
8. ¿Cuándo tendría sentido crear v3?
9. ¿Por qué no deberíamos sobrescribir silenciosamente v1?
10. ¿Qué archivos no deberían subirse a GitHub?

---

# Objetivo final

~~~text
Dataset
  ↓
preprocess.py
  ↓
train.py
  ↓
v1: 100 árboles
  ├── model.pkl
  ├── metrics.json
  ├── metadata.json
  └── MLflow run
  ↓
v2: 200 árboles
  ├── model.pkl
  ├── metrics.json
  ├── metadata.json
  └── MLflow run
  ↓
compare_versions.py
  ↓
decisión justificada
  ↓
production.json
  ↓
Git commit
~~~

El objetivo central del Tema 17 es pasar de:

**"tengo un modelo"**

a:

**"sé exactamente qué versión tengo, cómo fue generada, cómo rindió y por qué la conservaría o reemplazaría".**


---

# Continuación: Tema 18

En este laboratorio aprendiste a crear, comparar y seleccionar versiones de un modelo.

El siguiente paso es responder:

> **¿Qué ocurre cuando el modelo que seleccionamos comienza a perder desempeño?**

Continúa con:

- [Tema 18 - Reentrenamiento y despliegue automatizado](../tema18_reentrenamiento_despliegue_automatizado/README.md)

```text
T17
versionar y seleccionar
        ↓
T18
monitorear, activar trigger,
reentrenar, validar y promover
```
