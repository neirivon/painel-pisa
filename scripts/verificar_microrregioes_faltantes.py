from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
import pandas as pd
import unidecode

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]

# Coletar dados do SAEB e IBGE
df_saeb = pd.DataFrame(db["saeb_2021_municipios_9ano"].find({}, {"_id": 0, "NO_MUNICIPIO": 1, "MICRORREGIAO": 1}))
df_geo = pd.DataFrame(db["ibge_microrregioes_2015"].find({}, {"_id": 0, "NM_MICRO": 1}))

# Normalizador
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unidecode.unidecode(str(texto).lower().strip())

df_saeb["microrregiao_norm"] = df_saeb["MICRORREGIAO"].apply(normalizar)
df_geo["microrregiao_norm"] = df_geo["NM_MICRO"].apply(normalizar)

# Municípios-alvo da análise
municipios_alvo = [
    "Ararendá", "Cruz", "Pires Ferreira",
    "Santana do Mundaú", "São Vicente Ferrer", "Jijoca de Jericoacoara"
]

# Filtrar e verificar
df_alvo = df_saeb[df_saeb["NO_MUNICIPIO"].isin(municipios_alvo)].copy()
df_alvo["existe_na_geo"] = df_alvo["microrregiao_norm"].isin(df_geo["microrregiao_norm"])

# Mostrar resultado
print("\n🔍 Verificação de microrregiões no MongoDB (ibge_microrregioes_2015):\n")
print(df_alvo[["NO_MUNICIPIO", "MICRORREGIAO", "microrregiao_norm", "existe_na_geo"]].to_string(index=False))

# Fechar conexão
client.close()

