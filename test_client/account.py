import requests


url = 'http://127.0.0.1:8000/api/account/'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
}

# Exemple de requête GET
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Accès autorisé, réponse:", response.json())
else:
    print("Erreur d'accès:", response.status_code, response.text)
