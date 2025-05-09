import requests

animal_id = 'teststageS'
url = f'http://127.0.0.1:8000/api/update/{animal_id}'

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk',  # remplace par ton vrai token d’accès
}

# Envoi d'une requête GET
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Données Page update info de l'animal récupérées :", response.json())
else:
    print("Erreur GET :", response.status_code, response.text)
