from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_ibge_microrregioes_corrigido.py

import pandas as pd
from pymongo import MongoClient

# Caminho do CSV exportado com geometria
CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")bge_microrregioes_geometry_corrigido.csv"

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["ibge_microrregioes_geometry"]

# Limpar coleção existente
colecao.delete_many({})
print("🧹 Coleção 'ibge_microrregioes_geometry' limpa com sucesso.")

# Carregar CSV com colunas reais
df = pd.read_csv(CAMINHO_CSV)

# Converter para dicionários
registros = df.to_dict(orient="records")

# Inserir na coleção
colecao.insert_many(registros)
print(f"✅ {len(registros)} documentos inseridos com sucesso na coleção 'ibge_microrregioes_geometry'.")

# Encerrar conexão
client.close()

