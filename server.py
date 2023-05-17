#pip install flask
from flask import Flask


#Se o cliente tem o pagamento aprovado
#Se o cliente tem o pagamento reprovado
#Se o cliente tem o pagamento reenbolsado

pagamentos = [
               {'nome': 'Kalpana', 'email': 'teste@teste.com', 'status': 'aprovado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Caio', 'email': 'teste.caio@teste.com', 'status': 'recusado', 'valor': 800, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Amanda', 'email': 'teste.amanda@teste.com', 'status': 'reembolsado', 'valor': 750, 'forma_pagamento': 'pix', 'parcelas': 5}
    
             ]


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
            
                

if __name__ == "__main__":
    app.run(debug=True)