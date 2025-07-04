from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
from transformers import pipeline
import torch

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_origem = db["relatorio_inep_pisa_2000_v2"]
colecao_destino = db["relatorio_inep_pisa_2000_analise_v2"]

# Carregar modelo BERT zero-shot
classifier = pipeline("zero-shot-classification", model="facebooos.path.join(k, "b")art-large-mnli", device=0 if torch.cuda.is_available() else -1)

# Rótulos educacionais (poderão ser expandidos)
labels = ["Crítica à qualidade das escolas", "Desempenho por nível socioeconômico", "Comparação internacional", "Sugestões de política pública"]

# Limpar coleção destino
colecao_destino.drop()

# Processar cada seção
documento = colecao_origem.find_one({"ano": 2000})
total_paragrafos = 0
total_armazenados = 0

for secao in documento.get("secoes", []):
    nome_secao = secao.get("secao", "Sem título")
    for i, elemento in enumerate(secao.get("elementos", [])):
        if elemento.get("tipo") == "texto":
            texto = elemento.get("conteudo", "").strip()
            if not texto:
                continue
            total_paragrafos += 1
            print(f"  📄 [{total_paragrafos}] Parágrafo {i + 1}: {texto[:60].replace(chr(10), ' ')}...")

            resultado = classifier(texto, labels, multi_label=True)
            analise = {
                "ano": 2000,
                "secao": nome_secao,
                "paragrafo": i,
                "texto_original": texto,
                "classificacao": dict(zip(resultado["labels"], resultado["scores"]))
            }
            colecao_destino.insert_one(analise)
            total_armazenados += 1

# Fechar conexão
client.close()

print("\n✅ Análise concluída.")
print(f"📊 Total de parágrafos processados: {total_paragrafos}")
print(f"📁 Total de análises armazenadas: {total_armazenados}")

