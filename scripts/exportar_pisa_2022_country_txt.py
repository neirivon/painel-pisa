from pymongo import MongoClient
from pprint import pformat
from pathlib import Path

# Conectar ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017")
colecao = client["pisa"]["pisa_2022_country_cognitive"]

# Buscar até 50 documentos
documentos = list(colecao.find({}, {"_id": 0}).limit(50))
client.close()

# Formatando a saída para melhor leitura
texto_formatado = "\n\n".join([pformat(doc) for doc in documentos])

# Caminho de saída
arquivo_saida = Path("amostra_pisa_2022_country_cognitive.txt")
arquivo_saida.write_text(texto_formatado, encoding="utf-8")

print(f"✅ Arquivo salvo com sucesso em: {arquivo_saida.resolve()}")

