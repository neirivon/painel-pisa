import json
import requests
from datetime import datetime
from pymongo import MongoClient
from pathlib import Path

# === CONFIGURAÇÕES ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
DB_PISA = "pisa"
DB_SAEB = "saeb"
COL_PISA = "pisa_2022_student_qqq"
COL_SAEB = "saeb_2021_municipios_9ano"
COL_RAR = "rubrica_avaliativa_rubricas"
COL_RUBRICA = "rubrica_sinapse_ia"
ARQUIVO_SAIDA = f"avaliacao_completa_llama3_" + datetime.now().strftime("%Y%m%d_%H%M") + ".txt"

# === FUNÇÃO DE LOG ===
def registrar_log(msg):
    hora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{hora} {msg}")

# === CHAMADA À IA LOCAL (OLLAMA + LLAMA3) ===
def analisar_com_ollama(prompt: str, modelo="llama3"):
    url = "http://localhost:11434/api/generate"
    payload = {"model": modelo, "prompt": prompt, "stream": False}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception as e:
        return f"[ERRO IA] {e}"

# === CONECTAR AO MONGODB E CARREGAR DADOS ===
def carregar_dados():
    registrar_log("📥 Conectando ao MongoDB e carregando dados reais...")
    client = MongoClient(MONGO_URI)

    try:
        db_pisa = client[DB_PISA]
        db_saeb = client[DB_SAEB]
        db_rubricas = client["rubricas"]

        alunos_brasil = list(db_pisa[COL_PISA].find(
            {"CNT": "BRA"},
            {"PV1READ": 1, "PV1MATH": 1, "PV1SCIE": 1, "_id": 0}
        ))

        municipios_saeb = list(db_saeb[COL_SAEB].find(
            {},
            {"nota_geral": 1, "nivel_lp": 1, "nivel_mat": 1, "_id": 0}
        ))

        criterios_rar = list(db_rubricas[COL_RAR].find().sort("numero", 1))

        rubrica_doc = db_rubricas[COL_RUBRICA].find_one({"versao": "v1.4"})
        if not rubrica_doc or "dimensoes" not in rubrica_doc:
            raise ValueError("❌ Documento da rubrica v1.4 não encontrado ou mal formatado no MongoDB.")

        rubrica_sinapse = rubrica_doc["dimensoes"]

        registrar_log(f"✅ Dados carregados: {len(alunos_brasil)} alunos PISA | {len(municipios_saeb)} municípios SAEB | {len(criterios_rar)} critérios RAR | {len(rubrica_sinapse)} dimensões na Rubrica")
        return alunos_brasil, municipios_saeb, criterios_rar, rubrica_sinapse

    finally:
        client.close()

# === GERA CONTEXTO PARA TRIANGULAÇÃO ===
def gerar_contexto_triangulacao(dim, alunos_pisa, municipios_saeb):
    media_pisa_read = sum(a.get("PV1READ", 0) or 0 for a in alunos_pisa) / len(alunos_pisa)
    media_pisa_math = sum(a.get("PV1MATH", 0) or 0 for a in alunos_pisa) / len(alunos_pisa)
    media_pisa_scie = sum(a.get("PV1SCIE", 0) or 0 for a in alunos_pisa) / len(alunos_pisa)
    media_saeb = sum(m.get("nota_geral", 0) or 0 for m in municipios_saeb) / len(municipios_saeb)

    if "Cognitiva" in dim:
        return f"O SAEB 2021 apresenta nota média de {round(media_saeb,2)}. No PISA 2022, as médias foram: Leitura={round(media_pisa_read,2)}, Matemática={round(media_pisa_math,2)}, Ciências={round(media_pisa_scie,2)}. Isso aponta fragilidade cognitiva crítica em leitura crítica e resolução de problemas."
    elif "Inclusão" in dim or "Equidade" in dim:
        return "As desigualdades regionais são evidentes no SAEB e PISA, com disparidades significativas de acesso, ESCS e infraestrutura, exigindo rubricas mais sensíveis à equidade."
    else:
        return f"Média geral SAEB: {round(media_saeb,2)} | PISA: L={round(media_pisa_read,2)} M={round(media_pisa_math,2)} C={round(media_pisa_scie,2)}. Use isso como base para contextualizar sua avaliação."

# === EXECUÇÃO PRINCIPAL ===
registrar_log("📑 Carregando rubrica SINAPSE IA v1.4 diretamente do MongoDB...")
alunos_pisa, municipios_saeb, criterios_rar, rubrica_sinapse = carregar_dados()
linhas_saida = []

registrar_log("🚀 Iniciando avaliação completa com triangulação PISA/SAEB + LLAMA3...")

for idx, dim in enumerate(rubrica_sinapse, start=1):
    titulo = dim["dimensao"]
    descritores = "\n".join([f"{n['nota']} - {n['nome']}: {n['descricao']}" for n in dim["niveis"]])
    exemplos = "\n".join(dim.get("exemplos", []))
    contexto = gerar_contexto_triangulacao(titulo, alunos_pisa, municipios_saeb)
    bloco_dim = f"\n=== DIMENSÃO {idx}/{len(rubrica_sinapse)}: {titulo.upper()} ===\n"

    for crit in criterios_rar:
        nome_criterio = crit["dimensao"]
        niveis_txt = "\n".join([f"{i+1} - {crit[f'nivel_{i+1}']}" for i in range(4)])
        prompt = f"""Você é um avaliador educacional especialista.

Avalie a dimensão da Rubrica SINAPSE IA: **{titulo}**

📚 Descritores:
{descritores}

🎯 Exemplos:
{exemplos}

📊 Dados reais do SAEB/PISA:
{contexto}

🧩 Critério RAR: {nome_criterio}
{niveis_txt}

📝 Tarefa:
1. Atribua uma nota de 1 a 4.
2. Justifique com base nos dados reais e descritores.
3. Sugira melhorias.
4. Aponte autores ou teorias de apoio.
"""
        registrar_log(f"🔎 Avaliando {titulo} → {nome_criterio}...")
        resposta = analisar_com_ollama(prompt)
        bloco_dim += f"\n{resposta}\n"
        registrar_log("✔️ Concluído.")

    linhas_saida.append(bloco_dim)

Path(ARQUIVO_SAIDA).write_text("\n".join(linhas_saida), encoding="utf-8")
registrar_log(f"✅ Avaliação final salva em: {ARQUIVO_SAIDA}")
