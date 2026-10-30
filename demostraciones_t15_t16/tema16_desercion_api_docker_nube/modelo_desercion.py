import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

data = {
    "edad": [18, 19, 20, 21, 22, 23, 24, 25],
    "promedio": [9, 8, 7, 6, 5, 6, 7, 5],
    "asistencia": [90, 85, 80, 70, 60, 65, 75, 50],
    "desercion": [0, 0, 0, 1, 1, 1, 0, 1],
}

df = pd.DataFrame(data)
X = df[["edad", "promedio", "asistencia"]]
y = df["desercion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

modelo = RandomForestClassifier(n_estimators=200, random_state=42)
modelo.fit(X_train, y_train)

accuracy = accuracy_score(y_test, modelo.predict(X_test))
joblib.dump({"model": modelo, "features": list(X.columns)}, "modelo_desercion.pkl")

print("Modelo de deserción entrenado")
print(f"Accuracy didáctica de prueba: {accuracy:.3f}")
print("Artefacto creado: modelo_desercion.pkl")
