import requests

# URL de ton API
BASE_URL = 'http://localhost:8000'  # Remplace par l'URL de ton serveur Django si nécessaire
TOKEN_OBTAIN_URL = f'{BASE_URL}/api/token/'
TOKEN_REFRESH_URL = f'{BASE_URL}/api/token/refresh/'

# Identifiants de l'utilisateur
username = 'trebmal'  # Remplace par le nom d'utilisateur de test
password = 'manulove'  # Remplace par le mot de passe de test

# Fonction pour obtenir un token d'accès
def get_access_token():
    # Corps de la requête
    data = {
        'username': username,
        'password': password
    }

    # Envoi de la requête POST pour obtenir le token
    response = requests.post(TOKEN_OBTAIN_URL, data=data)

    if response.status_code == 200:
        print("Token obtenu avec succès!")
        # Réponse avec access et refresh token
        tokens = response.json()
        print(f"Access Token: {tokens['access']}")
        print(f"Refresh Token: {tokens['refresh']}")
        return tokens
    else:
        print(f"Échec de l'obtention du token: {response.status_code}")
        print(response.json())

# Fonction pour rafraîchir le token d'accès
def refresh_access_token(refresh_token):
    # Corps de la requête avec le refresh token
    data = {
        'refresh': refresh_token
    }

    # Envoi de la requête POST pour rafraîchir le token
    response = requests.post(TOKEN_REFRESH_URL, data=data)

    if response.status_code == 200:
        print("Token rafraîchi avec succès!")
        # Nouveau token d'accès
        new_tokens = response.json()
        print(f"Nouveau Access Token: {new_tokens['access']}")
        return new_tokens
    else:
        print(f"Échec du rafraîchissement du token: {response.status_code}")
        print(response.json())

if __name__ == '__main__':
    # Obtenir un premier token
    tokens = get_access_token()

    if tokens:
        # Utiliser le refresh token pour en obtenir un nouveau
        refresh_access_token(tokens['refresh'])
