import json
import requests
from datetime import datetime
from pymongo import MongoClient
from pathlib import Path

# === CONFIGURAÇÕES ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
DB_PISA = "pisa"
DB_SAEB = "saeb"
DB_RELAT = "relatorios_inep"
COL_PISA = "pisa_2022_student_qqq"
COL_SAEB = "saeb_2021_municipios_9ano"
COL_RELAT_SAEB = "saeb_relatorios_2021"
COL_RELAT_PISA = "relatorio_inep_2022"
COL_RAR = "rubrica_avaliativa_rubricas"
ARQ_RUBRICA = "/home/neirivon/Downloads/rubrica_sinapse_ia_v1_5.json"
ARQUIVO_SAIDA = f"avaliacao_hibrida_llama3_v1_5_" + datetime.now().strftime("%Y%m%d_%H%M") + ".txt"

# === FUNÇÃO DE LOG ===
def registrar_log(msg):
    hora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{hora} {msg}")

# === CHAMADA AO OLLAMA ===
def analisar_com_ollama(prompt: str, modelo="llama3"):
    url = "http://localhost:11434/api/generate"
    payload = {"model": modelo, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception as e:
        return f"[ERRO IA] {e}"

# === CARREGAMENTO DOS DADOS ===
def carregar_dados():
    registrar_log("📥 Conectando ao MongoDB...")
    client = MongoClient(MONGO_URI)
    try:
        db_pisa = client[DB_PISA]
        db_saeb = client[DB_SAEB]
        db_rel = client[DB_RELAT]
        db_rub = client["rubricas"]

        alunos_pisa = list(db_pisa[COL_PISA].find({"CNT": "BRA"}, {"PV1READ": 1, "PV1MATH": 1, "PV1SCIE": 1, "_id": 0}))
        municipios_saeb = list(db_saeb[COL_SAEB].find({}, {"nota_geral": 1, "nivel_lp": 1, "nivel_mat": 1, "_id": 0}))
        textos_saeb = " ".join([d.get("texto", "") for d in db_saeb[COL_RELAT_SAEB].find({}, {"texto": 1, "_id": 0})])
        textos_pisa = " ".join([d.get("texto", "") for d in db_rel[COL_RELAT_PISA].find({}, {"texto": 1, "_id": 0})])
        criterios_rar = list(db_rub[COL_RAR].find().sort("numero", 1))

        with open(ARQ_RUBRICA, encoding="utf-8") as f:
            rubrica = json.load(f)[0]  # assume array com um único elemento

        registrar_log(f"✅ {len(alunos_pisa)} alunos PISA | {len(municipios_saeb)} municípios SAEB | {len(criterios_rar)} critérios RAR")
        return alunos_pisa, municipios_saeb, criterios_rar, rubrica["dimensoes"], textos_saeb + "\n" + textos_pisa

    finally:
        client.close()

# === GERA CONTEXTO DE TRIANGULAÇÃO ===
def gerar_contexto(dim, alunos_pisa, municipios_saeb):
    media_pisa = {k: round(sum(a.get(k, 0) or 0 for a in alunos_pisa)/len(alunos_pisa), 1) for k in ["PV1READ", "PV1MATH", "PV1SCIE"]}
    media_saeb = round(sum(m.get("nota_geral", 0) or 0 for m in municipios_saeb) / len(municipios_saeb), 1)
    contexto = f"📊 SAEB 2021: {media_saeb} | PISA 2022 → Leitura: {media_pisa['PV1READ']} | Matemática: {media_pisa['PV1MATH']} | Ciências: {media_pisa['PV1SCIE']}"
    return contexto

# === AVALIAÇÃO COMPLETA ===
def executar_avaliacao():
    registrar_log("🔍 Iniciando avaliação híbrida da Rubrica SINAPSE IA v1.5...")
    alunos, saeb, criterios, dimensoes, relatorios = carregar_dados()
    linhas = []

    for idx, dim in enumerate(dimensoes, start=1):
        titulo = dim["dimensao"]
        descritores = "\n".join([f"{n['nota']} - {n['nome']}: {n['descricao']}" for n in dim["niveis"]])
        exemplos = "\n".join(dim.get("exemplos", []))
        contexto = gerar_contexto(titulo, alunos, saeb)

        for crit in criterios:
            nome_criterio = crit["dimensao"]
            niveis_rar = "\n".join([f"{i+1} - {crit[f'nivel_{i+1}']}" for i in range(4)])
            prompt = f"""
Você é um avaliador especialista em rubricas educacionais.
Avalie a dimensão: **{titulo}**

📚 Descritores:
{descritores}

🎯 Exemplos:
{exemplos}

📊 Dados reais:
{contexto}

📄 Trechos de relatórios SAEB/PISA:
{relatorios[:2000]} [...]

🧩 Critério RAR: {nome_criterio}
{niveis_rar}

📝 Tarefa:
1. Atribua uma nota de 1 a 4.
2. Justifique com base nos dados e descritores.
3. Sugira melhorias.
4. Fundamente em autores ou documentos.
"""
            registrar_log(f"🧠 Avaliando: {titulo} → {nome_criterio}...")
            resposta = analisar_com_ollama(prompt)
            bloco = f"\n=== {idx}. {titulo.upper()} | Critério: {nome_criterio} ===\n{resposta}\n"
            linhas.append(bloco)
            registrar_log("✔️ Concluído.")

    Path(ARQUIVO_SAIDA).write_text("\n".join(linhas), encoding="utf-8")
    registrar_log(f"✅ Avaliação salva em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    executar_avaliacao()

