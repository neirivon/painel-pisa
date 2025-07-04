from pathlib import Path
from weasyprint import HTML
from datetime import datetime

# === CONFIGURAÇÕES ===
ARQUIVO_TXT = "/home/neirivon/SINAPSE2.0/PISA/avaliacao_completa_llama3_20250619_2012.txt"
PASTA_ICONES = "/home/neirivon/SINAPSE2.0/PISA/icones_dimensoes/"
ARQUIVO_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/relatorio_visual_educacional_llama3_final.pdf"

# === LÊ O CONTEÚDO DO TXT ===
texto = Path(ARQUIVO_TXT).read_text(encoding="utf-8")
blocos = texto.split("=== DIMENSÃO")

# === EMOJIS EDUCATIVOS POR TEMA (ordem presumida) ===
emojis = ["🧠", "🏡", "📝", "💬", "🧮", "🤝", "🎓", "📍"]
dim_cores = ["#34495e", "#1abc9c", "#3498db", "#9b59b6", "#e67e22", "#f39c12", "#16a085", "#c0392b"]

# === GERA HTML FORMATADO COM CORES, ÍCONES E EMOJIS ===
html = """
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Arial'; font-size: 14px; line-height: 1.6; color: #333; padding: 30px; }}
    h1 {{ text-align: center; color: #2c3e50; }}
    h2 {{ margin-top: 40px; font-size: 20px; color: #2c3e50; border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
    .dimensao {{ padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #f9f9f9; }}
    img.icone {{ float: right; width: 64px; height: 64px; margin-left: 10px; }}
    .bloco {{ white-space: pre-wrap; background: #fcfcfc; border-left: 4px solid #ddd; padding: 10px 15px; margin: 10px 0; }}
  </style>
</head>
<body>
<h1>📘 Relatório de Avaliação Educacional com IA – LLAMA3</h1>
<p>Gerado automaticamente em: <strong>{}</strong></p>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M"))

# === ADICIONA CADA DIMENSÃO ===
for idx, bloco in enumerate(blocos[1:], 1):
    titulo_raw = bloco.split("\n")[0].replace(":", "").strip()
    conteudo = bloco.replace(titulo_raw, "").strip()

    emoji = emojis[idx - 1] if idx <= len(emojis) else "🔎"
    cor = dim_cores[idx - 1] if idx <= len(dim_cores) else "#bdc3c7"
    icone_nome = titulo_raw.lower().replace(" ", "_").replace("(", "").replace(")", "")
    icone_path = f"{PASTA_ICONES}/{icone_nome}.png"

    html += f"""
    <div class="dimensao" style="border-left: 10px solid {cor};">
      <h2>{emoji} {titulo_raw}</h2>
      <img src="file://{icone_path}" class="icone">
      <div class="bloco">{conteudo}</div>
    </div>
    """

html += "</body></html>"

# === GERA O PDF ===
HTML(string=html).write_pdf(ARQUIVO_SAIDA)
print(f"✅ PDF gerado com sucesso: {ARQUIVO_SAIDA}")

