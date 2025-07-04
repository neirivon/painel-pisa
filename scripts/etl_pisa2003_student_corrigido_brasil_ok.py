# etl_pisa2003_student_corrigido_brasil_ok.py

import pandas as pd
from pymongo import MongoClient

# --- Função para conexão MongoDB ---
def conectar_mongo():
    uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
    client = MongoClient(uri)
    db = client["pisa"]
    return db

# --- Parâmetros do arquivo ---
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

# --- Definindo colunas fixas (baseado no Manual SPSS PISA 2003) ---
colspecs = [
    (3, 6),      # CNT (País) -> posição 4 a 6 (lembrando índice começa do 0)
    (359, 365),  # PV1READ -> posição 360 a 365
    (659, 665),  # PV1MATH -> posição 660 a 665
    (959, 965),  # PV1SCIE -> posição 960 a 965
    (1135, 1145) # W_FSTUWT -> posição 1136 a 1145
]

nomes_colunas = ["CNT", "PV1READ", "PV1MATH", "PV1SCIE", "W_FSTUWT"]

# --- Leitura do arquivo ---
print("⏳ Lendo o arquivo com colunas fixas...")
df = pd.read_fwf(CAMINHO_ARQUIVO, colspecs=colspecs, names=nomes_colunas)

# --- Limpeza dos dados ---
print("🧹 Limpando dados...")
df["CNT"] = df["CNT"].str.strip()  # Tirar espaços
df = df.dropna(subset=["CNT", "PV1READ", "PV1MATH", "PV1SCIE"])  # Manter apenas registros válidos

# --- Conversão de tipos ---
for col in ["PV1READ", "PV1MATH", "PV1SCIE", "W_FSTUWT"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Remover registros inválidos ---
df = df.dropna(subset=["W_FSTUWT"])  # Peso amostral é obrigatório

# --- Conexão MongoDB ---
db = conectar_mongo()

# --- Limpar coleção ---
print("🗑️ Limpando coleção antiga...")
db.pisa2003_student.delete_many({})

# --- Inserção dos novos dados ---
print("📤 Inserindo dados corretos...")
db.pisa2003_student.insert_many(df.to_dict(orient="records"))

client.close()
print(f"✅ {len(df)} documentos inseridos com sucesso!")
print("🏁 ETL finalizado!")

