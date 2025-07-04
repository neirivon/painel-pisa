from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# atualizar_ibge_saeb_5ano.py

from pymongo import MongoClient

# 🔗 Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_5ano"]

# 📘 Dicionário IBGE: mapeamento por código do município
dados_ibge = {
    6322170: {"NO_MUNICIPIO": "Vilhena", "NO_UF": "Rondônia", "REGIAO": "Norte", "MESORREGIAO": "Leste Rondoniense", "MICRORREGIAO": "Vilhena"},
    1100015: {"NO_MUNICIPIO": "Alta Floresta D'Oeste", "NO_UF": "Rondônia", "REGIAO": "Norte", "MESORREGIAO": "Leste Rondoniense", "MICRORREGIAO": "Cacoal"},
    1100023: {"NO_MUNICIPIO": "Ariquemes", "NO_UF": "Rondônia", "REGIAO": "Norte", "MESORREGIAO": "Madeira-Guaporé", "MICRORREGIAO": "Ariquemes"},
    # Adicione todos os demais municípios relevantes aqui...
}

# 🛠 Atualização em massa
contador = 0
for codigo, info in dados_ibge.items():
    resultado = colecao.update_many(
        {"ID_MUNICIPIO": codigo},
        {"$set": info}
    )
    contador += resultado.modified_count

client.close()
print(f"✅ {contador} documentos atualizados com sucesso na coleção 'saeb_2021_municipios_5ano'.")

