from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_municipios_saeb2021.py

from pymongo import MongoClient

# === Dados dos municípios (Top 10 e Bottom 10) ===
dados = [
    # TOP 10
    {"CO_MUNICIPIO": 2308005, "NO_MUNICIPIO": "Massapê", "ESTADO": "CE", "REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Sobral", "MEDIA_5_LP": 316.17, "MEDIA_5_MT": 336.30},
    {"CO_MUNICIPIO": 2310951, "NO_MUNICIPIO": "Pires Ferreira", "ESTADO": "CE", "REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Ipu", "MEDIA_5_LP": 313.39, "MEDIA_5_MT": 320.15},
    {"CO_MUNICIPIO": 2301257, "NO_MUNICIPIO": "Ararendá", "ESTADO": "CE", "REGIAO": "Nordeste", "MESORREGIAO": "Sertões Cearenses", "MICRORREGIAO": "Sertão de Crateús", "MEDIA_5_LP": 309.52, "MEDIA_5_MT": 329.73},

    # BOTTOM 10
    {"CO_MUNICIPIO": 1303908, "NO_MUNICIPIO": "São Paulo de Olivença", "ESTADO": "AM", "REGIAO": "Norte", "MESORREGIAO": "Sudoeste Amazonense", "MICRORREGIAO": "Alto Solimões", "MEDIA_5_LP": 123.56, "MEDIA_5_MT": 141.08},
    {"CO_MUNICIPIO": 2203008, "NO_MUNICIPIO": "Cristalândia do Piauí", "ESTADO": "PI", "REGIAO": "Nordeste", "MESORREGIAO": "Sudoeste Piauiense", "MICRORREGIAO": "Chapadas do Extremo Sul Piauiense", "MEDIA_5_LP": 128.25, "MEDIA_5_MT": 149.90},
    {"CO_MUNICIPIO": 1304062, "NO_MUNICIPIO": "Tabatinga", "ESTADO": "AM", "REGIAO": "Norte", "MESORREGIAO": "Sudoeste Amazonense", "MICRORREGIAO": "Alto Solimões", "MEDIA_5_LP": 128.91, "MEDIA_5_MT": 152.59},
    {"CO_MUNICIPIO": 1501105, "NO_MUNICIPIO": "Bagre", "ESTADO": "PA", "REGIAO": "Norte", "MESORREGIAO": "Marajó", "MICRORREGIAO": "Portel", "MEDIA_5_LP": 129.76, "MEDIA_5_MT": 156.28},
    {"CO_MUNICIPIO": 1400704, "NO_MUNICIPIO": "Uiramutã", "ESTADO": "RR", "REGIAO": "Norte", "MESORREGIAO": "Norte de Roraima", "MICRORREGIAO": "Nordeste de Roraima", "MEDIA_5_LP": 135.02, "MEDIA_5_MT": 131.16},
    {"CO_MUNICIPIO": 2401701, "NO_MUNICIPIO": "Bom Jesus", "ESTADO": "RN", "REGIAO": "Nordeste", "MESORREGIAO": "Agreste Potiguar", "MICRORREGIAO": "Agreste Potiguar", "MEDIA_5_LP": 149.76, "MEDIA_5_MT": 142.10},
    {"CO_MUNICIPIO": 2110401, "NO_MUNICIPIO": "São Benedito do Rio Preto", "ESTADO": "MA", "REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Chapadinha", "MEDIA_5_LP": 129.97, "MEDIA_5_MT": 142.60}
]

# === Conexão com o MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_topbottom"]

# === Inserir os dados ===
colecao.delete_many({})  # Limpa antes para evitar duplicação
resultado = colecao.insert_many(dados)
client.close()

print(f"✅ {len(resultado.inserted_ids)} documentos inseridos com sucesso na coleção 'saeb_2021_municipios_topbottom'")

