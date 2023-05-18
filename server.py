#pip install flask
from flask import Flask, request, Response, jsonify
import ssl, json


#- A gente precisa criar um sistema que recebe um webhook do sistema de pagamento e decida como vamos tratar o cliente

#- se o cliente tem o pagamento aprovado, então devemos:
	#- liberar o acesso dele ao curso
	#- enviar mensagem de boas vindas
#- se o cliente tem o pagamento recusado
	#- enviar mensagem de pagamento recusado
#- se o cliente tem o status reembolsado
	#- tirar o acesso dele ao curso
#- Precisamos ter registrado (para poder consultar quando precisarmos) todos os webhooks que chegaram e todas as "tratativas" que o sistema fez.
	#Ex: se o sistema mandou liberar o acesso ao curso e enviou mensagem, tem que ter um registro que o sistema fez isso (no banco de dados mesmo)
#- o sistema precisa ter autenticação de login para só poder entrar usuários autorizados. A criação de conta só pode ser feita por usuários que tenham o token: uhdfaAADF123 que deve ser enviado junto do formulário de criação de conta
#- os usuários devem ter 1 tela onde possam ver todas as tratativas que o sistema fez para cada usuário e que seja possível pesquisar por um usuário e ver o que rolou com ele

#As funcionalidades de enviar mensagem, tirar acesso e liberar acesso não precisam "fazer nada", só precisam "printar o que seria feito", do tipo:
#print("Liberar acesso do e-mail: fulano@email.com")
#ou então
#print("Enviar mensagem de boas vindas para o email: fulano@email.com")

pagamentos = [
               {'nome': 'Kalpana', 'email': 'teste@teste.com', 'status': 'aprovado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Caio', 'email': 'teste.caio@teste.com', 'status': 'recusado', 'valor': 800, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Amanda', 'email': 'teste.amanda@teste.com', 'status': 'reembolsado', 'valor': 750, 'forma_pagamento': 'pix', 'parcelas': 5}
    
             ]

users = [
             {"username": "Carlos", "secret": "@admin456"}    
        ]

def check_user(username, secret):
    for user in users:
        if (user["username"] == username) and (user["secret"] == secret):
            return True
    return False

def liberar_acesso(username):
    # Corpo da função
    # Código para liberar o acesso ao curso
    print("Bem-vindo(a),", username)
    print("Acesso ao curso liberado!")
    
def verificar_pagamento_recusado(informacoes_pagamento):
    # Código para verificar o pagamento
    if informacoes_pagamento["status"] == "recusado":
        print("Pagamento recusado do cliente:", informacoes_pagamento["cliente"])
    else:
        print("Pagamento aprovado do cliente:", informacoes_pagamento["cliente"])
informacoes_pagamento = {
    "nome": "Amanda",
    "status": "recusado",
}

verificar_pagamento_recusado(informacoes_pagamento)

def verificar_pagamento_reenbolsado(informacoes_pagamento):
    # Código para verificar o pagamento
    if informacoes_pagamento["status"] == "reembolsado":
        print("Pagamento reembolsado do cliente:", informacoes_pagamento["cliente"])
    else:
        print("Pagamento não reembolsado do cliente:", informacoes_pagamento["cliente"])
# Exemplo de obtenção das informações do pagamento
informacoes_pagamento = {
    "nome": "Caio",
    "status": "reembolsado",
    # Outras informações relevantes
}

# Chamar a função para verificar o pagamento
verificar_pagamento_reenbolsado(informacoes_pagamento)
     
          

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/pagamentos")
def get_pagamentos():
    return {'pagamentos': pagamentos}

@app.route("/pagamentos/<status>")
def get_pagamentos_status(status):
    out_pagamentos = []
    for pagamento in pagamentos:
        if status == pagamento['status'].lower():
            out_pagamentos.append(pagamento)
    return {'pagamentos': out_pagamentos} 
    
@app.route("/pagamentos/<info>/<value>")
def get_pagamentos_info(info, value):
    out_pagamentos = []
    for pagamento in pagamentos:
        if info in pagamento.keys():
            value_pagamento = pagamento[info]
            
            if type(value_pagamento) == str:
                if value == value_pagamento.lower():
                    out_pagamentos.append(pagamento)
            if type(value_pagamento) == int:
                if int(value) == value_pagamento:
                    out_pagamentos.append(pagamento)       
                    
    return {'pagamento': out_pagamentos}



@app.route("/informations", methods=['POST'])
def get_pagamentos_post():
    
    username = request.form['username']
    secret = request.form['secret']
    
    if not check_user(username, secret):
        #401 http Unauthorized
        return Response("Unauthorized", status=401)
    
    info = request.form['info']
    value = request.form['value']
    
    out_pagamentos = []
    for pagamento in pagamentos:
        if info in pagamento.keys():
            value_pagamento = pagamento[info]
            
            if type(value_pagamento) == str:
                if value == value_pagamento.lower():
                    out_pagamentos.append(pagamento)
            if type(value_pagamento) == int:
                if int(value) == value_pagamento:
                    out_pagamentos.append(pagamento)       
                    
    return {'pagamento': out_pagamentos}
            
#sistema que recebe um webhook do sistema de pagamento

@app.route("/", methods=["POST"])
def imprimir():
    response = {"status": 200}
    return jsonify(response)

@app.route("/pix", methods=["POST"])
def imprimirPix():
    imprime = print(request.json)
    data = request.json
    with open('data.txt', 'a') as outfile:
        outfile.write("\n")
        json.dump(data, imprime)
    return jsonify(imprime)

if __name__ == "__main__":
    app.run(debug=True)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('chain-pix-prod.crt')
    context.load_cert_chain(
        'caminho-certificados/server_ssl.crt.pem', #Gerar uma chave privada
        'caminho-certificados/server_ssl.key.pem') #Gerar uma chave publica
    app.run(ssl_context=context, host='0.0.0.0')