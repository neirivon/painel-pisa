import json
from fpdf import FPDF
import os
from datetime import datetime

# Caminho para o JSON com as questões
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"

# Caminho para a fonte TTF DejaVuSans
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Pasta de saída dos PDFs
OUTPUT_DIR = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Nome do PDF com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
PDF_PATH = os.path.join(OUTPUT_DIR, f"gabarito_professor_{timestamp}.pdf")

# Classe PDF com cabeçalho personalizado
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Gabarito Pedagógico - Prova PISA adaptada ao TMAP", ln=True, align="C")
        self.ln(5)

# Criação do PDF
pdf = PDF()
pdf.add_font("DejaVu", fname=FONT_PATH)
pdf.add_font("DejaVu", style="B", fname=FONT_PATH)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("DejaVu", size=12)

# Carrega as questões
with open(JSON_PATH, "r", encoding="utf-8") as f:
    questoes = json.load(f)

# Adiciona conteúdo
for idx, questao in enumerate(questoes, 1):
    pdf.set_font("DejaVu", "B", 12)
    pdf.multi_cell(0, 8, f"{idx}. [{questao['disciplina']}] {questao['pergunta_tmap']}")
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(0, 8, f"✔ Gabarito / Resposta Modelo:\n{questao['resposta_modelo']}")
    pdf.ln(5)

# Salva PDF
pdf.output(PDF_PATH)
print(f"✅ PDF gerado com sucesso: {PDF_PATH}")

