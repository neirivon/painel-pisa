from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

# Caminho do arquivo
CAMINHO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "D")ADOos.path.join(S, "2")02os.path.join(2, "e")scs_trend.csv"

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2022_escs_media"]

# Leitura do CSV
df = pd.read_csv(CAMINHO, sep=None, engine="python")

# Eliminar registros sem ESCS
df = df.dropna(subset=["escs_trend"])

# Agrupar por país e calcular a média de ESCS
df_media = df.groupby("cnt")["escs_trend"].mean().reset_index()

# Renomear colunas para clareza
df_media.columns = ["codigo", "media_escs"]

# Adicionar nomes dos países (com fallback para "Desconhecido")
import pycountry
def obter_nome_pais(cod):
    try:
        return pycountry.countries.get(alpha_3=cod.upper()).name
    except:
        return "Desconhecido"
df_media["pais"] = df_media["codigo"].apply(obter_nome_pais)

# Converter para dicionário e inserir no MongoDB
registros = df_media.to_dict(orient="records")
colecao.delete_many({})
colecao.insert_many(registros)

client.close()
print(f"✅ Importação finalizada com {len(registros)} países com ESCS.")

