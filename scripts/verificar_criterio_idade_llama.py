from pymongo import MongoClient
from datetime import datetime
import ollama

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
colecao_saida = db["pisa_criterios_idade_validados"]

pergunta = (
    "Este texto confirma que o critério de seleção dos estudantes do PISA "
    "é ter 15 anos completos até o dia 1º de maio do ano da aplicação? "
    "Responda apenas com: CONFIRMA, NEGA ou IRRELEVANTE."
)

colecoes = db.list_collection_names()
total_confirmados = 0

for nome_col in colecoes:
    colecao = db[nome_col]
    print(f"🔍 Verificando coleção: {nome_col}")
    
    for doc in colecao.find({}, {"texto": 1, "nome": 1, "arquivo": 1, "file": 1, "pagina": 1, "page": 1, "n_page": 1}):
        if "texto" not in doc:
            continue

        texto = doc["texto"]
        trecho_analisado = texto.strip()[:3000]

        # Construção do prompt
        prompt_llama = f"{pergunta}\n\nTEXTO:\n{trecho_analisado}"

        try:
            resposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt_llama}])
            conteudo = resposta["message"]["content"].strip().upper()

            # Verifica se confirmou
            if "CONFIRMA" in conteudo:
                total_confirmados += 1
                print(f"✅ Confirmação em {nome_col} | Doc: {doc.get('nome') or doc.get('arquivo') or doc.get('file')}")

                # Tentativa de extração de nome do documento e página
                nome_doc = doc.get("nome") or doc.get("arquivo") or doc.get("file", "desconhecido")
                pagina = doc.get("pagina") or doc.get("page") or doc.get("n_page", "desconhecida")

                colecao_saida.insert_one({
                    "colecao_origem": nome_col,
                    "documento_id": str(doc["_id"]),
                    "nome_documento": nome_doc,
                    "pagina": pagina,
                    "resposta_llama": conteudo,
                    "texto_analisado": trecho_analisado,
                    "timestamp": datetime.now()
                })

        except Exception as e:
            print(f"⚠️ Erro com documento {doc.get('_id', '?')}: {e}")

# Finalização
client.close()
print(f"✅ Conexão com MongoDB encerrada.")
print(f"📊 Total de confirmações registradas: {total_confirmados}")

