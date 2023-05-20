import sqlite3

pagamentos = [
               {'nome': 'Kalpana', 'email': 'teste@teste.com', 'status': 'aprovado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Caio', 'email': 'teste.caio@teste.com', 'status': 'recusado', 'valor': 800, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Amanda', 'email': 'teste.amanda@teste.com', 'status': 'reembolsado', 'valor': 750, 'forma_pagamento': 'pix', 'parcelas': 5},
               {'nome': 'Joao', 'email': 'teste.joao@teste.com', 'status': 'removido', 'valor': 600, 'forma_pagamento': 'pix', 'parcelas': 4}
    
             ]

conn = sqlite3.connect('enterprise.db')

cursor = conn.cursor()

for pagamento in pagamentos:
    cursor.execute("""
            INSERT INTO pagamentos (nome, email, status, valor, forma_pagamento, parcelas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pagamento['nome'], pagamento['email'], pagamento['status'], pagamento['valor'], pagamento['forma_pagamento'], pagamento['parcelas']))
    
print("Dados inseridos com secesso!")
    
conn.commit()
conn.close()