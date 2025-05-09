import requests

# 📌 Identifiants à tester (à adapter)
animal_id = "test001"
service_id = 5  # ID du service à supprimer

# 🔗 URL de ton endpoint DELETE (à adapter selon ton routing)
url = f"http://localhost:8000/api/delete/nutrition/{animal_id}/{service_id}"

# 🔐 Remplace par un vrai token d'utilisateur authentifié
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
}

# 📡 Envoi de la requête DELETE
response = requests.delete(url, headers=headers)

# 📤 Affichage du résultat
if response.status_code == 200:
    print("✅ Succès :")
    print(response.json())
else:
    print(f"❌ Erreur {response.status_code} :")
    print(response.text)
