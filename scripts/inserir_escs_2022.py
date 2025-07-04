import pandas as pd
from pymongo import MongoClient

# Caminho para o CSV
CAMINHO_CSV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/ESC_TRENDS/escs_trend.csv"

# Carregar os dados
df = pd.read_csv(CAMINHO_CSV)

# Filtrar Brasil
df_brasil = df[df["cnt"] == "BRA"]

# Calcular a média do ESCS
media_escs = df_brasil["escs_trend"].mean(skipna=True)
print(f"Média ESCS Brasil 2022: {media_escs:.4f}")

# Conectar ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
col = db["historico_pisa_brasil"]

# Inserir documento
documento = {
    "Ano": 2022,
    "Pais": "Brazil",
    "Variavel": "ESCS",
    "Valor": round(media_escs, 4)
}

# Verificar duplicação
if col.count_documents({"Ano": 2022, "Pais": "Brazil", "Variavel": "ESCS"}) == 0:
    col.insert_one(documento)
    print("✅ Documento inserido com sucesso!")
else:
    print("⚠️ Documento já existe. Nenhuma inserção feita.")

client.close()

