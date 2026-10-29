from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import pandas as pd
app = FastAPI(
    title="API de clasificación de clientes",
    version="1.0"
)
artifact = joblib.load("model.pkl")
model = artifact["model"]
features = artifact["features"]
class ClienteInput(BaseModel):
    edad: int
    ingreso: float
    compras: int
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "features": features
    }

@app.post("/predict")
def predict(data: ClienteInput):
    entrada = pd.DataFrame(
        [[data.edad, data.ingreso, data.compras]],
        columns=features
 )
    pred = int(model.predict(entrada)[0])
    prob = float(model.predict_proba(entrada)[0, 1])
    return {
        "prediccion": pred,
        "probabilidad_clase_1": round(prob, 4)
    }
@app.get("/", response_class=HTMLResponse)
def frontend():
    return """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Demo IA</title>
        <style>
            body { font-family: Arial; max-width: 620px; margin: 40px auto; }
            input, button { padding: 10px; margin: 6px 0; width: 100%; }
            #resultado { margin-top: 18px; padding: 12px; background: #f3f6f9; }
        </style>
    </head>
    <body>
        <h2>Clasificación de clientes</h2>
        <label>Edad</label><input id="edad" type="number" value="48">
        <label>Ingreso</label><input id="ingreso" type="number" value="65887">
        <label>Compras</label><input id="compras" type="number" value="6">
        <button onclick="predecir()">Predecir</button>
        <div id="resultado">Sin predicción todavía.</div>
        <script>
        async function predecir() {
            const payload = {
                edad: Number(document.getElementById("edad").value),
                ingreso: Number(document.getElementById("ingreso").value),
                compras: Number(document.getElementById("compras").value)
            };
            const respuesta = await fetch("/predict", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
            const datos = await respuesta.json();
            document.getElementById("resultado").innerText =
                JSON.stringify(datos, null, 2);
        }
        </script>
    </body>
    </html>
"""