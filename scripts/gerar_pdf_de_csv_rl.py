from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import csv
import os

CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor_final.pdf"

c = canvas.Canvas(PDF_PATH, pagesize=A4)
width, height = A4
y = height - 2 * cm

def draw_header():
    global y
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "📘 Gabarito para Correção – Rubrica SINAPSE v1.4")
    y -= 1 * cm
    c.setFont("Helvetica", 12)

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    draw_header()
    idx = 1
    for row in reader:
        if y < 4 * cm:
            c.showPage()
            y = height - 2 * cm
            draw_header()

        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, y, f"🔢 Questão {idx} – {row['disciplina']}")
        y -= 0.6 * cm

        c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, "🌱 Pergunta adaptada ao TMAP:")
        y -= 0.5 * cm

        for line in row['pergunta_adaptada_tmap'].split('\n'):
            c.drawString(2.5 * cm, y, line.strip())
            y -= 0.5 * cm

        c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, "✅ Resposta modelo sugerida:")
        y -= 0.5 * cm

        for line in row['resposta_modelo'].split('\n'):
            c.drawString(2.5 * cm, y, line.strip())
            y -= 0.5 * cm

        y -= 0.6 * cm
        idx += 1

c.save()
print(f"✅ PDF gerado com sucesso em: {PDF_PATH}")

