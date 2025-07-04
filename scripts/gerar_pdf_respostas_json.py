# scripts/gerar_pdf_respostas_json.py

from fpdf import FPDF
import json
import os

# Diretórios base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # scripts/
PROJETO_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))         # raiz do projeto PISA/
PDF_DIR = os.path.join(PROJETO_DIR, "painel_pisa", "pdfs_correcoes")
os.makedirs(PDF_DIR, exist_ok=True)

RUBRICA_DIMENSOES = {
    "Leitura": "Capacidade de Comunicação e Expressão",
    "Matemática": "Raciocínio Lógico e Solução de Problemas",
    "Ciências": "Relacionamento com Saberes Científicos e Culturais"
}

def log(msg):
    print(f"[LOG] {msg}")

def carregar_rubrica():
    caminho = os.path.join(PROJETO_DIR, "rubrica_sinapase_ia_v4.json")
    if not os.path.exists(caminho):
        log(f"❌ Arquivo de rubrica não encontrado: {caminho}")
        return {}
    log(f"📁 Carregando rubrica: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        rubrica = json.load(f)
    return {dim["dimensao"]: dim["niveis"] for dim in rubrica["dimensoes"]}

def gerar_pdf_para_aluno(matricula):
    caminho_json = os.path.join(PROJETO_DIR, "respostas_alunos.json")
    if not os.path.exists(caminho_json):
        log(f"❌ Arquivo respostas_alunos.json não encontrado: {caminho_json}")
        return

    log(f"📁 Lendo respostas do aluno em: {caminho_json}")
    with open(caminho_json, "r", encoding="utf-8") as f:
        alunos = json.load(f)

    aluno = next((a for a in alunos if a["matricula"] == matricula), None)
    if not aluno:
        log(f"❌ Matrícula {matricula} não encontrada no JSON.")
        return

    nome = aluno["nome"]
    respostas = aluno["respostas"]
    log(f"✅ Aluno localizado: {nome} ({matricula})")
    rubricas = carregar_rubrica()

    # Inicia PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Avaliação Individual - Correção com Rubrica SINAPSE IA v1.4", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Aluno: {nome}", ln=True)
    pdf.cell(0, 10, f"Matrícula: {matricula}", ln=True)
    pdf.ln(5)

    for idx, r in enumerate(respostas, start=1):
        disciplina = r["disciplina"]
        pergunta = r["questao"]
        resposta_aluno = r["resposta_aluno"]
        resposta_modelo = r["resposta_modelo"]

        log(f"📚 Processando questão {idx}: {disciplina}")

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{disciplina}", ln=True)

        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, f"Pergunta: {pergunta}")
        pdf.multi_cell(0, 8, f"Resposta do aluno: {resposta_aluno}")
        pdf.multi_cell(0, 8, f"✔️ Resposta esperada: {resposta_modelo}")
        pdf.ln(1)

        dimensao = RUBRICA_DIMENSOES.get(disciplina)
        if dimensao and dimensao in rubricas:
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 8, f"Dimensão da rubrica: {dimensao}", ln=True)
            pdf.set_font("Arial", '', 10)
            for nivel in rubricas[dimensao]:
                linha = f"{nivel['nota']} - {nivel['nome']}: {nivel['descricao']}"
                pdf.multi_cell(0, 6, linha)
            pdf.cell(0, 8, "Correção do professor (nota de 1 a 4): ______", ln=True)
        else:
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 8, "Rubrica não encontrada para esta disciplina.", ln=True)

        pdf.ln(6)

    nome_pdf = f"{nome.replace(' ', '_')}_{matricula}.pdf"
    caminho_pdf = os.path.join(PDF_DIR, nome_pdf)
    pdf.output(caminho_pdf)
    log(f"✅ PDF gerado com sucesso: {caminho_pdf}")

