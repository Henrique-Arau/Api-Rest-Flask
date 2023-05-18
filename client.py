import requests

data = {"username": "Carlos", "secret": "@admin456","info":"status", "value":"aprovado"}
response = requests.post("http://127.0.0.1:5000/informations", data=data)

if response.status_code == 200:
    message = response.json()
    print(message['pagamento'])
    print("Bem-vindo(a)")
    print("Acesso ao curso liberado!")
else:
    print(response.status_code)

