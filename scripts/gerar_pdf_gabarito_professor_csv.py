# scripts/gerar_pdf_gabarito_professor_csv.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import cm
import csv
import os

# Caminho absoluto do CSV
CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor.pdf"

# Estilo de parágrafo
styles = getSampleStyleSheet()
style_normal = styles["Normal"]
style_normal.fontName = "Helvetica"
style_normal.fontSize = 12
style_normal.leading = 16
style_normal.alignment = TA_LEFT

# Criação do PDF
doc = SimpleDocTemplate(PDF_PATH, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
story = []

# Título
story.append(Paragraph("🎓 Gabarito das Questões Adaptadas do PISA 2022 para o TMAP", styles["Title"]))
story.append(Spacer(1, 24))

# Carregar CSV e montar blocos
with open(CSV_PATH, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, 1):
        story.append(Paragraph(f"🔢 <b>Questão {idx} — {row['disciplina']}</b>", style_normal))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"📚 <b>Pergunta Original:</b> {row['pergunta_original']}", style_normal))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"🌱 <b>Pergunta Adaptada ao TMAP:</b> {row['pergunta_adaptada_tmap']}", style_normal))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"✅ <b>Resposta Modelo:</b> {row['resposta_modelo']}", style_normal))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"📌 <b>Rubrica:</b> {row['rubrica_pedagogica']}", style_normal))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"🧠 <b>Fonte:</b> {row['fonte']} — {row['ano']}, versão {row['versao']}", style_normal))
        story.append(Spacer(1, 12))

# Gerar PDF
try:
    doc.build(story)
    print(f"✅ PDF gerado com sucesso em: {PDF_PATH}")
except Exception as e:
    print(f"❌ Erro ao gerar o PDF: {e}")

