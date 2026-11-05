# Tema 18 - Reentrenamiento y despliegue automatizado

Esta práctica es una demostración **sencilla, local y reproducible** de los conceptos del Tema 18.

No vamos a desplegar un sistema real en nube ni a usar Kubernetes o Airflow. Vamos a **simular el ciclo MLOps completo** en una sola computadora para entender qué ocurre entre monitoreo, trigger, reentrenamiento, staging y promoción de una nueva versión.

El objetivo es pasar de:

```text
"ya desplegué un modelo"
```

a:

```text
"sé cómo detectar que se degradó,
cuándo reentrenarlo,
cómo probar la nueva versión
y cuándo promoverla"
```

---

# Flujo de la demostración

```text
Datos históricos
     ↓
Entrenamiento inicial
     ↓
MLflow Model Registry
     ↓
champion
     ↓
llega un lote nuevo
     ↓
monitoreo RMSE
     ↓
¿RMSE > umbral?
   /          \
 NO           SÍ
 ↓             ↓
conservar    TRIGGER
champion       ↓
           reentrenar
               ↓
           challenger
               ↓
             staging
               ↓
        pruebas automáticas
               ↓
        ¿cumple criterios?
          /          \
        NO            SÍ
        ↓              ↓
     rechazo       promoción
                       ↓
                 nuevo champion
```

---

# 0. ¿Qué conceptos del Tema 18 estamos representando?

La demostración traduce a código una versión simplificada de los conceptos del material:

1. entrenamiento y registro con MLflow;
2. Model Registry;
3. aliases como `champion` y `challenger`;
4. monitoreo de una métrica;
5. trigger de reentrenamiento;
6. reentrenamiento automático;
7. ambiente de staging simulado;
8. pruebas automáticas;
9. promoción o rechazo del nuevo modelo;
10. trazabilidad del proceso.

## Importante

En esta práctica:

- **staging es simulado localmente**;
- **producción se representa mediante el alias `champion`**;
- no hay usuarios reales;
- no hay infraestructura cloud;
- no hay un despliegue real de producción.

Esto se hace así para que primero comprendas la lógica del ciclo antes de añadir infraestructura.

---

# 1. ¿Qué problema vamos a simular?

Utilizaremos un problema de **regresión** con `RandomForestRegressor`.

La métrica será:

```text
RMSE
Root Mean Squared Error
```

En RMSE:

```text
menor = mejor
```

El modelo inicial se entrenará con datos históricos.

Después aparecerá un lote nuevo en el que cambia deliberadamente la distribución y la relación entre variables.

Esto simulará un entorno donde:

```text
el mundo cambió
      ↓
el champion ya no responde igual
      ↓
su error aumenta
```

---

# 2. Resultado esperado de esta demostración

Con los datos sintéticos incluidos en el generador, los valores esperados son aproximadamente:

```text
Champion - RMSE de prueba inicial: ≈ 1.34

Champion sobre lote nuevo:
RMSE ≈ 8.2

Umbral del trigger:
RMSE > 4.0

Resultado:
TRIGGER ACTIVADO
```

Después del reentrenamiento:

```text
Champion anterior en staging:  ≈ 8.7
Challenger en staging:         ≈ 2.6
```

Por lo tanto, en la ejecución normal de la demostración, el challenger debería pasar staging y convertirse en el nuevo `champion`.

Los valores pueden variar ligeramente según versiones de bibliotecas, pero la decisión general está diseñada para ser reproducible.

---

# 3. Estructura de la práctica

```text
tema18_reentrenamiento_despliegue_automatizado/
├── data/
│   ├── README.md
│   └── generate_data.py
│
├── src/
│   ├── common.py
│   ├── bootstrap.py
│   ├── monitor.py
│   ├── retrain.py
│   ├── staging_validate.py
│   ├── promote.py
│   ├── pipeline.py
│   └── reset_demo.py
│
├── tests/
│   └── test_data_contract.py
│
├── reports/
│   └── README.md
│
├── requirements.txt
├── demo.ps1
├── demo.sh
└── README.md
```

---

# 4. Primera vez: clonar el repositorio

## Windows / PowerShell

```powershell
cd $HOME\Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd .\tema12-mlflow-colab
```

## macOS / Linux

```bash
cd ~/Documents
git clone https://github.com/MinaNik229/tema12-mlflow-colab.git
cd tema12-mlflow-colab
```

## ¿Qué estamos haciendo?

`git clone` crea una copia local del proyecto.

```text
GitHub
  ↓
git clone
  ↓
computadora del alumno
```

No estamos descargando solamente archivos: estamos obteniendo también el historial Git del proyecto.

---

# 5. Si ya tienes el repositorio

No vuelvas a ejecutar `git clone`.

## Windows

```powershell
cd $HOME\Documents\tema12-mlflow-colab
```

## macOS / Linux

```bash
cd ~/Documents/tema12-mlflow-colab
```

Primero revisa:

```bash
git status
git status --short
```

Si aparece:

```text
nothing to commit, working tree clean
```

entonces:

```bash
git switch main
git pull origin main
```

## ¿Por qué revisar antes de hacer pull?

Porque si tú modificaste archivos localmente, primero debes saber qué cambió antes de integrar nuevos cambios remotos.

---

# 6. Entrar al Tema 18 y abrir Visual Studio Code

## Windows

```powershell
cd .\demostraciones_t17_t18\tema18_reentrenamiento_despliegue_automatizado
dir
code .
```

## macOS / Linux

```bash
cd demostraciones_t17_t18/tema18_reentrenamiento_despliegue_automatizado
ls -la
code .
```

## ¿Qué revisar en VS Code?

Ubica:

```text
data/
src/
tests/
reports/
requirements.txt
```

La intención es que puedas seguir visualmente cómo cada carpeta corresponde a una etapa del flujo MLOps.

---

# 7. Crear un entorno virtual

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

Debe aparecer:

```text
(.venv)
```

## ¿Por qué?

Porque queremos que las dependencias de esta práctica estén aisladas.

Esto mejora la reproducibilidad:

```text
computadora
  ↓
.venv
  ↓
versiones de bibliotecas del proyecto
```

---

# 8. Instalar dependencias

## Windows

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## macOS / Linux

Con el entorno activo:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se instalarán:

- MLflow;
- pandas;
- NumPy;
- scikit-learn;
- pytest.

Comprueba:

```bash
python -c "import mlflow, pandas, sklearn, numpy, pytest; print('Dependencias OK')"
```

---

# 9. Reiniciar la demostración si ya la ejecutaste antes

La primera vez puedes omitir este paso.

Si quieres repetir la demostración desde cero:

## Windows

```powershell
python src\reset_demo.py
```

## macOS / Linux

```bash
python src/reset_demo.py
```

## ¿Qué elimina?

Solo artefactos generados por la demostración:

- `mlflow.db`;
- datos sintéticos generados;
- reportes;
- artefactos locales de MLflow.

No elimina el código ni el README.

---

# 10. Generar los datos

## Windows

```powershell
python data\generate_data.py
```

## macOS / Linux

```bash
python data/generate_data.py
```

Se crean:

```text
data/train.csv
data/production_batch.csv
```

## ¿Qué representa cada uno?

### train.csv

Representa los datos históricos con los que se creó el modelo original.

### production_batch.csv

Representa datos que llegan posteriormente.

En ese lote introdujimos un cambio deliberado.

## ¿Por qué hacemos esto?

Porque necesitamos observar una situación como:

```text
modelo funcionaba bien
      ↓
cambian los datos / entorno
      ↓
modelo pierde desempeño
```

Eso es lo que justifica el monitoreo y los triggers.

---

# 11. Ejecutar pruebas básicas de datos

```bash
python -m pytest -q
```

Deberías ver:

```text
2 passed
```

## ¿Qué estamos probando?

Las pruebas comprueban que:

- existen los datasets;
- las columnas esperadas están presentes;
- no hay valores nulos;
- existe una cantidad mínima de registros.

## ¿Por qué antes del entrenamiento?

Porque automatizar un pipeline no significa entrenar ciegamente.

Primero debemos validar la entrada.

---

# 12. Crear el champion inicial

## Windows

```powershell
python src\bootstrap.py
```

## macOS / Linux

```bash
python src/bootstrap.py
```

Este script:

1. carga `train.csv`;
2. separa entrenamiento y prueba;
3. entrena un `RandomForestRegressor`;
4. calcula RMSE;
5. registra parámetros y métricas en MLflow;
6. registra el modelo en el Model Registry;
7. asigna el alias `champion`.

El modelo usa:

```text
n_estimators = 150
max_depth = 5
```

---

# 13. ¿Qué significa champion?

`champion` es un alias.

No es otra copia física del modelo.

Es una referencia flexible:

```text
champion
   ↓
versión 1
```

Más adelante podemos mover ese alias:

```text
champion
   ↓
versión 2
```

sin cambiar el código que busca al `champion`.

---

# 14. Abrir MLflow

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
Tema18_Reentrenamiento_Automatizado
```

y el modelo registrado:

```text
Tema18_RandomForest_RMSE
```

Debes poder identificar:

- parámetros;
- RMSE;
- versión del modelo;
- alias `champion`;
- artefacto del modelo.

Detén MLflow con:

```text
Ctrl + C
```

---

# 15. Monitorear el champion

Ahora simularemos que el modelo está operando y recibimos un lote nuevo.

## Windows

```powershell
python src\monitor.py
```

## macOS / Linux

```bash
python src/monitor.py
```

Deberías observar algo semejante a:

```text
RMSE observado: ≈ 8.2
Umbral:         4.0
Trigger:        SÍ
Decisión:       RETRAIN
```

---

# 16. ¿Qué es el trigger?

El trigger es una condición que decide si debe iniciarse una acción.

En esta práctica:

```text
SI RMSE > 4.0
ENTONCES reentrenar
```

Conceptualmente:

```text
monitoreo
   ↓
métrica
   ↓
comparación con umbral
   ↓
condición
   ↓
trigger
```

## Importante

El umbral 4.0 es **didáctico**.

En un proyecto real debe justificarse con:

- desempeño histórico;
- impacto de negocio;
- riesgo;
- tolerancia al error;
- métricas de validación;
- costo del reentrenamiento.

---

# 17. Reentrenar manualmente para entender el proceso

Antes de automatizarlo, ejecutaremos cada etapa.

## Windows

```powershell
python src\retrain.py
```

## macOS / Linux

```bash
python src/retrain.py
```

El script:

1. toma los datos históricos;
2. incorpora parte del lote nuevo;
3. reserva una parte para staging;
4. entrena una nueva configuración;
5. registra el nuevo modelo;
6. le asigna el alias `challenger`.

El challenger utiliza:

```text
n_estimators = 250
max_depth = 8
```

---

# 18. ¿Qué significa challenger?

Ahora el Model Registry representa:

```text
champion
   ↓
modelo actualmente aceptado

challenger
   ↓
modelo nuevo que intenta reemplazarlo
```

Todavía **no hemos promovido** al challenger.

Primero debe pasar staging.

---

# 19. ¿Qué estamos llamando staging?

En un sistema real, staging sería un ambiente separado y controlado.

Aquí lo simulamos mediante:

```text
reports/staging_batch.csv
```

y un conjunto de pruebas.

Esto permite explicar la idea:

```text
desarrollo
   ↓
candidato
   ↓
STAGING
   ↓
pruebas
   ↓
producción
```

sin necesitar infraestructura externa.

---

# 20. Ejecutar validación de staging

## Windows

```powershell
python src\staging_validate.py
```

## macOS / Linux

```bash
python src/staging_validate.py
```

La validación comprueba:

### 1. Smoke test

¿El modelo logra generar predicciones?

### 2. Predicciones válidas

¿Las salidas son números finitos?

### 3. Umbral de calidad

```text
challenger RMSE <= 4.0
```

### 4. Mejora mínima

```text
champion RMSE - challenger RMSE >= 0.20
```

---

# 21. Resultado esperado en staging

Deberías observar aproximadamente:

```text
Champion RMSE:   ≈ 8.7
Challenger RMSE: ≈ 2.6
Mejora:          ≈ 6.0

Smoke test:      PASS
Predicciones:    PASS
Calidad:         PASS
Mejora mínima:   PASS

Decisión:        PROMOTE
```

## ¿Por qué no promovemos solamente porque el challenger es nuevo?

Porque:

```text
nuevo ≠ mejor
```

Primero debe demostrar que cumple criterios.

---

# 22. Promover el challenger

Si staging indicó `PROMOTE`:

## Windows

```powershell
python src\promote.py
```

## macOS / Linux

```bash
python src/promote.py
```

El script mueve los aliases.

Antes:

```text
champion   → versión 1
challenger → versión 2
```

Después:

```text
previous_champion → versión 1
champion          → versión 2
challenger        → versión 2
```

## ¿Qué significa esto?

Estamos simulando la promoción del nuevo modelo.

No estamos haciendo un deploy real a usuarios.

Estamos actualizando la referencia de qué versión consideramos aprobada.

---

# 22A. Revisar aliases desde la terminal

También puedes comprobar rápidamente qué versión apunta a cada alias.

## Windows

```powershell
python src\status.py
```

## macOS / Linux

```bash
python src/status.py
```

Verás algo semejante a:

```text
champion           -> versión 2
challenger         -> versión 2
previous_champion  -> versión 1
```

Esto ayuda a visualizar que un alias es una referencia móvil a una versión registrada.

---

# 23. Revisar el resultado en MLflow

Vuelve a iniciar:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Revisa el modelo:

```text
Tema18_RandomForest_RMSE
```

Ahora deberías observar varias versiones y aliases.

Esta es una de las ideas centrales del Model Registry:

```text
múltiples versiones
+
metadatos
+
aliases
+
trazabilidad
```

---

# 24. Automatizar el flujo completo

Hasta ahora ejecutamos manualmente:

```text
monitor
↓
retrain
↓
staging
↓
promote
```

Ahora vamos a dejar que un pipeline tome las decisiones.

Para repetirlo limpiamente:

## Windows

```powershell
python src\reset_demo.py
python data\generate_data.py
python src\bootstrap.py
python src\pipeline.py
```

## macOS / Linux

```bash
python src/reset_demo.py
python data/generate_data.py
python src/bootstrap.py
python src/pipeline.py
```

---

# 25. ¿Qué hace pipeline.py?

```text
1. pytest
   ↓
2. monitorea champion
   ↓
3. compara RMSE con umbral
   ↓
4. si NO supera → termina
   ↓
5. si SÍ supera → retraining
   ↓
6. registra challenger
   ↓
7. staging
   ↓
8. pruebas
   ↓
9. si pasa → promote
   ↓
10. si falla → conserva champion
```

Esta es la parte de la práctica que representa una **automatización local del pipeline**.

En un entorno real, un orquestador o un pipeline CI/CD podría ejecutar esta lógica.

---

# 26. ¿Dónde aparece CI/CD en esta demostración?

No estamos creando un pipeline cloud real.

Estamos simulando la lógica que CI/CD automatizaría:

```text
cambio / evento
  ↓
pruebas
  ↓
pipeline
  ↓
modelo candidato
  ↓
staging
  ↓
validación
  ↓
promoción/rechazo
```

El archivo:

```text
src/pipeline.py
```

representa esa secuencia.

Más adelante podría ser ejecutado por:

- GitHub Actions;
- GitLab CI;
- Airflow;
- Prefect;
- Kubeflow;
- otra plataforma de automatización.

---

# 27. ¿Qué tipo de trigger usamos?

El material distingue distintos tipos de triggers.

Esta práctica implementa uno **basado en desempeño**:

```text
RMSE > 4.0
```

Otros proyectos podrían usar:

### Trigger por datos

```text
data drift > umbral
```

### Trigger temporal

```text
reentrenar cada mes
```

### Trigger por evento

```text
llegó una nueva fuente de datos
```

### Trigger por desempeño

```text
F1 < 0.80
Accuracy < 0.85
RMSE > 4.0
```

No todos los proyectos deben usar el mismo trigger.

---

# 28. Archivos de evidencia generados

Durante la ejecución se crean archivos en:

```text
reports/
```

como:

```text
bootstrap.json
monitor.json
retrain.json
staging_batch.csv
staging_report.json
promotion.json
```

## ¿Para qué sirven?

Permiten ver qué ocurrió en cada etapa.

Por ejemplo, `staging_report.json` documenta:

- RMSE champion;
- RMSE challenger;
- mejora;
- pruebas;
- decisión PROMOTE/REJECT.

Estos reportes están ignorados por Git porque son resultados locales de ejecución.

---

# 29. Atajos para demostración docente

Una vez que comprendas el flujo manual, puedes utilizar los scripts auxiliares.

## Windows

```powershell
.\demo.ps1 reset
.\demo.ps1 data
.\demo.ps1 bootstrap
.\demo.ps1 monitor
.\demo.ps1 retrain
.\demo.ps1 staging
.\demo.ps1 promote
.\demo.ps1 status
.\demo.ps1 ui
```

Para el pipeline automático:

```powershell
.\demo.ps1 pipeline
```

## macOS / Linux

```bash
bash demo.sh reset
bash demo.sh data
bash demo.sh bootstrap
bash demo.sh monitor
bash demo.sh retrain
bash demo.sh staging
bash demo.sh promote
bash demo.sh status
bash demo.sh ui
```

Pipeline automático:

```bash
bash demo.sh pipeline
```

---

# 30. Si quiero repetir la demostración completa

## Windows

```powershell
.\demo.ps1 reset
.\demo.ps1 data
.\demo.ps1 bootstrap
.\demo.ps1 pipeline
```

## macOS / Linux

```bash
bash demo.sh reset
bash demo.sh data
bash demo.sh bootstrap
bash demo.sh pipeline
```

Después:

```bash
bash demo.sh ui
```

o en Windows:

```powershell
.\demo.ps1 ui
```

---

# 31. ¿Qué ocurre si el trigger NO se activa?

El pipeline termina sin reentrenar.

```text
RMSE <= umbral
      ↓
NO RETRAIN
      ↓
se conserva champion
```

Esto es importante.

Automatización no significa:

```text
reentrenar siempre
```

Significa:

```text
reentrenar cuando una condición justificada lo requiere
```

---

# 32. ¿Qué ocurre si el challenger falla staging?

El pipeline NO mueve el alias champion.

```text
challenger
   ↓
staging
   ↓
FAIL
   ↓
REJECT
   ↓
champion permanece
```

Esto es una compuerta de calidad.

---

# 33. Buenas prácticas que representa esta actividad

1. No reentrenar sin una razón.
2. Definir un trigger medible.
3. Registrar cada modelo.
4. Mantener un champion conocido.
5. Crear un challenger antes de reemplazarlo.
6. Probar antes de promover.
7. Documentar la decisión.
8. Conservar trazabilidad.
9. Separar monitoreo, reentrenamiento y promoción.
10. Automatizar solamente después de entender el proceso manual.

---

# 34. Relación con deep learning

El flujo conceptual sería el mismo con una red neuronal:

```text
checkpoint champion
      ↓
monitoreo
      ↓
trigger
      ↓
reentrenamiento / fine-tuning
      ↓
checkpoint challenger
      ↓
staging
      ↓
pruebas
      ↓
promoción
```

Cambiarían aspectos como:

- GPU;
- tiempo de entrenamiento;
- checkpoints `.pt`, `.pth`, `.keras`;
- memoria;
- latencia;
- costo computacional.

Pero el ciclo MLOps se conserva.

---

# 35. Actualizar Git al finalizar

Los archivos generados localmente están ignorados.

Lo que normalmente versionarías son cambios deliberados en:

- código;
- configuración;
- documentación;
- tests.

Regresa a la raíz.

## Windows

```powershell
cd $HOME\Documents\tema12-mlflow-colab
```

## macOS / Linux

```bash
cd ~/Documents/tema12-mlflow-colab
```

Revisa:

```bash
git status
git status --short
git diff
```

---

# 36. Si modificaste la práctica y quieres conservar los cambios

Agrega solamente la carpeta del Tema 18:

```bash
git add demostraciones_t17_t18/tema18_reentrenamiento_despliegue_automatizado
git status
```

Después:

```bash
git commit -m "Actualiza demostracion Tema 18"
```

Antes de enviar:

```bash
git pull --rebase origin main
```

Y si tienes permisos:

```bash
git push origin main
```

Los alumnos sin permisos sobre el repositorio docente deben trasladar la lógica a su propio repositorio.

---

# 37. Preguntas de cierre

Al terminar deberías poder responder:

1. ¿Qué diferencia hay entre champion y challenger?
2. ¿Qué función tiene un trigger?
3. ¿Por qué no debemos reentrenar en cada ejecución?
4. ¿Qué significa staging?
5. ¿Qué pruebas debería pasar un modelo candidato?
6. ¿Por qué una versión nueva no debe promoverse automáticamente?
7. ¿Qué registra MLflow?
8. ¿Qué representa el Model Registry?
9. ¿Qué parte de esta práctica simula CI/CD?
10. ¿Qué cambiarías para adaptar el flujo a tu proyecto?

---

# Resumen final

```text
PRODUCCIÓN SIMULADA
champion
   ↓
MONITOREO
RMSE
   ↓
TRIGGER
RMSE > 4.0
   ↓
REENTRENAMIENTO
   ↓
MLFLOW
nueva versión
   ↓
challenger
   ↓
STAGING
   ↓
PRUEBAS
   ↓
PROMOTE / REJECT
   ↓
nuevo champion o se conserva el anterior
```

El objetivo del Tema 18 no es simplemente volver a entrenar un modelo.

El objetivo es comprender cómo construir un ciclo **controlado, reproducible y trazable** para decidir **cuándo actualizarlo y cuándo no**.
