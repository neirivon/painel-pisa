from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import json

# Caminhos absolutos
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
PDF_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/gabarito_professor.pdf"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # fonte instalada via apt

# Registrar a fonte
pdfmetrics.registerFont(TTFont("DejaVu", FONT_PATH))

def carregar_questoes():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
    # Verifica se os itens são strings JSON em vez de dicionários
    if isinstance(dados[0], str):
        dados = [json.loads(q) for q in dados]
    return dados

def gerar_pdf(questoes):
    c = canvas.Canvas(PDF_PATH, pagesize=A4)
    largura, altura = A4
    margem = 2 * cm
    largura_util = largura - 2 * margem
    altura_util = altura - 2 * margem

    style = ParagraphStyle(
        name="Normal",
        fontName="DejaVu",
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
    )

    c.setFont("DejaVu", 14)
    c.drawCentredString(largura / 2, altura - margem, "GABARITO DO PROFESSOR — QUESTÕES TMAP")
    y = altura - margem - 2 * cm

    for idx, q in enumerate(questoes, start=1):
        titulo = f"<b>🔢 Questão {idx} – {q['disciplina']}</b>"
        pergunta = f"<b>📘 Pergunta Adaptada:</b><br/>{q['pergunta_adaptada_tmap']}"
        resposta = f"<b>✅ Resposta Esperada:</b><br/>{q.get('resposta_modelo', '❌ Não informada.')}"

        elementos = [
            Paragraph(titulo, style),
            Paragraph(pergunta, style),
            Paragraph(resposta, style),
        ]

        frame = Frame(margem, margem, largura_util, y - margem, showBoundary=0)
        frame.addFromList(elementos, c)

        c.showPage()
        y = altura - margem - 2 * cm

    c.save()
    print(f"✅ PDF salvo em: {PDF_PATH}")

if __name__ == "__main__":
    try:
        questoes = carregar_questoes()
        os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
        gerar_pdf(questoes)
    except Exception as e:
        print(f"❌ Erro ao gerar o PDF: {e}")

