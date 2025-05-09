# # ____________homeapi '/api'________________# ____________homeapi '/api'________________

# import requests
# "
# endpoint = "http://localhost:8000/api/" #http://127.0.0.1:8000/ 

# get_response = requests.get(endpoint) # HTTP Request
# t raw text response

# print(get_response.json())









# # ________________dataentry__________________# ________________dataentry__________________



# import requests

# endpoint = "http://localhost:8000/api/dataentry" #http://127.0.0.1:8000/ 
# headers = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
# }

# get_response = requests.get(endpoint, headers=headers) # HTTP Request


# if get_response.status_code == 200:
#     print("Accès autorisé, réponse:", get_response.json())
# else:
#     print("Erreur d'accès:", get_response.status_code, get_response.text)












# # ________________report__________________# ________________report__________________



# import requests

# endpoint = "http://localhost:8000/api/report" #http://127.0.0.1:8000/ 
# headers = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
# }

# get_response = requests.get(endpoint, headers=headers) # HTTP Request


# if get_response.status_code == 200:
#     print("Accès autorisé, réponse:", get_response.json())
# else:
#     print("Erreur d'accès:", get_response.status_code, get_response.text)









# ________________success__________________# ________________success__________________



import requests

endpoint = "http://localhost:8000/api/dbsuccess" #http://127.0.0.1:8000/ 
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MDk3OTY5LCJpYXQiOjE3NDY3Mzc5NjcsImp0aSI6IjBiYmEzYmRkNWE4MzRjMmY4MjgwMTE2MGE3Zjc4MWM2IiwidXNlcl9pZCI6MX0.jMxDhh7NT8RL4cM6FplHnFw4xLUXK4Umn7U8CivBsJk'
}

get_response = requests.get(endpoint, headers=headers) # HTTP Request


if get_response.status_code == 200:
    print("Accès autorisé, réponse:", get_response.json())
else:
    print("Erreur d'accès:", get_response.status_code, get_response.text)
