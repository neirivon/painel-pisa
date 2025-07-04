from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import pycountry

# === Caminhos dos arquivos Excel ===
CAMINHO_MAT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_coos.path.join(g, "p")isa2022_ms_cog_overall_math_compendium.xlsx"
CAMINHO_READ = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_coos.path.join(g, "p")isa2022_ms_cog_overall_read_compendium.xlsx"
CAMINHO_SCIE = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_coos.path.join(g, "p")isa2022_ms_cog_overall_scie_compendium.xlsx"

# === Leitura dos arquivos ===
df_mat = pd.read_excel(CAMINHO_MAT)
df_read = pd.read_excel(CAMINHO_READ)
df_scie = pd.read_excel(CAMINHO_SCIE)

# === Padronizar colunas ===
df_mat = df_mat.rename(columns={"CNT": "codigo", "Mean score": "matematica"})
df_read = df_read.rename(columns={"CNT": "codigo", "Mean score": "leitura"})
df_scie = df_scie.rename(columns={"CNT": "codigo", "Mean score": "ciencias"})

# === Juntar os três dataframes ===
df_merge = df_mat[["codigo", "matematica"]].merge(
    df_read[["codigo", "leitura"]], on="codigo", how="inner"
).merge(
    df_scie[["codigo", "ciencias"]], on="codigo", how="inner"
)

# === Adicionar nome do país ===
def obter_nome_pais(codigo):
    pais = pycountry.countries.get(alpha_3=codigo.upper())
    return pais.name if pais else "Desconhecido"

df_merge["pais"] = df_merge["codigo"].apply(obter_nome_pais)

# === Conectar ao MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

# === Inserir no MongoDB ===
colecao = db["pisa_ocde_2022_medias_resumo"]
colecao.delete_many({})
colecao.insert_many(df_merge.to_dict(orient="records"))

client.close()
print(f"✅ Importação concluída com sucesso: {len(df_merge)} países inseridos.")

