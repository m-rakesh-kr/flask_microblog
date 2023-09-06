import requests

# response = requests.get('http://localhost:8000/api/users/1')
# print(response.json())


response = requests.post('http://localhost:8000/api/tokens', auth=('rakesh', 'mypassword'))
print(response.json())

