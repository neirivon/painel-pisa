# scripts/importar_saeb2023_9ef.py

import os
import json
import pandas as pd
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

# =====================
# CONFIGURAÇÃO
# =====================
CAMINHO_CSV_ORIGEM = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/DADOS/TS_ALUNO_9EF.csv"
CSV_SAIDA = "dados_processados/saeb/saeb_2023_9ef.csv"
JSON_SAIDA = "dados_processados/saeb/saeb_2023_9ef.json"
NOME_BANCO = "saeb"
NOME_COLECAO = "saeb_2023_9ef"
ANO = 2023

# =====================
# LEITURA DO CSV ORIGINAL
# =====================
print("📄 Lendo arquivo CSV original...")
df = pd.read_csv(CAMINHO_CSV_ORIGEM, sep=";", encoding="latin1", low_memory=False)
df.columns = df.columns.str.strip()
df["ano"] = ANO

# =====================
# SALVAR VERSÃO UTF-8 CSV
# =====================
os.makedirs(os.path.dirname(CSV_SAIDA), exist_ok=True)
df.to_csv(CSV_SAIDA, index=False, encoding="utf-8")
print(f"✅ CSV salvo em: {CSV_SAIDA}")

# =====================
# SALVAR COMO JSON
# =====================
df.to_json(JSON_SAIDA, orient="records", force_ascii=False, indent=2)
print(f"✅ JSON salvo em: {JSON_SAIDA}")

# =====================
# INSERIR NO MONGODB
# =====================
print("📡 Conectando ao MongoDB dockerizado com autenticação...")

try:
    db, client = conectar_mongo(
        nome_banco=NOME_BANCO,
        uri="mongodb://admin:admin123@localhost:27017/?authSource=admin"
    )
    colecao = db[NOME_COLECAO]

    print("🧹 Removendo documentos anteriores da coleção (se houver)...")
    colecao.delete_many({})

    print("⬆️ Inserindo novos documentos...")
    dados = df.to_dict(orient="records")
    colecao.insert_many(dados)
    print(f"✅ Inserção concluída: {len(dados)} registros em {NOME_BANCO}.{NOME_COLECAO}")

finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

