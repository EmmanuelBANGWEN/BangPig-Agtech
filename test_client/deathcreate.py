
# # ✅ 1. Requête GET : récupérer les infos de décès d’un animal


# import requests

# animal_id = 'teststageS'  # Remplace par un ID existant
# url = f'http://127.0.0.1:8000/api/death/{animal_id}'
# headers = {
#     'Authorization': 'Bearer VOTRE_TOKEN_ICI',  # remplace avec ton token valide
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     print("Infos décès récupérées :", response.json())
# else:
#     print("Erreur GET :", response.status_code, response.text)









# ✅ 2. Requête POST : enregistrer un nouveau décès pour cet animal


import requests

animal_id = 'teststageS'  # Remplace par un ID existant
url = f'http://127.0.0.1:8000/api/create/death/{animal_id}'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
    # 'Content-Type': 'application/json'
}

data = {

    "date_death": "2025-05-09",
    "postmortem_findings": "Maladie",
    "cause_death": "Fièvre porcine détectée à l'avance."
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Décès enregistré :", response.json())
else:
    print("Erreur POST :", response.status_code, response.text)
