from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import pycountry

# Caminho atualizado do arquivo correto
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune2os.path.join(4, "F")inal release versioos.path.join(n, "b")kos.path.join(g, "p")isa2022_ms_bkg_stu_overall_compendium.xlsx"

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2022_resumo_paises"]

# Ler o arquivo Excel
df = pd.read_excel(CAMINHO_ARQUIVO)

# Selecionar apenas colunas relevantes (verificadas dinamicamente)
colunas_esperadas = ["CNT", "PV1MATH", "PV1READ", "PV1SCIE", "ESCS"]
colunas_presentes = [col for col in colunas_esperadas if col in df.columns]
df = df[colunas_presentes]

# Renomear colunas para clareza
df.rename(columns={
    "CNT": "codigo",
    "PV1MATH": "matematica",
    "PV1READ": "leitura",
    "PV1SCIE": "ciencias",
    "ESCS": "escs"
}, inplace=True)

# Adicionar nome do país (com fallback "Desconhecido")
df["pais"] = df["codigo"].apply(lambda cod: pycountry.countries.get(alpha_3=cod.upper()).name if pycountry.countries.get(alpha_3=cod.upper()) else "Desconhecido")

# Criar documentos para o MongoDB
documentos = []
for _, row in df.iterrows():
    doc = {
        "codigo": row["codigo"],
        "pais": row["pais"],
        "ano": 2022,
        "pontuacoes": {
            "matematica": row.get("matematica"),
            "leitura": row.get("leitura"),
            "ciencias": row.get("ciencias"),
            "escs": row.get("escs")
        }
    }
    documentos.append(doc)

# Inserir no banco de dados
colecao.delete_many({})
colecao.insert_many(documentos)
client.close()

print(f"✅ Importação concluída: {len(documentos)} países com dados agregados inseridos.")

