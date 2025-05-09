import requests

# URL de l'API
url = f"http://127.0.0.1:8000/api/report/pigletweaned"

# Données du formulaire (dates au format YYYY-MM-DD)
data = {
    "from_date": "2024-01-01",
    "to_date": "2025-12-31"
}

# Authentification (exemple avec token JWT)
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# Requête POST
response = requests.post(url, json=data, headers=headers)

# Affichage de la réponse
if response.status_code == 200:
    result = response.json()
    print("Total:", result["totalcount"])
    print("Mâles:", result["malecount"])
    print("Femelles:", result["femalecount"])
    print("Graph HTML 1:", result["graph_json"][:500], "...")  # tronqué
    print("Graph HTML 2:", result["graph_json2"][:500], "...")
else:
    print("Erreur:", response.status_code)
    print(response.text)
