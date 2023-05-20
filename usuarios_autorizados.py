# Código de exemplo para um sistema com autenticação de login em Python

# Dicionário com usuários autorizados (pode ser substituído por um banco de dados)
usuarios_autorizados = {
    'usuario1': 'senha1',
    'usuario2': 'senha2',
    'usuario3': 'senha3'
}

def login():
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    # Verificar se o usuário e a senha estão corretos
    if username in usuarios_autorizados and usuarios_autorizados[username] == password:
        print("Login bem-sucedido: Usuario autorizado!")
        # Resto do código do sistema após o login bem-sucedido
    else:
        print("Usuario não authorizado!")

# Chamada da função de login para testar o sistema
login()


