# scriptos.path.join(s, "t")estar_leitura_mongo_terminal.py

from painel_pisa.utils.conexao_mongo import conectar_mongo

# Conectar ao MongoDB
db, client = conectar_mongo()
colecao = db["questoes_ordenadas_v6a"]

# Buscar todas as questões
questoes = list(colecao.find({}, {"_id": 0}))

# Exibir as primeiras 3 questões para teste
for q in questoes[:3]:
    print("\n--- Questão ---")
    print(f"ID: {q.get('questao_id')}")
    print(f"Área: {q.get('area')}")
    print(f"Pergunta: {q.get('pergunta')}")

