from pymongo import MongoClient
import pandas as pd

# Conexão com MongoDB local
client = MongoClient("mongodbos.path.join(:, "/")localhost:27017/")
db = client["pisa"]

# Lista de coleções alvo
colecoes = [
    "pisa_2000_medias",
    "pisa_ocde_2000_relatorio",
    "pisa2000_comparativo_lmc",
    "pisa2000_medias_oficiais",
    "pisa2000_student_escs",
    "pisa2003_student",
    "relatorios_inep_pisa",
    "relatorios_inep_pisa_bloom",
    "relatorios_inep_pisa_bloom_nova",
    "relatorios_inep_pisa_secoes"
]

# Função para coletar estatísticas básicas da coleção
def analisar_colecao(nome_colecao):
    colecao = db[nome_colecao]
    total_docs = colecao.count_documents({})
    exemplo = colecao.find_one()
    campos = list(exemplo.keys()) if exemplo else []
    return {
        "colecao": nome_colecao,
        "total_documentos": total_docs,
        "campos_exemplo": campos
    }

# Executa análise
resultados = [analisar_colecao(nome) for nome in colecoes]

# Mostra resultado em tabela
df = pd.DataFrame(resultados)
print(df.to_string(index=False))

