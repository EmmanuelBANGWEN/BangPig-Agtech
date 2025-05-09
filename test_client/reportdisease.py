import requests

# Remplace par l'URL de ton endpoint API
url = "http://localhost:8000/api/report/disease" 

# Remplace ce token par celui de ton utilisateur connecté
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ Réponse OK")
    print(response.json())
else:
    print(f"❌ Erreur: {response.status_code}")
    print(response.text)
