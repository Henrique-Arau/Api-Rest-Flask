import sqlite3

#pagamentos = [
#               {'nome': 'Kalpana', 'email': 'teste@teste.com', 'status': 'aprovado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Caio', 'email': 'teste.caio@teste.com', 'status': 'recusado', 'valor': 800, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Amanda', 'email': 'teste.amanda@teste.com', 'status': 'reembolsado', 'valor': 750, 'forma_pagamento': 'pix', 'parcelas': 5},
#               {'nome': 'Joao', 'email': 'teste.joao@teste.com', 'status': 'removido', 'valor': 600, 'forma_pagamento': 'pix', 'parcelas': 4}
#    
#             ]


conn = sqlite3.connect('enterprise.db')

cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE pagamentos (
                  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  nome VARCHAR(100),
                  email VARCHAR(100),
                  status VARCHAR(50),
                  valor DECIMAL(10, 2),
                  forma_pagamento VARCHAR(50),
                  parcelas INT 
                  );    
""")

print("Tabela criada com sucesso")

# desconectando do nosso banco de dados
conn.close()