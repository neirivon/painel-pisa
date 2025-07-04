from fpdf import FPDF
from fpdf.enums import XPos, YPos
import json
import os

# Caminho dos arquivos
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
PDF_DIR = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/"
PDF_PATH = os.path.join(PDF_DIR, "gabarito_professor_moderno.pdf")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

os.makedirs(PDF_DIR, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", style="B", size=14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, "Gabarito Pedagógico para Correção - Prova PISA/TMAP",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(4)

# Inicia PDF
pdf = PDF()
pdf.add_font("DejaVu", "", FONT_PATH)       # Regular
pdf.add_font("DejaVu", "B", FONT_PATH)      # Bold
pdf.add_font("DejaVu", "I", FONT_PATH)      # Italic
pdf.add_page()
pdf.set_font("DejaVu", size=11)

# Cores por disciplina
disciplinas_cores = {
    "Leitura": (70, 130, 180),
    "Matemática": (34, 139, 34),
    "Ciências": (123, 104, 238)
}

# Emojis por disciplina
disciplinas_emojis = {
    "Leitura": "📖",
    "Matemática": "🧮",
    "Ciências": "🔬"
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    questoes = json.load(f)

for idx, q in enumerate(questoes, 1):
    disciplina = q.get("disciplina", "")
    cor = disciplinas_cores.get(disciplina, (0, 0, 0))
    emoji = disciplinas_emojis.get(disciplina, "❓")

    pdf.set_text_color(*cor)
    pdf.set_font("DejaVu", style="B", size=12)
    pdf.cell(0, 10, f"{emoji} Questão {idx} — {disciplina}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("DejaVu", style="", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, f"🔸 Pergunta Original:\n{q['pergunta_original']}")
    pdf.ln(1)
    pdf.multi_cell(0, 7, f"🔹 Pergunta Adaptada ao TMAP:\n{q['pergunta_adaptada_tmap']}")
    pdf.ln(1)
    pdf.set_text_color(0, 102, 0)
    pdf.multi_cell(0, 7, f"✅ Resposta Modelo:\n{q['resposta_modelo']}")
    pdf.ln(2)
    pdf.set_text_color(90, 90, 90)
    pdf.set_font("DejaVu", style="I", size=10)
    pdf.cell(0, 6, f"📚 Fonte: {q['fonte']} | Versão: {q['versao']}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

# Salva PDF
try:
    pdf.output(PDF_PATH)
    print(f"✅ PDF moderno gerado com sucesso em: {PDF_PATH}")
except Exception as e:
    print(f"❌ Erro ao gerar o PDF: {e}")

