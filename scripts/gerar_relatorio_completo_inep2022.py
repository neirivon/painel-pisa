import os
import json
from datetime import datetime
import pandas as pd
from bson import ObjectId
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo
import ollama
from tqdm import tqdm

# ============ CONFIGURAÇÕES ============
NOME_BANCO_ORIGEM = "relatorios_inep"
COLECAO_PARAGRAFOS = "inep_2022"
COLECAO_RELATORIO = "relatorio_completo_inep_2022"
MODELO_IA = "llama3"

DIRETORIO_SAIDA = "dados_processados/relatorios_completos"
ARQUIVO_JSON = os.path.join(DIRETORIO_SAIDA, "relatorio_completo_inep_2022.json")
ARQUIVO_CSV = os.path.join(DIRETORIO_SAIDA, "relatorio_completo_inep_2022.csv")

# ============ CONEXÃO COM MONGODB ============
db, client = conectar_mongo(nome_banco=NOME_BANCO_ORIGEM)
colecao_paragrafos = db[COLECAO_PARAGRAFOS]
colecao_relatorio = db[COLECAO_RELATORIO]

# ============ BUSCAR PARÁGRAFOS ============
print("🔍 Coletando parágrafos...")
paragrafos = list(colecao_paragrafos.find({ "erro": None }).sort("ordem", 1))
texto_original = "\n\n".join([p["paragrafo"] for p in paragrafos])
print(f"✅ Total de parágrafos: {len(paragrafos)}")

# ============ GERAÇÃO COM IA ROBUSTA ============
print(f"🧠 Gerando texto mesclado com o modelo {MODELO_IA}...")
prompt = f"""
Você receberá trechos segmentados de um relatório técnico do INEP relacionado ao PISA 2022.
Sua tarefa é unificar todos os parágrafos em um único texto coeso, mantendo o sentido, a estrutura e a linguagem formal.

Evite repetir frases, conecte ideias e melhore a fluidez. Mantenha fidelidade ao conteúdo.
Parágrafos a serem mesclados:
{texto_original}
"""

resposta = ollama.chat(model=MODELO_IA, messages=[{"role": "user", "content": prompt}])
texto_mesclado = resposta["message"]["content"].strip()
print("✅ Texto mesclado gerado.")

# ============ MONTAGEM DO DOCUMENTO ============
documento = {
    "ano": 2022,
    "titulo": "Relatório INEP — PISA 2022 (Texto Mesclado)",
    "texto_original": texto_original,
    "texto_mesclado_ia": texto_mesclado,
    "modelo_usado": MODELO_IA,
    "data_processamento": datetime.now().isoformat(),
    "quantidade_paragrafos": len(paragrafos)
}

# ============ INSERIR NO MONGODB ============
colecao_relatorio.delete_many({})  # Limpeza anterior
colecao_relatorio.insert_one(documento)
print("🗃️ Documento salvo no MongoDB em 'relatorio_completo_inep_2022'.")

try:
    # =====================
    # EXPORTAR PARA JSON
    # =====================
    os.makedirs(DIRETORIO_SAIDA, exist_ok=True)
    documento_serializavel = {k: str(v) if isinstance(v, ObjectId) else v for k, v in documento.items()}
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(documento_serializavel, f, ensure_ascii=False, indent=2)
    print(f"📁 JSON salvo em: {ARQUIVO_JSON}")

    # =====================
    # EXPORTAR PARA CSV
    # =====================
    df = pd.DataFrame([{
        "ano": documento["ano"],
        "titulo": documento["titulo"],
        "modelo_usado": documento["modelo_usado"],
        "texto_mesclado_ia": documento["texto_mesclado_ia"]
    }])
    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")
    print(f"📁 CSV salvo em: {ARQUIVO_CSV}")

finally:
    client.close()
    print("✅ Conexão com MongoDB encerrada.")
