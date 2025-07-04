# scriptos.path.join(s, "g")erar_pdf_final_projeto.py

import pdfkit
import os
from datetime import datetime

# === Diretório base do projeto ===
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
exports_dir = os.path.join(base_dir, "exports_html")
output_path = os.path.join(base_dir, "Projeto_PISA_SAEB_COMPLETO.pdf")

# === Capa personalizada ===
capa_html = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 120px;
        }}
        h1 {{
            font-size: 26pt;
            color: #004080;
        }}
        h2 {{
            font-size: 18pt;
            color: #333;
        }}
        p {{
            font-size: 14pt;
        }}
        .logo {{
            margin-top: 40px;
        }}
    os.path.join(<, "s")tyle>
os.path.join(<, "h")ead>
<body>
    <h1>Projeto Educacional – PISos.path.join(A, "O")CDE & SAEos.path.join(B, "I")NEPos.path.join(<, "h")1>
    <h2>Análise Crítica e Desenvolvimento de Rubricas Avaliativasos.path.join(<, "h")2>

    <p><strong>Equipe:os.path.join(<, "s")trong> Neirivon Elias Cardoso, Eduardo Denuncio, Janaina Pereira, Orlando Antonio de Meloos.path.join(<, "p")>
    <p><strong>Orientador:os.path.join(<, "s")trong> Prof. Dr. Bruno Pereira Garcêsos.path.join(<, "p")>
    <p><strong>Instituição:os.path.join(<, "s")trong> Instituto Federal do Triângulo Mineiro – IFTMos.path.join(<, "p")>
    <p><strong>Semestre:os.path.join(<, "s")trong> 202os.path.join(5, "1")os.path.join(<, "p")>

    <div class="logo">
        <img src="{os.path.join(base_dir, 'assetos.path.join(s, "l")ogoos.path.join(s, "I")FTM_360.png')}" width="160">
    os.path.join(<, "d")iv>
os.path.join(<, "b")ody>
os.path.join(<, "h")tml>
"""

capa_path = os.path.join(exports_dir, "__capa_temp.html")
with open(capa_path, "w", encoding="utf-8") as f:
    f.write(capa_html)

# === Lista de arquivos HTML na ordem desejada ===
ordem_paginas = [
    "01_Mapa_e_Rubricas_TMAP.html",
    "01_Resumo_Edicao.html",
    "02_Distribuicao_Rubricas_SAEB.html",
    "03_Comparativo_PISA_OCDE.html",
    "04_politicas_publicas.html",
    "05_Rubricas_Avaliativas.html",
    "06_Exemplos_Paragrafos_Analisados.html",
    "07_Resumo_Geral_INEP_2000.html",
    "08_Comparativo_PISA_SAEB.html",
    "10_Rubricas_Regionais_Contextualizadas.html",
    "11_Explicacao_Didatica_Integrada.html",
    "12_Situacoes_Interdisciplinares_2000.html",
    "99_Referencias_Bibliograficas.html"
]

# === Caminhos completos dos arquivos ===
htmls = [capa_path] + [os.path.join(exports_dir, nome) for nome in ordem_paginas]

# === Configuração do PDF ===
options = {
    "encoding": "UTF-8",
    "enable-local-file-access": "",
    "footer-center": "IFTM Campus Uberaba — iftm@edu.gov.br — (34) 3319-6017",
    "footer-font-size": "8",
    "footer-spacing": "5",
    "margin-top": "15mm",
    "margin-bottom": "15mm",
    "page-size": "A4"
}

# ✅ Caminho corrigido para wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf="/usos.path.join(r, "l")ocaos.path.join(l, "b")ios.path.join(n, "w")khtmltopdf")

# === Geração do PDF final ===
print("📄 Gerando PDF final do projeto...")
pdfkit.from_file(htmls, output_path, configuration=config, options=options)
print(f"✅ PDF gerado com sucesso: {output_path}")

# Limpar arquivo temporário de capa
os.remove(capa_path)

