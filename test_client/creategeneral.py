import requests

# URL de l’API
url = 'http://127.0.0.1:8000/api/create/general/'

# En-têtes avec authentification
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # 'Content-Type': 'application/json'
}

# Données à envoyer (adaptées à ton modèle)
data = {
    "animal_id": "test001",
    "dob": "2025-05-01",
    "gender": "Male",
    "breed": "Race locale",
    "dam_no": "M001",
    "sire_no": "P001",
    "grand_dam": "GM001",
    "grand_sire": "GP001",
    "colitter_size_of_birth": 8,
    "color_and_marking": "Noir avec taches blanches",
    "abnormalities": "no"
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, json=data)

# Affichage du résultat
if response.status_code == 201:
    print("✅ Animal créé avec succès :", response.json())
else:
    print("❌ Erreur :", response.status_code, response.text)
