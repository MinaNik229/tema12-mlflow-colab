from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "churn.csv"


def load_and_validate(path: Path = DATA_PATH) -> pd.DataFrame:
    """Carga el dataset y realiza las validaciones básicas del laboratorio."""
    data = pd.read_csv(path)

    print("\n=== Primeras filas ===")
    print(data.head())

    print("\n=== Valores nulos por columna ===")
    print(data.isnull().sum())

    print("\n=== Tipos de datos ===")
    print(data.dtypes)

    required = {
        "tenure_months",
        "monthly_charges",
        "support_calls",
        "contract_months",
        "auto_pay",
        "churn",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")

    return data


def prepare_xy(data: pd.DataFrame):
    """Replica la lógica del PDF: limpiar nulos y separar X / y."""
    clean = data.dropna().copy()
    X = clean.drop("churn", axis=1)
    y = clean["churn"]
    return X, y


if __name__ == "__main__":
    df = load_and_validate()
    X, y = prepare_xy(df)

    print("\n=== Resumen de preprocesamiento ===")
    print(f"Filas originales: {len(df)}")
    print(f"Filas después de dropna(): {len(X)}")
    print(f"Variables de entrada: {list(X.columns)}")
    print("Distribución de churn:")
    print(y.value_counts().sort_index())
