from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import pycountry

# === Conexão MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_destino = db["pisa_ocde_2022_resumo_geral"]

# === Função para carregar e preparar os dados ===
def carregar_medias(caminho, coluna_valor, nova_coluna):
    df = pd.read_excel(caminho)
    df = df.rename(columns={
        df.columns[0]: "codigo",
        df.columns[1]: nova_coluna
    })
    df = df[["codigo", nova_coluna]].dropna()
    df["codigo"] = df["codigo"].str.strip()
    return df

# === Arquivos fonte ===
base_path = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_cog"
arquivo_mat = f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_math_compendium.xlsx"
arquivo_read = f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_read_compendium.xlsx"
arquivo_scie = f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_scie_compendium.xlsx"

# === Carregar os três domínios ===
df_mat = carregar_medias(arquivo_mat, "Mean score", "matematica")
df_read = carregar_medias(arquivo_read, "Mean score", "leitura")
df_scie = carregar_medias(arquivo_scie, "Mean score", "ciencias")

# === Merge dos domínios ===
df_merged = df_mat.merge(df_read, on="codigo").merge(df_scie, on="codigo")

# === Carregar ESCS do Mongo ===
escs_docs = list(db["pisa_ocde_2022_escs_media"].find({}, {"_id": 0}))
df_escs = pd.DataFrame(escs_docs)

# === Merge final com ESCS ===
df_final = df_merged.merge(df_escs, on="codigo", how="inner")

# === Garantir nomes dos países corretos ===
def get_nome_pais(cod):
    pais = pycountry.countries.get(alpha_3=cod)
    return pais.name if pais else "Desconhecido"

df_final["pais"] = df_final["codigo"].apply(get_nome_pais)

# === Inserção no Mongo ===
colecao_destino.delete_many({})
colecao_destino.insert_many(df_final.to_dict(orient="records"))
client.close()

print(f"✅ Importação completa: {len(df_final)} países inseridos em 'pisa_ocde_2022_resumo_geral'.")

