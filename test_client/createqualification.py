import requests

# ID de l’animal concerné (doit exister dans la base de données)
animal_id = 'test001'  

# URL de l’endpoint (à adapter à ton routeur DRF)
url = f'http://127.0.0.1:8000/api/create/qualification/{animal_id}'  # note le "/" à la fin si requis

# En-têtes HTTP avec le token JWT
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # 'Content-Type': 'application/json'
}

# Données POST valides
data = {
    "physical_fitness": "Very Good",
    "date_of_training": "2024-05-01",
    "period_of_training": 30,
    "training_score": "Excellent",
    "seminal_characteristics": "Good",
    "suitability": "yes"
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, json=data)

# Résultat
if response.status_code == 201:
    print("✅ Qualification enregistrée :", response.json())
else:
    print("❌ Erreur :", response.status_code, response.text)
