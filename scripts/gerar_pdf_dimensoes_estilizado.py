from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from pathlib import Path
import re

# === CONFIGURAÇÕES ===
ARQUIVO_TXT = "/home/neirivon/SINAPSE2.0/PISA/avaliacao_completa_llama3_20250619_2012.txt"
PASTA_IMAGENS = "/home/neirivon/SINAPSE2.0/PISA/icones_dimensoes/"
ARQUIVO_PDF_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/relatorio_avaliacao_IA_colorido_final.pdf"

# === ESTILOS ===
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TituloPrincipal", fontSize=20, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor("#2C3E50")))
styles.add(ParagraphStyle(name="TituloDimensao", fontSize=16, textColor=colors.HexColor("#1ABC9C"), spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="TextoAvaliacao", fontSize=11, leading=15, spaceAfter=10, fontName="Helvetica"))

# === FUNÇÃO AUXILIAR PARA MAPEAR DIMENSÃO → IMAGEM ===
def obter_nome_imagem(titulo):
    titulo = titulo.lower()
    if "cognitiva" in titulo:
        return "cognitiva.png"
    elif "socioeconômico" in titulo or "socioeconomico" in titulo:
        return "socioeconomico.png"
    elif "autonomia" in titulo or "autorregulação" in titulo:
        return "autonomia.png"
    elif "comunicação" in titulo or "expressão" in titulo:
        return "comunicacao.png"
    elif "raciocínio" in titulo or "problemas" in titulo:
        return "raciocinio.png"
    elif "responsabilidade" in titulo:
        return "responsabilidade.png"
    elif "saberes" in titulo or "científicos" in titulo:
        return "saberes.png"
    elif "equidade" in titulo or "pertencimento" in titulo:
        return "equidade.png"
    return None

# === CRIAÇÃO DO PDF ===
doc = SimpleDocTemplate(ARQUIVO_PDF_SAIDA, pagesize=A4,
                        rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
flow = []

# Título inicial
flow.append(Paragraph("📘 Avaliação da Rubrica SINAPSE IA com apoio da IA LLAMA3", styles["TituloPrincipal"]))
flow.append(Spacer(1, 12))

# Lê o conteúdo do TXT
with open(ARQUIVO_TXT, "r", encoding="utf-8") as f:
    linhas = f.read().split("\n")

# Processa cada dimensão com base no padrão === DIMENSÃO: <nome> ===
bloco = []
dimensao_atual = ""

for linha in linhas:
    if linha.startswith("=== DIMENSÃO"):
        if bloco and dimensao_atual:
            flow.append(PageBreak())
            flow.append(Paragraph(f"📌 {dimensao_atual}", styles["TituloDimensao"]))
            imagem = obter_nome_imagem(dimensao_atual)
            if imagem:
                caminho = Path(PASTA_IMAGENS) / imagem
                if caminho.exists():
                    flow.append(Image(str(caminho), width=80, height=80))
            flow.append(Spacer(1, 6))
            for par in bloco:
                flow.append(Paragraph(par, styles["TextoAvaliacao"]))
            bloco = []

        # Extrair nome da dimensão
        match = re.search(r"DIMENSÃO\s\d+/\d+:\s(.+?)\s*===", linha)
        if match:
            dimensao_atual = match.group(1).strip()
    elif linha.strip() == "":
        continue
    else:
        bloco.append(linha)

# Último bloco
if bloco and dimensao_atual:
    flow.append(PageBreak())
    flow.append(Paragraph(f"📌 {dimensao_atual}", styles["TituloDimensao"]))
    imagem = obter_nome_imagem(dimensao_atual)
    if imagem:
        caminho = Path(PASTA_IMAGENS) / imagem
        if caminho.exists():
            flow.append(Image(str(caminho), width=80, height=80))
    flow.append(Spacer(1, 6))
    for par in bloco:
        flow.append(Paragraph(par, styles["TextoAvaliacao"]))

# Geração final
doc.build(flow)
print(f"✅ PDF gerado com sucesso: {ARQUIVO_PDF_SAIDA}")

