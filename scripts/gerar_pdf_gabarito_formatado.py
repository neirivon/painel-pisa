from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
import csv
import os

# Caminhos
CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor_formatado.pdf"

# Documento PDF
doc = SimpleDocTemplate(PDF_PATH, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()
story = []

# Estilos personalizados
style_title = ParagraphStyle(name="Title", fontSize=18, textColor=colors.darkblue, leading=22, spaceAfter=14)
style_heading_leitura = ParagraphStyle(name="HeadingLeitura", fontSize=14, textColor=colors.darkgreen, spaceAfter=8, leading=18)
style_heading_matematica = ParagraphStyle(name="HeadingMatematica", fontSize=14, textColor=colors.darkblue, spaceAfter=8, leading=18)
style_heading_ciencias = ParagraphStyle(name="HeadingCiencias", fontSize=14, textColor=colors.darkred, spaceAfter=8, leading=18)
style_block = ParagraphStyle(name="Block", fontSize=11, leading=16)
style_label = ParagraphStyle(name="Label", fontSize=11, textColor=colors.HexColor('#333333'), leading=14)

# Cabeçalho
story.append(Paragraph("🎓 Gabarito das Questões Adaptadas do PISA 2022 para o TMAP", style_title))

# Leitura do CSV
with open(CSV_PATH, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, 1):
        disciplina = row['disciplina'].strip().lower()
        if disciplina == "leitura":
            style_heading = style_heading_leitura
            emoji = "📖"
        elif disciplina == "matemática" or disciplina == "matematica":
            style_heading = style_heading_matematica
            emoji = "🧮"
        elif disciplina == "ciências" or disciplina == "ciencias":
            style_heading = style_heading_ciencias
            emoji = "🧪"
        else:
            style_heading = styles["Heading2"]
            emoji = "❓"

        story.append(Paragraph(f"{emoji} Questão {idx} — {row['disciplina']}", style_heading))

        tabela = [
            [Paragraph("📘 <b>Pergunta Original:</b>", style_label), Paragraph(row['pergunta_original'], style_block)],
            [Paragraph("🌱 <b>Pergunta Adaptada ao TMAP:</b>", style_label), Paragraph(row['pergunta_adaptada_tmap'], style_block)],
            [Paragraph("✅ <b>Resposta Modelo:</b>", style_label), Paragraph(row['resposta_modelo'], style_block)],
            [Paragraph("📌 <b>Rubrica:</b>", style_label), Paragraph(row['rubrica_pedagogica'], style_block)],
            [Paragraph("🔍 <b>Fonte:</b>", style_label), Paragraph(f"{row['fonte']} — {row['ano']}, versão {row['versao']}", style_block)]
        ]

        tbl = Table(tabela, colWidths=[5.5*cm, 10*cm])
        tbl.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
            ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6)
        ]))

        story.append(tbl)
        story.append(Spacer(1, 20))

# Geração do PDF
doc.build(story)
print(f"✅ PDF gerado com sucesso em: {PDF_PATH}")

