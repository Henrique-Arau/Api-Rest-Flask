#pip install flask
from flask import Flask, request, Response, jsonify, g
import ssl, json
import smtplib
import sqlite3


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

#pagamentos = [
#               {'nome': 'Kalpana', 'email': 'teste@teste.com', 'status': 'aprovado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Caio', 'email': 'teste.caio@teste.com', 'status': 'recusado', 'valor': 800, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Amanda', 'email': 'teste.amanda@teste.com', 'status': 'reembolsado', 'valor': 750, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Joao', 'email': 'teste.joao@teste.com', 'status': 'removido', 'valor': 600, 'forma_pagamento': 'pix', 'parcelas': 4}
#    
#             ]


# criar o aplicativo
app = Flask(__name__)

DB_URL = "enterprise.db"



users = [
             {"username": "Carlos", "secret": "@admin456"}    
        ]

@app.before_request
def before_request():
    print("Conectando ao banco")
    conn = sqlite3.connect(DB_URL)
    g.conn = conn

@app.teardown_request
def after_request(exception):
    if g.conn is not None:
        g.conn.close
        print("Desconectando ao banco")
        
def query_employers_to_dict(conn, query):
    cursor = conn.cursor() 
    cursor.execute(query)
    employers_dict = [{'nome':row[0], 'email':row[1], 'status':row[2], 'valor':row[3], 'forma_pagamento':row[4], 'parcelas':row[5]}
                       for row in cursor.fetchall()]
    return employers_dict

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
    
#Recusado

def enviar_email(destinatario, assunto, corpo):
    remetente = "seu_email@example.com"
    senha = "sua_senha_do_email"

    mensagem = f"Subject: {assunto}\n\n{corpo}"

    with smtplib.SMTP("smtp.example.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, mensagem)

def pagamento_recusado(cliente):
    # Código para identificar o pagamento recusado
    # ...
    
    # Enviar mensagem de pagamento recusado
    destinatario = cliente["email"]
    assunto = "Pagamento Recusado"
    corpo = f"Olá {cliente['nome']}, o seu pagamento foi recusado. Por favor, entre em contato conosco para resolver a situação."

    enviar_email(destinatario, assunto, corpo)

# Exemplo de informações do cliente
    cliente = {
    "nome": "Caio",
    "email": "teste.caio@teste.com",
    # Outras informações do cliente
    }

# Chamar a função para enviar a mensagem de pagamento recusado
    pagamento_recusado(cliente)


#Reenbolsado

def verificar_pagamento_reenbolsado(informacoes_pagamento):
    # Código para verificar o pagamento
    if informacoes_pagamento["status"] == "reembolsado":
        print("Pagamento reembolsado do cliente:", informacoes_pagamento["cliente"])
    else:
        print("Pagamento não reembolsado do cliente:", informacoes_pagamento["cliente"])
# Exemplo de obtenção das informações do pagamento
    informacoes_pagamento = {
    "nome": "Amanda",
    "status": "reembolsado",
    # Outras informações relevantes
    }

# Chamar a função para verificar o pagamento
    verificar_pagamento_reenbolsado(informacoes_pagamento)

def remover_acesso_cliente(cliente):
    # Código para remover o acesso do cliente ao serviço
    # ...
    print("Acesso removido para o cliente:", cliente)
# Exemplo de identificação do cliente após o reembolso
    cliente = {
    "nome": "Joao",
    "id": 12345,
    # Outras informações do cliente
    }

# Chamar a função para remover o acesso
    remover_acesso_cliente(cliente)

          

@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/pagamentos")
def get_pagamentos():
    
    query = """
               SELECT nome, email, status, valor, forma_pagamento, parcelas
               FROM pagamentos;
    """
    
    employers_dict = query_employers_to_dict(g.conn, query)
    
    print(employers_dict)
    return {'pagamentos': employers_dict}

@app.route("/pagamentos/<status>")
def get_pagamentos_status(status):
    
    query = """
               SELECT nome, email, status, valor, forma_pagamento, parcelas
               FROM pagamentos
               WHERE "status" LIKE "{}";
    """.format(status)
    
    employers_dict = query_employers_to_dict(g.conn, query)
    
    return {'pagamentos': employers_dict} 

    
@app.route("/pagamentos/<info>/<value>")
def get_pagamentos_info(info, value):
    
    if value.isnumeric():
        value = float(value)
    
    query = """
               SELECT nome, email, status, valor, forma_pagamento, parcelas
               FROM pagamentos
               WHERE "{}" LIKE "{}";
    """.format(info, value)
    
    employers_dict = query_employers_to_dict(g.conn, query)
                    
    return {'pagamentos': employers_dict}



@app.route("/register", methods=['POST'])
def get_pagamentos_post():
    
    username = request.form['username']
    secret = request.form['secret']
    
    if not check_user(username, secret):
        #401 http Unauthorized
        return Response("Unauthorized", status=401)
    
    
    nome = request.form['nome']
    email = request.form['email']
    status = request.form['status']
    valor = request.form['valor']
    forma_pagamento = request.form['forma_pagamento']
    parcelas = request.form['parcelas']
    
    
    query = """
        INSERT INTO pagamentos (nome, email, status, valor, forma_pagamento, parcelas)
        VALUES ("{}", "{}", "{}", "{}", "{}", "{}");
    """.format(nome, email, status, valor, forma_pagamento, parcelas)
    
    cursor = g.conn.cursor()
    cursor.execute(query)
    
    g.conn.commit()
        
                    
    return {'pagamento': "Registered employee"}
            
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