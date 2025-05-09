import requests

# ID de l’animal concerné (doit exister dans la base de données)
animal_id = 'test001'

# URL de l’endpoint
url = f'http://127.0.0.1:8000/api/create/disposal/{animal_id}'

# En-têtes HTTP avec autorisation
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # 'Content-Type': 'application/json'
}

# Données à envoyer dans la requête POST
data = {
    "reason": "disosaltest",
    "sale_date": "2024-05-01",
    "weight_sale": "31",
    "revenue": "202422",
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, json=data)

# Affichage du résultat
if response.status_code == 201:
    print("✅ Diposal (Revenu generé) enregistrée :", response.json())
else:
    print("❌ Erreur :", response.status_code, response.text)
