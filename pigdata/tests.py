# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from django.urls import reverse

# class APITest(APITestCase):

#     def setUp(self):
#         # Crée un utilisateur de test
#         self.username = 'testuser'
#         self.password = 'testpass'
#         self.user = User.objects.create_user(username=self.username, password=self.password)
#         self.token = Token.objects.create(user=self.user)

#     def test_home_api(self):
#         # Authentification avec le token
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.get('/api/')  # ou reverse('homeapi')
#         self.assertEqual(response.status_code, 200)

#     def test_login_api(self):
#         # Test du login avec une requête POST
#         data = {
#             'username': self.username,
#             'password': self.password
#         }
#         response = self.client.post('/api/login/', data, format='json')  # ou reverse('loginuserapi')
#         self.assertIn(response.status_code, [200, 400])  # 400 si déjà logué, 200 si OK

#     def test_register_api(self):
#         # Test de l'inscription
#         data = {
#             'username': 'newuser',
#             'password': 'newpass',
#             'email': 'newuser@example.com'
#         }
#         response = self.client.post('/api/register/', data, format='json')
#         self.assertIn(response.status_code, [200, 201, 400])

#     def test_dataentry_api_unauthenticated(self):
#         # Doit refuser sans token
#         response = self.client.get('/api/dataentry/')
#         self.assertEqual(response.status_code, 401)

#     def test_dataentry_api_authenticated(self):
#         # Doit fonctionner avec le token
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.get('/api/dataentry/')
#         self.assertIn(response.status_code, [200, 204])  # adapte selon la vue

#     def test_logout_api(self):
#         # Authentifie l'utilisateur
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.post('/api/logout/')
#         self.assertIn(response.status_code, [200, 204])


from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class AuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_and_access_protected_view(self):
        # Login
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        token = response.data['access']

        # Access protected view
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/dataentry/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bienvenue', response.data['message'])
