import os
import re
import csv
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Padrões de campo com expressões mais amplas
padroes = {
    "PV1MATH": re.compile(r"(pv\d*math|math|matematica|mat)\w*", re.IGNORECASE),
    "PV1READ": re.compile(r"(pv\d*read|read|leitura|lectura|lec)\w*", re.IGNORECASE),
    "PV1SCIE": re.compile(r"(pv\d*scie|science|ciencias|sci)\w*", re.IGNORECASE),
}

# Caminho de saída
saida_csv = "dados_processados/mapa_campos_desempenho_pisa.csv"
os.makedirs(os.path.dirname(saida_csv), exist_ok=True)

# Cabeçalho
resultados = [("colecao", "campo_detectado", "campo_equivalente")]

# Iterar sobre coleções
for nome_col in db.list_collection_names():
    doc = db[nome_col].find_one()
    if not doc:
        continue
    for campo in doc.keys():
        for nome_padrao, regex in padroes.items():
            if regex.fullmatch(campo.lower()):
                resultados.append((nome_col, campo, nome_padrao))
                break

# Gravar CSV
with open(saida_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(resultados)

client.close()

print(f"✔ Arquivo salvo em: {saida_csv}")

