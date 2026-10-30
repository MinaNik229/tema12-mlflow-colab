import requests

url = "http://127.0.0.1:8000/predict"
payload = {
    "monto": 18000,
    "intentos_24h": 6,
    "es_extranjero": 1,
    "hora": 2,
}

response = requests.post(url, json=payload, timeout=10)
print("HTTP:", response.status_code)
print(response.json())
