import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="API de predicción de deserción", version="1.0")

artifact = joblib.load("modelo_desercion.pkl")
modelo = artifact["model"]
features = artifact["features"]

@app.get("/")
def home():
    return {"mensaje": "API de predicción de deserción activa"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True, "features": features}

@app.post("/predict")
def predict(edad: int, promedio: float, asistencia: float):
    datos = pd.DataFrame([[edad, promedio, asistencia]], columns=features)
    prediccion = int(modelo.predict(datos)[0])
    probabilidad = float(modelo.predict_proba(datos)[0, 1])
    riesgo = "Alto riesgo de deserción" if prediccion == 1 else "Bajo riesgo"
    return {
        "prediccion": prediccion,
        "riesgo": riesgo,
        "probabilidad_desercion": round(probabilidad, 4),
    }
