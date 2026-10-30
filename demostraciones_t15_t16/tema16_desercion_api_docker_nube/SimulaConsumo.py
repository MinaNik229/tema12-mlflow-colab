import requests

url = "http://127.0.0.1:8000/predict"
params = {
    "edad": 21,
    "promedio": 6,
    "asistencia": 65,
}

response = requests.post(url, params=params, timeout=10)
print("HTTP:", response.status_code)
print(response.json())
