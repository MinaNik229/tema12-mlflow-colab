import pickle
import pandas as pd

with open("model.pkl", "rb") as f:
    artifact = pickle.load(f)

model = artifact["model"]
features = artifact["features"]

casos = pd.DataFrame([
    {"monto": 18000, "intentos_24h": 6, "es_extranjero": 1, "hora": 2},
    {"monto": 800, "intentos_24h": 1, "es_extranjero": 0, "hora": 15},
    {"monto": 14000, "intentos_24h": 5, "es_extranjero": 0, "hora": 14},
], columns=features)

pred = model.predict(casos)
prob = model.predict_proba(casos)[:, 1]

resultado = casos.copy()
resultado["prediccion_fraude"] = pred
resultado["probabilidad_fraude"] = prob.round(4)
print(resultado.to_string(index=False))
