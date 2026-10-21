import numpy as np
import pandas as pd


# ============================================================
# CONFIGURACIÓN
# ============================================================
# Usamos una semilla fija para que los mismos datos
# puedan generarse nuevamente.

rng = np.random.default_rng(42)

n = 200


# ============================================================
# CREAR VARIABLES
# ============================================================

edad = rng.integers(
    22,
    56,
    size=n
)

ingreso = rng.integers(
    25000,
    70001,
    size=n
)

compras = rng.integers(
    1,
    8,
    size=n
)


# ============================================================
# CREAR VARIABLE OBJETIVO
# ============================================================

target = (
    (ingreso > 45000)
    &
    (compras > 4)
).astype(int)


# ============================================================
# CREAR DATAFRAME
# ============================================================

df = pd.DataFrame({
    "edad": edad,
    "ingreso": ingreso,
    "compras": compras,
    "target": target
})


# ============================================================
# GUARDAR DATASET
# ============================================================

df.to_csv(
    "data.csv",
    index=False
)


print("\nPrimeras filas:")
print(df.head())

print(
    "\nNúmero de registros:",
    len(df)
)

print(
    "\nDistribución del target:"
)

print(
    df["target"].value_counts()
)