import requests

# ✅ URL de l'API (à adapter selon ton projet local ou déployé)
url = "http://localhost:8000/api/search_update/"

# 🔐 En-têtes avec le token d’authentification
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# ========================
# 1. Requête GET (Recherche)
# ========================
params = {
    "query": "test001" 
}
response_get = requests.get(url, headers=headers, params=params)

print("🔍 GET - Résultat de la recherche :")
print(response_get.status_code)
print(response_get.json())

# ========================
# ✏️ 2. Requête POST (Mise à jour)
# ========================
data_post = {
    "query": "test001",  # Le même ID que pour la recherche
    "updated_data": {
        "breed": "fff", 
    }
}

response_post = requests.post(url, headers=headers, json=data_post)

print("\n✏️ POST - Résultat de la mise à jour :")
print(response_post.status_code)
print(response_post.json())
