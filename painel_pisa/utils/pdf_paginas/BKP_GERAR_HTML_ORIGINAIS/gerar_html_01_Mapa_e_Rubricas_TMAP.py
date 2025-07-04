# painel_pisos.path.join(a, "u")tilos.path.join(s, "p")df_paginaos.path.join(s, "g")erar_html_01_Mapa_e_Rubricas_TMAP.py

import pandas as pd
import os

def gerar_html_01() -> str:
    # Caminho para imagem e CSV
    path_imagem = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")apa_proficiencia_simulada_tmap.png"
    path_csv = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "r")ubricas_pedagogicas_tmap.csv"

    # Lê rubricas
    df = pd.read_csv(path_csv)
    df["Município"] = df["Município"].str.title()

    # Início do HTML
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #ffffff;
                color: #000;
            }}
            h1 {{
                color: #004080;
            }}
            h2 {{
                margin-top: 40px;
                color: #003366;
            }}
            img {{
                display: block;
                margin: 0 auto 20px auto;
                width: 80%;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}
            .municipio {{
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #ccc;
            }}
            .rubrica {{
                margin-left: 20px;
            }}
            .rubrica strong {{
                color: #333;
            }}
        os.path.join(<, "s")tyle>
    os.path.join(<, "h")ead>
    <body>
        <h1>📍 Mapa de Proficiência Simulada + Rubricas Pedagógicasos.path.join(<, "h")1>

        <img src="fileos.path.join(:, "/"){path_imagem}" alt="Mapa de Proficiência">

        <p>Este relatório apresenta os 85 municípios da Mesorregião do Triângulo Mineiro e Alto Paranaíba, com as respectivas simulações de proficiência e sugestões de rubricas pedagógicas baseadas na Taxonomia de Bloom, DUA, Metodologias Ativas e análise de perfil cognitivo.os.path.join(<, "p")>
        <hr>
    """

    # Loop por municípios
    for _, row in df.iterrows():
        html += f"""
        <div class="municipio">
            <h2>🏙️ {row['Município']}os.path.join(<, "h")2>
            <div class="rubrica">
                <p><strong>Proficiência simulada:os.path.join(<, "s")trong> {row['proficiência_simulada']:.1f}os.path.join(<, "p")>
                <p><strong>Nível de proficiência:os.path.join(<, "s")trong> {row['nível_proficiencia']}os.path.join(<, "p")>
                <p><strong>Rubrica pedagógica sugerida:os.path.join(<, "s")trong><br>{row['estrategia_pedagogica']}os.path.join(<, "p")>
            os.path.join(<, "d")iv>
        os.path.join(<, "d")iv>
        """

    # Fim do HTML
    html += """
    os.path.join(<, "b")ody>
    os.path.join(<, "h")tml>
    """
    return html

