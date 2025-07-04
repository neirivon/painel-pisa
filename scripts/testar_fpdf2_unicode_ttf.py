from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()

# Caminho absoluto para a fonte
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError("Fonte DejaVuSans.ttf não encontrada em /usr/share/fonts/truetype/dejavu/")

# Adiciona a fonte TTF (com suporte a Unicode)
pdf.add_font("DejaVu", fname=FONT_PATH)
pdf.set_font("DejaVu", size=14)

# Teste de linha com emojis e símbolos Unicode
pdf.cell(0, 10, "✅ Teste Unicode com fpdf2: π, √, Ω, 🎓, 📚, ✨", new_x="LMARGIN", new_y="NEXT")

# Salva PDF
pdf.output("/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/teste_fpdf2_unicode_completo.pdf")
print("✅ PDF com Unicode gerado com sucesso.")

