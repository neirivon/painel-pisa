from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
import os

# Caminho de saída do novo PDF
output_pdf = os.path.expanduser("~/SINAPSE2.0/PISA/TCLE_IFTM_Sem_Tracos_Espacos.pdf")

# Estilo de texto
styles = getSampleStyleSheet()
style_normal = styles["Normal"]

# Iniciar geração do PDF
c = canvas.Canvas(output_pdf, pagesize=A4)

# Texto do documento com espaços no lugar dos traços
text_lines = [
    "Instituto Federal do Triângulo Mineiro - Campus Uberaba",
    "Mestrado Profissional em Educação Tecnológica - IFTM",
    "",
    "Pesquisador Responsável: Neirivon Elias Cardoso",
    "E-mail: neirivon.cardoso@estudante.iftm.edu.br",
    "",
    "Título da Pesquisa:",
    "Análise Educacional com Foco em Avaliações Externas e Rubricas Pedagógicas no 9º Ano do Ensino Fundamental",
    "",
    "1. APRESENTAÇÃO",
    "Você está sendo convidado(a) a autorizar a participação de seu(ua) filho(a) ou dependente legal, estudante do 9º ano do Ensino Fundamental, na presente pesquisa educacional, que tem por objetivo analisar práticas de avaliação, competências cognitivas e indicadores socioeducacionais por meio de atividades adaptadas de avaliações internacionais (como o PISA/OCDE) e nacionais (como o SAEB).",
    "",
    "2. PROCEDIMENTOS",
    "A participação envolverá o preenchimento de questionários e/ou atividades educacionais digitais, de forma voluntária, remota ou presencial, em horário previamente acordado com a escola.",
    "",
    "3. RISCOS E BENEFÍCIOS",
    "Não há riscos físicos ou psicológicos significativos. A participação poderá beneficiar o(a) aluno(a) por meio de atividades que desenvolvem habilidades cognitivas e metacognitivas, com base em metodologias ativas e rubricas pedagógicas.",
    "",
    "4. CONFIDENCIALIDADE",
    "Todas as informações coletadas serão tratadas de forma anônima, sigilosa e agregada. Nenhum dado individual identificável será divulgado.",
    "",
    "5. DIREITO DE RETIRADA",
    "O(a) responsável poderá retirar a autorização a qualquer momento, sem prejuízo ao(à) estudante.",
    "",
    "6. DECLARAÇÃO DE CONSENTIMENTO",
    "Eu,                      , CPF nº              , declaro que:",
    "* Fui adequadamente informado(a) sobre os objetivos, procedimentos e garantias éticas da pesquisa;",
    "* Autorizo a participação de meu/minha filho(a)/dependente legal               , nas atividades descritas acima;",
    "* Estou ciente de que posso revogar este consentimento a qualquer momento.",
    "",
    "Local:                     Data:    /    /",
    "Assinatura Digital via GOV.BR (ICP-Brasil)"
]

# Posicionar texto
x = 50
y = 750
for line in text_lines:
    if line.strip() == "":
        y -= 10
    else:
        p = Paragraph(line, style_normal)
        w, h = p.wrap(500, y)
        p.drawOn(c, x, y - h)
        y -= h + 5

# Finalizar PDF
c.save()

print(f"\n✅ PDF gerado com sucesso em:\n{output_pdf}")
