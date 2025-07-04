
import json
import requests
from pymongo import MongoClient
from datetime import datetime
from pathlib import Path

# === CONFIGURAÇÕES ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
DB_PISA = "pisa"
DB_SAEB = "saeb"
DB_RELATORIOS = ["saeb.saeb_relatorios_2021", "relatorios_inep.relatorio_inep_2022"]
COL_PISA = "pisa_2022_student_qqq"
COL_SAEB = "saeb_2021_municipios_9ano"
COL_RAR = "rubrica_avaliativa_rubricas"
COL_RUBRICA = "rubrica_sinapse_ia"
ARQUIVO_SAIDA = f"avaliacao_llama3_triangulacao_hibrida_" + datetime.now().strftime("%Y%m%d_%H%M") + ".txt"

def registrar_log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def analisar_com_ollama(prompt: str, modelo="llama3"):
    url = "http://localhost:11434/api/generate"
    payload = {"model": modelo, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception as e:
        return f"[ERRO IA] {e}"

def carregar_dados():
    registrar_log("📥 Carregando dados do MongoDB...")
    client = MongoClient(MONGO_URI)
    try:
        alunos_pisa = list(client[DB_PISA][COL_PISA].find({"CNT": "BRA"}, {"PV1READ": 1, "PV1MATH": 1, "PV1SCIE": 1, "_id": 0}))
        municipios_saeb = list(client[DB_SAEB][COL_SAEB].find({}, {"nota_geral": 1, "_id": 0}))
        criterios_rar = list(client["rubricas"][COL_RAR].find().sort("numero", 1))
        rubrica_doc = client["rubricas"][COL_RUBRICA].find_one({"versao": "v1.5"})

        textos_relatorios = []
        for banco_colecao in DB_RELATORIOS:
            banco, colecao = banco_colecao.split(".")
            docs = list(client[banco][colecao].find({}, {"texto": 1, "_id": 0}))
            textos_relatorios += [d["texto"] for d in docs if "texto" in d]

        return alunos_pisa, municipios_saeb, criterios_rar, rubrica_doc["dimensoes"], textos_relatorios
    finally:
        client.close()

def gerar_contexto(dim, alunos_pisa, municipios_saeb, relatorios):
    media_pisa = {
        "read": sum(a.get("PV1READ", 0) for a in alunos_pisa) / len(alunos_pisa),
        "math": sum(a.get("PV1MATH", 0) for a in alunos_pisa) / len(alunos_pisa),
        "scie": sum(a.get("PV1SCIE", 0) for a in alunos_pisa) / len(alunos_pisa),
    }
    media_saeb = sum(m.get("nota_geral", 0) for m in municipios_saeb) / len(municipios_saeb)
    relatorio_texto = " ".join(r for r in relatorios if dim.lower() in r.lower() or any(k in r.lower() for k in dim.lower().split()))

    return f"""
📊 Dados Quantitativos:
- Média SAEB 2021: {round(media_saeb, 2)}
- PISA 2022: Leitura={round(media_pisa['read'],2)}, Matemática={round(media_pisa['math'],2)}, Ciências={round(media_pisa['scie'],2)}

📄 Evidência Qualitativa (Relatórios):
{relatorio_texto[:1200]}...
"""

def executar_avaliacao():
    registrar_log("🔍 Iniciando avaliação híbrida da Rubrica SINAPSE IA v1.5...")
    alunos_pisa, municipios_saeb, criterios_rar, rubrica_sinapse, relatorios = carregar_dados()
    linhas_saida = []

    for idx, dim in enumerate(rubrica_sinapse, start=1):
        titulo = dim["dimensao"]
        descritores = "\n".join([f"{n['nota']} - {n['nome']}: {n['descricao']}" for n in dim["niveis"]])
        exemplos = "\n".join(dim.get("exemplos", []))
        contexto = gerar_contexto(titulo, alunos_pisa, municipios_saeb, relatorios)

        for crit in criterios_rar:
            nome_criterio = crit["dimensao"]
            niveis_txt = "\n".join([f"{i+1} - {crit[f'nivel_{i+1}']}" for i in range(4)])
            prompt = f"""Você é um avaliador educacional com base em dados do SAEB, PISA e relatórios do INEP.

Avalie a dimensão: **{titulo}**

🧩 Critério RAR: {nome_criterio}
{niveis_txt}

📚 Descritores:
{descritores}

🌱 Exemplos práticos:
{exemplos}

📈 Triangulação Quantitativa e Qualitativa:
{contexto}

📝 Tarefa:
1. Atribua uma nota de 1 a 4 para a dimensão conforme o critério.
2. Justifique pedagogicamente.
3. Sugira melhorias.
4. Cite bases teóricas que reforcem sua decisão.
"""
            registrar_log(f"✏️ Avaliando dimensão: {titulo} / Critério: {nome_criterio}...")
            resposta = analisar_com_ollama(prompt)
            linhas_saida.append(f"== {titulo} | Critério: {nome_criterio} ==\n{resposta}\n")
            registrar_log("✅ Concluído.")

    Path(ARQUIVO_SAIDA).write_text("\n\n".join(linhas_saida), encoding="utf-8")
    registrar_log(f"📁 Arquivo salvo: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    executar_avaliacao()
