from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_9ano"]

# Buscar nomes distintos dos municípios
municipios = colecao.distinct("NO_MUNICIPIO")

# Ordenar os nomes
municipios.sort()

# Salvar em arquivo TXT
with open("municipios_saeb_2021.txt", "w", encoding="utf-8") as f:
    for nome in municipios:
        f.write(nome + "\n")

# Mensagem final
print(f"✅ {len(municipios)} municípios salvos em 'municipios_saeb_2021.txt'.")

# Fechar a conexão
client.close()

