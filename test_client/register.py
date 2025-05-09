import requests

url = 'http://127.0.0.1:8000/api/register/'  # adapte le chemin si nécessaire

# Données d'inscription à envoyer
data = {
    'username': 'nouvelutilisateur',
    'email': 'nouveau@exemple.com',
    'password1': 'motdepassefort123',
    'password2': 'motdepassefort123'  # si tu as une validation par double mot de passe
}

# Envoi de la requête POST
response = requests.post(url, data=data)

# Affichage des résultats
if response.status_code == 201:
    print("✅ Inscription réussie :", response.json())
else:
    print(f"❌ Erreur {response.status_code} :", response.json())
