from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

# === Caminho do arquivo Excel ===
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "I")NEos.path.join(P, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune2os.path.join(4, "p")isa2022_ms_bkg_stu_overall_compendium.xlsx"

# === Conexão com MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2022_resumo_paises"]

# === Leitura do Excel ===
df = pd.read_excel(CAMINHO_ARQUIVO)

# === Verificar nomes das colunas disponíveis ===
colunas_esperadas = ["CNT", "PV1MATH", "PV1READ", "PV1SCIE", "ESCS"]
colunas_encontradas = df.columns.tolist()
df = df[[c for c in colunas_esperadas if c in colunas_encontradas]]

# === Renomear colunas ===
df = df.rename(columns={
    "CNT": "codigo",
    "PV1MATH": "matematica",
    "PV1READ": "leitura",
    "PV1SCIE": "ciencias",
    "ESCS": "escs"
})

# === Criar estrutura de documentos para MongoDB ===
documentos = []
for _, row in df.iterrows():
    doc = {
        "codigo": row["codigo"],
        "ano": 2022,
        "pontuacoes": {
            "matematica": row.get("matematica", None),
            "leitura": row.get("leitura", None),
            "ciencias": row.get("ciencias", None),
            "escs": row.get("escs", None)
        }
    }
    documentos.append(doc)

# === Inserir no MongoDB ===
colecao.delete_many({})
colecao.insert_many(documentos)
client.close()

print(f"✅ Importação concluída: {len(documentos)} países com médias inseridos na coleção 'pisa_ocde_2022_resumo_paises'.")

