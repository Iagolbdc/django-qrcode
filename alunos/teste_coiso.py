import requests

request = {
	"email": "iago@123.com",
	"password": "12345678"
}

response = requests.post("http://localhost:8000/auth/login/", data=request)

token_access = response.json()["tokens"]["access"]

headers = {
    "Authorization": f"Bearer {token_access}"
}

verify = requests.post("http://localhost:8000/aluno/verificar_horarios/", headers=headers)