import json
import os
from datetime import datetime
from bson import ObjectId
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo
import ollama
import pandas as pd

# Suprimir warning de socket não fechado do Ollama
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed <socket.socket")

# ============ CONFIGURAÇÕES ============
NOME_BANCO = "relatorios_inep"
COLECAO_ORIGEM = "relatorio_completo_inep_2022"
ARQUIVO_JSON = "dados_processados/relatorios_completos/inferencias_globais_inep2022.json"
ARQUIVO_CSV = "dados_processados/relatorios_completos/inferencias_globais_inep2022.csv"
MODELO_IA = "llama3"

# ============ CONECTAR AO MONGO ============
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[COLECAO_ORIGEM]

# ============ RECUPERAR DOCUMENTO ============
documento = colecao.find_one()
texto = documento["texto_mesclado_ia"]

print("🧠 Enviando texto completo para inferência global com Rubrica SINAPSE expandida...")

# ============ PROMPT COMPLETO ============

prompt = f"""
Você é um especialista em avaliação educacional, com domínio em Taxonomia de Bloom, Rubrica SINAPSE, Taxonomia SOLO, neuropsicopedagogia, metodologias ativas, PRISMA 2020 e BNCC.

Analise o texto abaixo, que representa a versão mesclada de um relatório técnico do INEP sobre o PISA 2022. Retorne um parecer global estruturado, cobrindo os seguintes 10 aspectos:

1. Nível da Taxonomia de Bloom predominante
2. Polaridade geral do sentimento
3. Rubrica SINAPSE Global (Dimensão + Nível)
4. Avaliação da estrutura segundo a PRISMA 2020
5. Taxonomia SOLO Global
6. Coerência textual e fluidez
7. Frases com tom inadequado ou conversacional
8. Perfil neuropsicopedagógico dominante
9. Metodologia ativa recomendada
10. Alinhamento com a BNCC (quando aplicável)

Texto a ser analisado:
{texto}
"""

# ============ INFERÊNCIA COM LLaMA3 ============
resposta = ollama.chat(model=MODELO_IA, messages=[{"role": "user", "content": prompt}])
conteudo = resposta["message"]["content"]
print("✅ Inferência completada.")

# ============ PREPARAR DADOS PARA ATUALIZAÇÃO ============
inferencias = {
    "inferencias_gerais": conteudo,
    "modelo_ia_inferencia": MODELO_IA,
    "data_inferencia": datetime.now().isoformat()
}

# ============ ATUALIZAR NO MONGODB ============
colecao.update_one(
    { "_id": documento["_id"] },
    { "$set": inferencias }
)
print("🗃️ Documento atualizado no MongoDB com inferências globais completas.")

# ============ EXPORTAR PARA JSON ============
os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
documento_exportado = {**documento, **inferencias}
documento_exportado["_id"] = str(documento_exportado["_id"])  # ObjectId para string

with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(documento_exportado, f, ensure_ascii=False, indent=2)
print(f"📁 JSON salvo em: {ARQUIVO_JSON}")

# ============ EXPORTAR PARA CSV ============
df = pd.DataFrame([{
    "ano": documento_exportado["ano"],
    "titulo": documento_exportado["titulo"],
    "modelo_ia_inferencia": documento_exportado["modelo_ia_inferencia"],
    "inferencias_gerais": documento_exportado["inferencias_gerais"]
}])
df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")
print(f"📁 CSV salvo em: {ARQUIVO_CSV}")

# ============ FINALIZAR ============
client.close()
print("✅ Processo de inferência com Rubrica SINAPSE Global finalizado com sucesso.")

