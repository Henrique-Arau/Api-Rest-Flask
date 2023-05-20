import requests

data = {"username": "Carlos", "secret": "@admin456","status":"aprovado", "nome":"joão", "email":"joão@teste.com.br", "status":"reprovado", "valor": 600, "forma_pagamento":"pix", "parcelas": 5}
response = requests.post("http://127.0.0.1:5000/register", data=data)

#response = requests.get('http://127.0.0.1:5000/pagamentos')

if response.status_code == 200:
    message = response.json()
    print(message['pagamento'])
    print("Bem-vindo(a)")
else:
    print(response.status_code)
    
    
    
