# import requests

# # Remplace par l'adresse de ton serveur local ou hébergé
# url = "http://127.0.0.1:8000/api/login/"

# # Données à envoyer
# data = {
#     "username": "trebmal",
#     "password": "manulove"
# }

# # Envoi de la requête POST
# response = requests.post(url, json=data)

# # Affichage du résultat
# print("Status code:", response.status_code)
# print("Response:", response.json())








# Logout test 

import requests

# URL de l'endpoint logout
url = 'http://127.0.0.1:8000/api/logout/'

# Jeton d'accès à insérer ici
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'  # mets ici ton vrai token JWT

# En-têtes avec le token JWT pour autoriser la requête
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Envoi de la requête GET pour se déconnecter
response = requests.get(url, headers=headers)

# Affichage du résultat
if response.status_code == 200:
    print("✅ Déconnexion réussie :", response.json())
else:
    print(f"❌ Erreur {response.status_code} :", response.json())
