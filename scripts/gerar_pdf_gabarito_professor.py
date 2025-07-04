import json
from fpdf import FPDF
from datetime import datetime
import os

# Caminhos absolutos
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor.pdf"

# Classe PDF com cabeçalho
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "GABARITO DO PROFESSOR — QUESTÕES ADAPTADAS AO TMAP", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, num, disciplina):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0)
        self.cell(0, 10, f"🔢 Questão {num} – {disciplina}", ln=True)
        self.ln(2)

    def chapter_body(self, pergunta, resposta_modelo):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"📘 Pergunta Adaptada:\n{pergunta}")
        self.ln(1)
        self.set_font("Arial", "I", 11)
        self.multi_cell(0, 8, f"✅ Resposta Esperada:\n{resposta_modelo}")
        self.ln(8)

def carregar_questoes():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Corrigir se vier como lista de strings JSON
    if isinstance(dados, list) and isinstance(dados[0], str):
        print("⚠️ Corrigindo: convertendo lista de strings para lista de dicionários.")
        dados = [json.loads(q) for q in dados if q.strip().startswith("{")]

    return dados

def gerar_pdf(questoes):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for idx, q in enumerate(questoes, start=1):
        pdf.chapter_title(idx, q["disciplina"])
        pdf.chapter_body(q["pergunta_adaptada_tmap"], q.get("resposta_modelo", "❌ Resposta não informada."))

    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
    pdf.output(PDF_PATH)
    print(f"✅ PDF gerado com sucesso em: {PDF_PATH}")

if __name__ == "__main__":
    try:
        questoes = carregar_questoes()
        gerar_pdf(questoes)
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")

