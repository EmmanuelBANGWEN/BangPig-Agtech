import requests

# 🌐 URL de l’API
url = "http://localhost:8000/api/generate/"

# 🔐 En-têtes avec un token d'authentification admin valide
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# 🚀 Requête POST
response = requests.post(url, headers=headers)

# 📌 Affichage du résultat
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
