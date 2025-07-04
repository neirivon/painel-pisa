import json

# Carregando a rubrica
with open("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v4.json", encoding="utf-8") as f:
    rubrica = json.load(f)

# Emojis e cores para as dimensões
emoji_cor_dimensao = {
    "Progressão Cognitiva Educacional": ("🧠", "#1f77b4"),
    "Perfil Socioeconômico e Contextual": ("🏡", "#2ca02c"),
    "Autonomia e Autorregulação da Aprendizagem": ("🎯", "#ff7f0e"),
    "Capacidade de Comunicação e Expressão": ("🗣️", "#d62728"),
    "Raciocínio Lógico e Solução de Problemas": ("🔢", "#9467bd"),
    "Engajamento e Responsabilidade Social": ("🤝", "#8c564b"),
    "Relacionamento com Saberes Científicos e Culturais": ("📚", "#17becf"),
    "Pertencimento e Equidade Territorial (CTC + EJI + ESCS)": ("🌍", "#bcbd22")
}

html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Rubrica SINAPSE IA v1.4</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background: #fdfdfd; }
        h1 { color: #2c3e50; font-size: 2.4em; }
        h2 { margin-top: 30px; }
        h3 { color: #2c3e50; margin-bottom: 4px; }
        .dimensao { margin-bottom: 40px; padding-bottom: 10px; border-bottom: 1px solid #ccc; }
        .nivel { margin-left: 20px; margin-bottom: 15px; }
        .exemplos { margin-left: 40px; color: #555; font-style: italic; }
    </style>
</head>
<body>
    <h1>📘 Rubrica SINAPSE IA – Versão 1.4</h1>
"""

for idx, dim in enumerate(rubrica["dimensoes"], 1):
    nome = dim["dimensao"]
    emoji, cor = emoji_cor_dimensao.get(nome, ("🔸", "#333"))
    html += f"<div class='dimensao'>\n"
    html += f"<h2 style='color:{cor};'>{emoji} {idx}. {nome}</h2>\n"

    for nivel in dim["niveis"]:
        html += f"<div class='nivel'>\n"
        html += f"<h3>🧩 Nível {nivel['nota']} – {nivel['nome']}</h3>\n"
        html += f"<p><strong>Descrição:</strong> {nivel['descricao']}</p>\n"
        html += f"</div>\n"

    html += f"<p><strong>📌 Exemplos práticos:</strong></p>\n<ul class='exemplos'>\n"
    for exemplo in dim["exemplos"]:
        html += f"<li>{exemplo}</li>\n"
    html += "</ul>\n</div>\n"

html += "</body>\n</html>"

with open("painel_pisa/dados_cloud/rubrica_sinapse_ia_v4.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML com emojis e cores gerado: painel_pisa/dados_cloud/rubrica_sinapse_ia_v4.html")

