import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)
n = 800

data = pd.DataFrame({
    "monto": rng.uniform(50, 20000, n).round(2),
    "intentos_24h": rng.integers(1, 8, n),
    "es_extranjero": rng.integers(0, 2, n),
    "hora": rng.integers(0, 24, n),
})

score = (
    2 * (data["monto"] > 12000).astype(int)
    + 2 * (data["intentos_24h"] >= 5).astype(int)
    + data["es_extranjero"].astype(int)
    + ((data["hora"] <= 5) | (data["hora"] >= 23)).astype(int)
)
noise = rng.random(n) < 0.05
fraude = (score >= 3).astype(int)
fraude = np.where(noise, 1 - fraude, fraude)
data["fraude"] = fraude

features = ["monto", "intentos_24h", "es_extranjero", "hora"]
X = data[features]
y = data["fraude"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
)

model = LogisticRegression(max_iter=500, class_weight="balanced", random_state=RANDOM_STATE)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
artifact = {"model": model, "features": features}

with open("model.pkl", "wb") as f:
    pickle.dump(artifact, f)

print("Modelo de fraude entrenado")
print(f"Accuracy de prueba: {accuracy:.3f}")
print("Artefacto creado: model.pkl")
