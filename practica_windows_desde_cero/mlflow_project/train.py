import argparse

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# ============================================================
# 1. RECIBIR HIPERPARÁMETROS
# ============================================================

parser = argparse.ArgumentParser()

parser.add_argument(
    "--C",
    type=float,
    default=1.0,
    help="Inverso de la intensidad de regularización"
)

parser.add_argument(
    "--max_iter",
    type=int,
    default=200,
    help="Número máximo de iteraciones"
)

args = parser.parse_args()

C = args.C
max_iter = args.max_iter


# ============================================================
# 2. CONFIGURAR MLFLOW
# ============================================================

# La información de los experimentos se almacenará
# en una base SQLite llamada mlflow.db.

mlflow.set_tracking_uri(
    "sqlite:///mlflow.db"
)

mlflow.set_experiment(
    "Clasificacion_Clientes"
)


# ============================================================
# 3. CARGAR DATASET
# ============================================================

data = pd.read_csv(
    "data.csv"
)

X = data.drop(
    "target",
    axis=1
)

y = data["target"]


# ============================================================
# 4. DIVIDIR LOS DATOS
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 5. CREAR UN RUN EN MLFLOW
# ============================================================

with mlflow.start_run():

    # --------------------------------------------------------
    # Registrar parámetros
    # --------------------------------------------------------

    mlflow.log_param(
        "C",
        C
    )

    mlflow.log_param(
        "max_iter",
        max_iter
    )


    # --------------------------------------------------------
    # Crear el modelo
    # --------------------------------------------------------

    model = LogisticRegression(
        C=C,
        max_iter=max_iter
    )


    # --------------------------------------------------------
    # Entrenar
    # --------------------------------------------------------

    model.fit(
        X_train,
        y_train
    )


    # --------------------------------------------------------
    # Realizar predicciones
    # --------------------------------------------------------

    y_pred = model.predict(
        X_test
    )


    # --------------------------------------------------------
    # Calcular accuracy
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )


    # --------------------------------------------------------
    # Registrar métrica
    # --------------------------------------------------------

    mlflow.log_metric(
        "accuracy",
        accuracy
    )


    # --------------------------------------------------------
    # Registrar modelo
    # --------------------------------------------------------

    mlflow.sklearn.log_model(
        sk_model=model,
        name="modelo"
    )


    # --------------------------------------------------------
    # Mostrar resultado
    # --------------------------------------------------------

    print(
        "================================"
    )

    print(
        "C:",
        C
    )

    print(
        "max_iter:",
        max_iter
    )

    print(
        "Accuracy:",
        accuracy
    )

    print(
        "================================"
    )