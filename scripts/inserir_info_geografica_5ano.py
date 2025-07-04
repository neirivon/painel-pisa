from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_info_geografica_5ano.py

import pandas as pd
from pymongo import MongoClient

# === 1. Caminho do CSV extraído ===
CAMINHO_CSV = "municipios_ibge_mesorregioes_microregioes.csv"

# === 2. Conexão MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_5ano"]

# === 3. Carregar CSV com dados do IBGE ===
df_ibge = pd.read_csv(CAMINHO_CSV)

# === 4. Contador de atualizações ===
total_atualizados = 0

# === 5. Atualizar cada documento da coleção ===
for _, row in df_ibge.iterrows():
    id_municipio = int(row["ID_MUNICIPIO"])
    update_result = colecao.update_many(
        {"ID_MUNICIPIO": id_municipio},
        {
            "$set": {
                "NO_MUNICIPIO": row["NO_MUNICIPIO"],
                "NO_UF": row["NO_UF"],
                "REGIAO": row["REGIAO"],
                "MESORREGIAO": row["MESORREGIAO"],
                "MICRORREGIAO": row["MICRORREGIAO"]
            }
        }
    )
    total_atualizados += update_result.modified_count

# === 6. Encerrar conexão e feedback ===
client.close()
print(f"✅ {total_atualizados} documentos atualizados com sucesso na coleção 'saeb_2021_municipios_5ano'.")

