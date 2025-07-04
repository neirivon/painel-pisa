from pymongo import MongoClient
from pathlib import Path
from datetime import datetime

# Conexão segura com MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["metadados_relatorios_ia_html"]

# Caminho dos relatórios gerados
output_dir = Path("avaliacoes_ia")
arquivos_html = sorted(output_dir.glob("prompt_ia_dimensao_*.html"))

docs = []
for arquivo in arquivos_html:
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
        resumo = " ".join(conteudo.split()[:30])  # Primeiras 30 palavras
    
    doc = {
        "nome_arquivo": arquivo.name,
        "caminho": str(arquivo.resolve()),
        "data_criacao": datetime.utcnow().isoformat(),
        "resumo_inicio": resumo
    }
    docs.append(doc)

if docs:
    resultado = colecao.insert_many(docs)
    print(f"✅ {len(resultado.inserted_ids)} metadados inseridos com sucesso.")
else:
    print("⚠️ Nenhum arquivo HTML encontrado para processar.")

# Encerrando conexão
client.close()

