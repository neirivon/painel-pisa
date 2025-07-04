from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pathlib import Path

# Caminho do arquivo de entrada
CAMINHO_TXT = "/home/neirivon/SINAPSE2.0/PISA/avaliacao_completa_llama3_20250619_2012.txt"
CAMINHO_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/relatorio_avaliacao_llama3_colorido.pdf"

# Emojis e cores por dimensão (exemplos)
ICONES = ["📘", "📗", "📙", "📕", "📒", "📓", "🧠", "🧩"]
CORES = [colors.lightblue, colors.lightgreen, colors.lightgoldenrodyellow,
         colors.pink, colors.violet, colors.burlywood, colors.lightgrey, colors.peachpuff]

# Fontes maiores e mais agradáveis para leitura
pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSerif.ttf"))
addMapping("DejaVu", 0, 0, "DejaVu")

# Estilos de parágrafos
estilo_titulo = ParagraphStyle(name="Titulo", fontName="DejaVu", fontSize=18, leading=22,
                               alignment=TA_CENTER, spaceAfter=20, textColor=colors.darkblue)
estilo_dimensao = ParagraphStyle(name="Dimensao", fontName="DejaVu", fontSize=14, leading=18,
                                 textColor=colors.white, backColor=colors.darkblue,
                                 alignment=TA_LEFT, spaceBefore=10, spaceAfter=10, leftIndent=10)
estilo_texto = ParagraphStyle(name="Texto", fontName="DejaVu", fontSize=12, leading=16,
                              spaceBefore=4, spaceAfter=4)

def gerar_pdf():
    # Carrega o texto
    texto = Path(CAMINHO_TXT).read_text(encoding="utf-8")

    # Divide em blocos por dimensão
    blocos = texto.strip().split("=== DIMENSÃO ")
    elementos = []

    elementos.append(Paragraph("📊 Relatório de Avaliação – Rubrica SINAPSE IA com Triangulação PISA/SAEB e LLAMA3", estilo_titulo))
    elementos.append(Spacer(1, 20))

    for i, bloco in enumerate(blocos[1:]):  # ignora índice 0 (vazio)
        partes = bloco.split("===\n", 1)
        cabecalho = partes[0].strip()
        corpo = partes[1].strip()

        emoji = ICONES[i % len(ICONES)]
        cor = CORES[i % len(CORES)]
        titulo = f"{emoji} Dimensão {cabecalho}"

        # Adiciona cabeçalho com fundo colorido
        elementos.append(Paragraph(titulo, ParagraphStyle(name="Cabecalho",
                                                           fontName="DejaVu",
                                                           fontSize=14,
                                                           leading=18,
                                                           backColor=cor,
                                                           textColor=colors.black,
                                                           spaceBefore=10,
                                                           spaceAfter=10,
                                                           leftIndent=5)))
        # Parágrafos do corpo
        for par in corpo.split("\n\n"):
            elementos.append(Paragraph(par.strip().replace("**", ""), estilo_texto))

        elementos.append(PageBreak())

    # Cria PDF
    doc = SimpleDocTemplate(CAMINHO_SAIDA, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=40, bottomMargin=30)

    doc.build(elementos)
    print(f"✅ PDF gerado com sucesso em: {CAMINHO_SAIDA}")

if __name__ == "__main__":
    gerar_pdf()

