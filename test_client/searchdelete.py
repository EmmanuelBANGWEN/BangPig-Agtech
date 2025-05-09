import requests

# 🔗 URL de l'API avec le paramètre `query`
base_url = "http://localhost:8000/api/search_delete/"  # Remplace par l’URL réelle
params = {
    "query": "manu f"  # Remplace par un animal_id existant
}

# 🔐 En-têtes avec authentification (Token ou JWT)
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # "Content-Type": "application/json"
}

# 🚀 Envoi de la requête GET
response = requests.get(base_url, headers=headers, params=params)

# 📊 Affichage des résultats
if response.status_code == 200:
    print("✅ Résultats de la recherche :")
    print(response.json())
else:
    print(f"❌ Erreur {response.status_code} :")
    print(response.text)
