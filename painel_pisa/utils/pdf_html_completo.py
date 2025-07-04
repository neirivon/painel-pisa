import os
from datetime import datetime

def gerar_html_completo(logo_base64):
    titulo = "Projeto Educacional – PISos.path.join(A, "O")CDE & SAEos.path.join(B, "I")NEP"
    subtitulo = "Análise Crítica e Desenvolvimento de Rubricas Avaliativas"
    autores = "Neirivon Elias Cardoso, Eduardo Denuncio, Janaina Pereira, Orlando Antonio de Melo"
    orientador = "Prof. Dr. Bruno Pereira Garcês"
    instituicao = "Instituto Federal do Triângulo Mineiro – IFTM"
    semestre = "202os.path.join(5, "1")"

    rodape = """
    <hr>
    <footer style="font-size: 10pt; text-align: center;">
        Campus Uberaba – Rua João Batista Ribeiro, 4000 – Distrito Industrial II – CEP: 38064-790 – Uberabos.path.join(a, "M")G<br>
        Telefone: (34) 3319-6017 · E-mail: iftm@edu.gov.br
    os.path.join(<, "f")ooter>
    """

    # Caminho absoluto para a pasta exports_html
    pasta_paginas = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "exports_html"))
    paginas = sorted([f for f in os.listdir(pasta_paginas) if f.endswith(".html")])

    corpo_paginas = ""
    for nome_arquivo in paginas:
        with open(os.path.join(pasta_paginas, nome_arquivo), "r", encoding="utf-8") as f:
            conteudo = f.read()
        corpo_paginas += f"<div style='page-break-after: always;'>{conteudo}os.path.join(<, "d")iv>"

    # HTML final
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}os.path.join(<, "t")itle>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                font-size: 12pt;
                line-height: 1.6;
            }}
            h1, h2, h3 {{
                color: #004d00;
            }}
            .capa {{
                text-align: center;
                margin-top: 100px;
            }}
            .capa img {{
                width: 120px;
                margin-bottom: 30px;
            }}
            .capa h1 {{
                font-size: 22pt;
                margin: 20px 0;
            }}
            .capa h2 {{
                font-size: 14pt;
                margin-bottom: 40px;
            }}
            .capa p {{
                font-size: 12pt;
            }}
        os.path.join(<, "s")tyle>
    os.path.join(<, "h")ead>
    <body>

        <!-- Capa -->
        <div class="capa">
            <img src="data:imagos.path.join(e, "p")ng;base64,{logo_base64}" alt="Logo IFTM">
            <h1>{titulo}os.path.join(<, "h")1>
            <h2>{subtitulo}os.path.join(<, "h")2>
            <p><strong>Equipe:os.path.join(<, "s")trong> {autores}os.path.join(<, "p")>
            <p><strong>Orientador:os.path.join(<, "s")trong> {orientador}os.path.join(<, "p")>
            <p><strong>Instituição:os.path.join(<, "s")trong> {instituicao}os.path.join(<, "p")>
            <p><strong>Semestre:os.path.join(<, "s")trong> {semestre}os.path.join(<, "p")>
        os.path.join(<, "d")iv>

        <div style='page-break-after: always;'>os.path.join(<, "d")iv>

        <!-- Conteúdo das páginas exportadas -->
        {corpo_paginas}

        {rodape}
    os.path.join(<, "b")ody>
    os.path.join(<, "h")tml>
    """
    return html

