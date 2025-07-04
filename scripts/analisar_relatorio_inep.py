from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# analisar_relatorio_inep.py

from pymongo import MongoClient
from transformers import pipeline
import uuid
import time

# === Conexão com MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_origem = db["relatorio_inep_pisa_2000"]
colecao_destino = db["relatorio_inep_pisa_2000_analise"]

# === Pipeline zero-shot com BERT ===
print("🧠 Carregando modelo BERT (zero-shot)...")
classifier = pipeline("zero-shot-classification", model="facebooos.path.join(k, "b")art-large-mnli")

# === Categorias ===
bloom_labels = ["Lembrar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar"]
metodologias = ["Aula invertida", "Círculo de leitura", "Estudo de caso", "Projeto interdisciplinar"]
perfis = ["Lógico-matemático", "Verbal-linguístico", "Visual-espacial", "Cinestésico", "Interpessoal", "Intrapessoal"]

# === Função de análise ===
def analisar_texto(texto):
    resultado_bloom = classifier(texto, bloom_labels)
    resultado_metodo = classifier(texto, metodologias)
    resultado_perfil = classifier(texto, perfis)

    bloom = resultado_bloom["labels"][0]
    metodologia = resultado_metodo["labels"][0]
    perfil = resultado_perfil["labels"][0]

    rubrica = f"Competência cognitiva relacionada ao nível '{bloom}' está pouco desenvolvida no trecho analisado."

    return {
        "taxonomia_bloom": bloom,
        "rubrica_avaliativa": rubrica,
        "metodologia_sugerida": metodologia,
        "perfil_neuropsicopedagogico": perfil
    }

# === Análise do Relatório INEP 2000 ===
print("🚀 Iniciando análise do relatório INEP 2000...")
documentos = colecao_origem.find({"ano": 2000})
total_armazenados = 0
total_textos = 0

for doc in documentos:
    for secao in doc.get("secoes", []):
        nome_secao = secao.get("secao")
        print(f"\n📂 Seção: {nome_secao}")
        for i, elemento in enumerate(secao.get("elementos", [])):
            if elemento.get("tipo") == "texto":
                texto = elemento.get("conteudo", "").strip()
                if texto:
                    total_textos += 1
                    trecho_curto = texto[:60].replace("\n", " ")
                    print(f"  📄 [{total_textos}] Parágrafo {i+1}: {trecho_curto}...")
                    analise = analisar_texto(texto)
                    colecao_destino.insert_one({
                        "edicao": "2000",
                        "secao": nome_secao,
                        "paragrafo_original": texto,
                        "analise": analise,
                        "uuid": str(uuid.uuid4())
                    })
                    total_armazenados += 1
                    time.sleep(0.2)

print(f"\n✅ Análise concluída.")
print(f"📊 Total de parágrafos processados: {total_textos}")
print(f"📁 Total de análises armazenadas: {total_armazenados}")

client.close()  # <- encerramento seguro da conexão
# === TODO: Triangulação com SAEB ===
# Posteriormente, cruzar os níveis Bloom e rubricas desta análise
# com os resultados das coleções do banco SAEB.

