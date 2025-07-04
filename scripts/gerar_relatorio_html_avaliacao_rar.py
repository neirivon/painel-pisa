import pymongo
import pandas as pd
from datetime import datetime

# Conexão MongoDB dockerizado
client = pymongo.MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["sinapse"]
collection = db["avaliacao_rar_sinapse_ia"]

# Buscar todos os documentos
docs = list(collection.find())
if not docs:
    print("⚠️ Nenhum dado encontrado na coleção.")
    exit()

# Converter para DataFrame
df = pd.DataFrame(docs)
df = df.drop(columns=["_id"])  # Oculta campo interno

# Geração do HTML
html = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>Avaliação da Rubrica SINAPSE IA via LLaMA 3</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #f9f9f9;
            padding: 30px;
        }}
        h1 {{
            text-align: center;
            color: #003366;
        }}
        .info {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }}
        th {{
            background-color: #003366;
            color: white;
            padding: 12px;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ccc;
            vertical-align: top;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .nota-baixa {{
            background-color: #ffe0e0;
        }}
        .justificativa {{
            font-size: 13px;
            color: #333;
        }}
    </style>
</head>
<body>
    <h1>📘 Avaliação da Rubrica SINAPSE IA<br>Auxiliada por RAR e IA (LLaMA 3)</h1>
    <div class="info">
        Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
        Base: MongoDB dockerizado | Modelo: LLaMA 3 via Ollama
    </div>
    <table>
        <tr>
            <th>🧭 Dimensão</th>
            <th>🎯 Nível</th>
            <th>📌 Critério RAR</th>
            <th>📝 Nota</th>
            <th>💬 Justificativa da IA</th>
        </tr>
"""

# Preenchimento linha a linha
for _, row in df.iterrows():
    nota = int(row.get("nota_rar", 0))
    css_class = "nota-baixa" if nota <= 2 else ""
    html += f"""
        <tr class="{css_class}">
            <td>{row.get("dimensao", "-")}</td>
            <td>{row.get("nivel", "-")}</td>
            <td>{row.get("criterio_rar", "-")}</td>
            <td><strong>{nota}</strong></td>
            <td class="justificativa">{row.get("justificativa", "-")}</td>
        </tr>
    """

html += """
    </table>
</body>
</html>
"""

# Salvar
with open("avaliacao_rar_llama3_sinapse_ia.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Relatório salvo como 'avaliacao_rar_llama3_sinapse_ia.html'")

