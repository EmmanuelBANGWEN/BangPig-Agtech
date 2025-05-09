import requests

# URL de l'API
url = f"http://127.0.0.1:8000/api/report/selectpigs"

# Données envoyées à l’API (task = 1, 2, 3 ou 4 selon la logique métier)
data = {
    "task": "2",       # Exemple : "2" pour colitter_size_of_birth > amount
    "amount": 2        # Exemple de valeur pour le filtre
}

# Headers avec JWT ou Token si nécessaire
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# Requête POST
response = requests.post(url, json=data, headers=headers)

# Résultat
if response.status_code == 200:
    result = response.json()
    print("🐷 Mâles :", result["male"])
    print("👩 Femelles :", result["female"])
    print("Total mâles :", result["malelen"])
    print("Total femelles :", result["femalelen"])
else:
    print("Erreur:", response.status_code)
    print(response.text)
