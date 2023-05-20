import requests

data = {"username": "Carlos", "secret": "@admin456","info":"status", "value":"aprovado"}
response = requests.post("http://127.0.0.1:5000/informations", data=data)

#response = requests.get('http://127.0.0.1:5000/pagamentos')

if response.status_code == 200:
    message = response.json()
    print(message['pagamento'])
    print("Bem-vindo(a)")
else:
    print(response.status_code)
    
    
    
# Login e cadastro


usuarios = {
    "usuario1": {
        "senha": "senha1",
        "token": "token1"
    },
    "usuario2": {
        "senha": "senha2",
        "token": "token2"
    }
}

def criar_conta():
    nome_usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    token = input("Digite o token: ")

    if token_valido(token):
        usuarios[nome_usuario] = {"senha": senha, "token": token}
        print("Conta criada com sucesso!")
    else:
        print("Token inválido!")

def fazer_login():
    nome_usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    

    if nome_usuario in usuarios and usuarios[nome_usuario]["senha"] == senha:
        print("Login bem-sucedido!")
        print("Acesso ao curso liberado!")
    else:
        print("Usuário ou senha inválidos!")

def token_valido(token):
    # Verificar se o token é válido (implemente a lógica de validação do token conforme sua necessidade)
    # Retorna True se o token for válido e False caso contrário
    return True

# Exemplo de uso:
opcao = input("Escolha uma opção: 1 - Criar conta | 2 - Fazer login: ")

if opcao == "1":
    criar_conta()
elif opcao == "2":
    fazer_login()
else:
    print("Opção inválida!")


