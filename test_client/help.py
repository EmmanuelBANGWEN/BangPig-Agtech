import requests

#  URL de l'API (à adapter à ton projet local ou déployé)
url = f"http://127.0.0.1:8000/api/help/"

#  En-têtes avec le token d'authentification (ex: Token ou JWT)
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

#  Données du message de contact à tester
data = {
    "name": "Jean Dupont",
    "email": "jean.dupont@example.com",
    "number": "+237690112233",
    "message": "Bonjour, j'aimerais avoir plus d'informations sur votre application."
}

#  Requête POST vers l'API
response = requests.post(url, headers=headers, json=data)

#  Affichage des résultats
if response.status_code == 200:
    print("✅ Message envoyé avec succès :")
    print(response.json())
else:
    print(f"❌ Erreur {response.status_code} :")
    print(response.text)
