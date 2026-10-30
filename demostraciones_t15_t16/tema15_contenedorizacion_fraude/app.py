import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="API de detección de fraude", version="1.0")

with open("model.pkl", "rb") as f:
    artifact = pickle.load(f)

model = artifact["model"]
features = artifact["features"]

class Transaccion(BaseModel):
    monto: float = Field(gt=0)
    intentos_24h: int = Field(ge=0)
    es_extranjero: int = Field(ge=0, le=1)
    hora: int = Field(ge=0, le=23)

@app.get("/")
def home():
    return {"mensaje": "API de modelo de fraude funcionando"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True, "features": features}

@app.post("/predict")
def predict(data: Transaccion):
    entrada = pd.DataFrame([data.model_dump()], columns=features)
    prediction = int(model.predict(entrada)[0])
    probability = float(model.predict_proba(entrada)[0, 1])
    return {
        "prediccion": prediction,
        "riesgo": "Posible fraude" if prediction == 1 else "Riesgo bajo",
        "probabilidad_fraude": round(probability, 4),
    }
