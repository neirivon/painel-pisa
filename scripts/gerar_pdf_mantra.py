from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import os

# Caminho do arquivo de entrada e saída
arquivo_txt = "/home/neirivon/Downloads/transcricao_mantra_sinapse.txt"
arquivo_pdf = "/home/neirivon/Downloads/mantra_sinapse.pdf"

# Carregar conteúdo do TXT (UTF-8)
with open(arquivo_txt, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Criar canvas e frame para layout fluido
c = canvas.Canvas(arquivo_pdf, pagesize=A4)
largura, altura = A4

# Estilo de parágrafo
estilos = getSampleStyleSheet()
estilo_centralizado = ParagraphStyle(
    'CentroGrande',
    parent=estilos['Normal'],
    fontName='Helvetica',
    fontSize=12,
    leading=16,
    alignment=TA_CENTER,
    spaceAfter=10
)

# Dividir conteúdo por parágrafos
blocos = conteudo.strip().split("\n\n")
elementos = []

# Adicionar parágrafos ao fluxo de layout
for bloco in blocos:
    linhas = bloco.strip().split('\n')
    for linha in linhas:
        elementos.append(Paragraph(linha.strip(), estilo_centralizado))
    elementos.append(Spacer(1, 0.5 * cm))

# Inserir conteúdo em frame ajustável
margem = 2 * cm
frame = Frame(margem, margem, largura - 2 * margem, altura - 2 * margem, showBoundary=0)
frame.addFromList(elementos, c)

# Finalizar e salvar PDF
c.save()

print(f"✅ PDF gerado com sucesso: {arquivo_pdf}")

