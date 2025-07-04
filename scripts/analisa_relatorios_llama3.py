from pymongo import MongoClient
from datetime import datetime
import ollama

# Configurações
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DATABASE_NAME = "pisa"
COLECOES_ALVO = [
    "relatorio_inep_pisa_2000"
]
BATCH_SIZE = 20

def analisar_com_llama3(texto):
    try:
        resposta = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um avaliador pedagógico com base na Rubrica SINAPSE IA versão 1.5. Analise o texto abaixo e retorne a dimensão mais provável, nível da Taxonomia de Bloom, metodologia ativa sugerida e referências educacionais se houver."
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )
        return resposta["message"]["content"]
    except Exception as e:
        print(f"❌ Erro na análise com LLAMA3: {e}")
        return None

def main():
    cliente = MongoClient(MONGO_URI)
    db = cliente[DATABASE_NAME]
    destino = db["analise_rubrica_sinapse_ia_v1_5"]

    for colecao_nome in COLECOES_ALVO:
        print(f"🔍 Analisando coleção: {colecao_nome}")
        colecao = db[colecao_nome]

        offset = 0
        total = colecao.count_documents({})
        print(f"🔢 Total de documentos em {colecao_nome}: {total}")

        while offset < total:
            documentos = colecao.find().skip(offset).limit(BATCH_SIZE)
            for doc in documentos:
                texto = (
                    doc.get("texto") or
                    doc.get("paragrafo") or
                    doc.get("content") or
                    doc.get("pagina") or
                    None
                )

                if not texto or len(str(texto).strip()) < 100:
                    continue

                resultado = analisar_com_llama3(str(texto))

                if resultado:
                    entrada = {
                        "colecao_origem": colecao_nome,
                        "ano": 2000,
                        "pagina": doc.get("pagina", None),
                        "texto_original": str(texto).strip(),
                        "analise_llama3": resultado,
                        "dimensao_sugerida": None,
                        "nivel_taxonomia_bloom": None,
                        "metodologia_ativa_sugerida": None,
                        "referencias_detectadas": [],
                        "timestamp": datetime.utcnow()
                    }

                    destino.insert_one(entrada)

            offset += BATCH_SIZE
            print(f"✅ Processados {min(offset, total)} de {total} documentos")

        print(f"✅ Fim da análise da coleção: {colecao_nome}")

    cliente.close()

if __name__ == "__main__":
    main()

