# scripts/importar_suplemento_tecnico_2023.py

import os
import pandas as pd
import json
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

ARQUIVO_CSV = os.path.expanduser("~/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/microdados_censo_escolar_2023/dados/suplemento_cursos_tecnicos_2023.csv")
ARQUIVO_JSON = "dados_processados/saeb/suplemento_tecnico_2023.json"

NOME_BANCO = "saeb"
NOME_COLECAO = "suplemento_tecnico_2023"

print("📄 Lendo suplemento de cursos técnicos 2023...")
df = pd.read_csv(ARQUIVO_CSV, sep=";", encoding="latin1", low_memory=False)
os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
df.to_json(ARQUIVO_JSON, orient="records", force_ascii=False, indent=2)
print(f"✅ JSON salvo em: {ARQUIVO_JSON}")

if CONFIG.get("USAR_MONGODB"):
    print("📡 Conectando ao MongoDB dockerizado com autenticação...")
    db, client = conectar_mongo(nome_banco=NOME_BANCO)
    colecao = db[NOME_COLECAO]
    print("🧹 Removendo documentos anteriores da coleção (se houver)...")
    colecao.delete_many({})
    print("⬆️ Inserindo novos documentos...")
    colecao.insert_many(df.to_dict(orient="records"))
    print(f"✅ Inserção concluída: {colecao.count_documents({})} registros em {NOME_BANCO}.{NOME_COLECAO}")
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

