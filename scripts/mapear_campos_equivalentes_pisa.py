import os
import re
import csv
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Expressões regulares para identificar variações de campos
padroes = {
    "PV1MATH": re.compile(r"(pv|p)?(math|mat|m)\d*", re.IGNORECASE),
    "PV1READ": re.compile(r"(pv|p)?(read|leitura|r)\d*", re.IGNORECASE),
    "PV1SCIE": re.compile(r"(pv|p)?(scie|science|ciencias|s)\d*", re.IGNORECASE),
    "CNT": re.compile(r"(cnt|pais|country)", re.IGNORECASE)
}

# Caminho de saída
saida_csv = "dados_processados/mapa_equivalencia_campos_pisa.csv"
os.makedirs(os.path.dirname(saida_csv), exist_ok=True)

# Cabeçalho do CSV
resultados = [("colecao", "campo_detectado", "campo_equivalente")]

# Verifica campos em cada coleção
for nome_col in db.list_collection_names():
    doc = db[nome_col].find_one()
    if not doc:
        continue
    for campo in doc.keys():
        for nome_padrao, regex in padroes.items():
            if regex.fullmatch(campo.lower()):
                resultados.append((nome_col, campo, nome_padrao))
                break

# Salvar em CSV
with open(saida_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(resultados)

# Fechar conexão
client.close()

print(f"✔ Arquivo salvo em: {saida_csv}")

