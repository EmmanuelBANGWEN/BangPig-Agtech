import requests

# L’animal_id à mettre à jour
animal_id = "test001"

# L’URL de l’API
url = f"http://127.0.0.1:8000/api/update/nutrition/{animal_id}"

# En-têtes avec le token d’authentification
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# Les données à mettre à jour (partial update)
data = {
    "remarks": "rassss ",

}

# Requête PUT
response = requests.put(url, headers=headers, json=data)

# Affichage de la réponse
print("Statut:", response.status_code)
print("Réponse:", response.json())
