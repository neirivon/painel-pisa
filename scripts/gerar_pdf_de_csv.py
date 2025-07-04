import csv
import os
from fpdf import FPDF
from datetime import datetime

# Caminhos absolutos
CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor_pdf.csv.pdf"

# Classe PDF com cabeçalho e layout melhorado
class PDFGabarito(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 16)
        self.set_text_color(0, 70, 140)
        self.cell(0, 10, "📘 Gabarito Oficial - Prova Adaptada PISA (TMAP)", ln=True, align="C")
        self.ln(5)

    def add_questao(self, idx, disciplina, pergunta, resposta):
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, f"🔢 Questão {idx} - Disciplina: {disciplina}", ln=True)

        self.set_font("Helvetica", '', 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 8, f"❓ Pergunta Adaptada:", ln=True)
        self.set_font("Helvetica", 'I', 11)
        self.multi_cell(0, 8, pergunta)

        self.ln(1)
        self.set_font("Helvetica", '', 11)
        self.multi_cell(0, 8, f"✅ Resposta Esperada:", ln=True)
        self.set_font("Helvetica", 'I', 11)
        self.multi_cell(0, 8, resposta)
        self.ln(5)

# Geração do PDF
try:
    pdf = PDFGabarito()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, 1):
            disciplina = row.get("disciplina", "").strip()
            pergunta = row.get("pergunta_adaptada_tmap", "").strip()
            resposta = row.get("resposta_modelo", "").strip()
            pdf.add_questao(idx, disciplina, pergunta, resposta)

    pdf.output(PDF_PATH)
    print(f"✅ PDF gerado com sucesso: {PDF_PATH}")
except Exception as e:
    print(f"❌ Erro ao gerar PDF: {e}")

