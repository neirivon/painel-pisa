from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
import pandas as pd
import unidecode

# === Conexão com o MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["ibge_microrregioes_2015"]

# === Função para normalizar os nomes ===
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unidecode.unidecode(str(texto).lower().strip())

# === Buscar todos os nomes das microrregiões ===
docs = list(colecao.find({}, {"_id": 0, "NM_MICRO": 1}))
df = pd.DataFrame(docs)
df["NM_MICRO_NORM"] = df["NM_MICRO"].apply(normalizar)

# === Palavras-chave para investigar ===
palavras_alvo = ["acarau", "camocim"]

# === Filtrar e exibir possíveis correspondências ===
for palavra in palavras_alvo:
    print(f"\n🔎 Microrregiões que contêm '{palavra}':\n")
    print(df[df["NM_MICRO_NORM"].str.contains(palavra, na=False)].to_string(index=False))

# === Encerrar a conexão com o banco ===
client.close()

