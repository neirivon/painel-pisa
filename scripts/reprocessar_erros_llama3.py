# scripts/reprocessar_erros_llama3.py

import json
import time
from tqdm import tqdm
import ollama
from bson import ObjectId
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

# ================== CONFIGURAÇÕES =====================
NOME_COLECAO = "inep_2022"
NOME_BANCO = "relatorios_inep"
MODELO_IA = "llama3"
ESPERAR_JSON = False  # Defina como True se a IA sempre retornar JSON estruturado

# ================== CONEXÃO MONGODB ===================
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

# ================== CONSULTA ==========================
documentos_com_erro = list(colecao.find({ "erro": { "$exists": True, "$ne": None } }))
print(f"🔁 Total de documentos com erro a reprocessar: {len(documentos_com_erro)}")

# ================== LOOP DE REPROCESSAMENTO ============
for doc in tqdm(documentos_com_erro, desc="🔁 Reprocessando parágrafos com erro"):
    _id = doc["_id"]
    paragrafo = doc.get("paragrafo", "").replace("\f", " ").replace("\n", " ").replace("\xa0", " ").strip()

    prompt = (
        "Analise o seguinte parágrafo e identifique:\n"
        "1. O nível da Taxonomia de Bloom mais provável;\n"
        "2. A polaridade do sentimento predominante;\n"
        "3. A dimensão e nível da Rubrica SINAPSE;\n"
        "4. As palavras-chave principais.\n\n"
        f"Texto:\n{json.dumps(paragrafo, ensure_ascii=False)}"
    )

    try:
        resposta = ollama.chat(model=MODELO_IA, messages=[{ "role": "user", "content": prompt }])
        conteudo = resposta.get("message", {}).get("content", "").strip()

        if not conteudo:
            raise ValueError("Resposta vazia da IA")

        if ESPERAR_JSON:
            try:
                analisado = json.loads(conteudo)
                colecao.update_one(
                    { "_id": ObjectId(_id) },
                    { "$set": { "resposta": analisado, "erro": None } }
                )
            except json.JSONDecodeError as e:
                colecao.update_one(
                    { "_id": ObjectId(_id) },
                    { "$set": { "erro": f"Erro ao decodificar JSON: {str(e)}" } }
                )
        else:
            colecao.update_one(
                { "_id": ObjectId(_id) },
                { "$set": { "resposta": conteudo, "erro": None } }
            )

    except Exception as e:
        colecao.update_one(
            { "_id": ObjectId(_id) },
            { "$set": { "erro": str(e) } }
        )
        time.sleep(1)  # Evita overload no Ollama local

client.close()
print("✅ Reprocessamento finalizado.")

