from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
import unicodedata
import pandas as pd

def normalizar(texto):
    """Remove acentos e transforma em minúsculas para comparação."""
    if not isinstance(texto, str): return ""
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in texto if not unicodedata.combining(c)]).lower().strip()

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
collection = db["saeb_2021_municipios_9ano"]

# Correções manuais
correcoes = {
    "ararenda": {"REGIAO": "Nordeste", "MESORREGIAO": "Sertões Cearenses", "MICRORREGIAO": "Sertão de Crateús"},
    "cruz": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Acaraú"},
    "jijoca de jericoacoara": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Camocim"},
    "santana do mundau": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Alagoano", "MICRORREGIAO": "União dos Palmares"},
    "sao vicente ferrer": {"REGIAO": "Nordeste", "MESORREGIAO": "Norte Maranhense", "MICRORREGIAO": "Viana"}
}

relatorio = []
for doc in collection.find({}, {"_id": 1, "NO_MUNICIPIO": 1}):
    nome_municipio = normalizar(doc.get("NO_MUNICIPIO", ""))
    for nome_corrigido, campos in correcoes.items():
        if nome_corrigido in nome_municipio:
            result = collection.update_one(
                {"_id": doc["_id"]},
                {"$set": campos}
            )
            relatorio.append({
                "NO_MUNICIPIO": doc["NO_MUNICIPIO"],
                "REFERENCIA": nome_corrigido,
                "ATUALIZADO": result.modified_count > 0
            })

# Salvar relatório para auditoria
df_relatorio = pd.DataFrame(relatorio)
df_relatorio.to_csv("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "r")elatorio_correcao_microrregioes.csv", index=False)

print("🚀 Atualizações concluídas. Total de registros corrigidos:", len(df_relatorio))
client.close()

