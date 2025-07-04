import pymongo
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from collections import defaultdict
import os

# Conexão com MongoDB dockerizado
client = pymongo.MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
collection = db["avaliacao_rar_sinapse_ia"]

# Campos avaliativos (A1–A6)
criterios = [
    "clareza_e_objetividade",
    "coerencia_entre_descritores",
    "adequacao_a_pratica_pedagogica",
    "alinhamento_entidades_normativas_e_avaliativas",
    "apoio_metacognicao",
    "engajamento_estudantil"
]

criterios_nomes = {
    "clareza_e_objetividade": "A1. Clareza e Objetividade",
    "coerencia_entre_descritores": "A2. Coerência entre os Descritores",
    "adequacao_a_pratica_pedagogica": "A3. Adequação à Prática Pedagógica",
    "alinhamento_entidades_normativas_e_avaliativas": "A4. Alinhamento às Entidades Normativas e Avaliativas",
    "apoio_metacognicao": "A5. Apoio à Metacognição",
    "engajamento_estudantil": "A6. Engajamento Estudantil"
}

# Buscar dados
documentos = list(collection.find({}))
if not documentos:
    print("⚠️ Nenhum dado encontrado na coleção.")
    exit()

# Organizar dados em DataFrame por dimensão
dados_por_dimensao = defaultdict(list)
for doc in documentos:
    linha = {"juiz": doc["juiz_avaliador"]}
    linha.update({k: int(doc.get(k, -1)) for k in criterios})
    dados_por_dimensao[doc["dimensao_avaliada"]].append(linha)

# Função auxiliar: interpretação do Kappa
def interpretar_kappa(valor):
    if valor < 0:
        return "❌ Discordância"
    elif valor < 0.2:
        return "⚠️ Fraca"
    elif valor < 0.4:
        return "🟡 Razoável"
    elif valor < 0.6:
        return "🟠 Moderada"
    elif valor < 0.8:
        return "🟢 Substancial"
    else:
        return "🟢 Quase Perfeita"

# Início HTML
html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório de Índice Kappa - Avaliação RAR</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
        th { background-color: #f5f5f5; }
        td.interpretacao { font-weight: bold; }
    </style>
</head>
<body>
<h1>Relatório de Consistência entre Juízes (Índice Kappa)</h1>
<p>Este relatório apresenta o nível de concordância entre juízes humanos para cada critério avaliativo da <strong>Rubrica SINAPSE IA</strong>, calculado com o índice <strong>Cohen's Kappa</strong>.</p>
<p><em>Legenda:</em> ❌ Discordância, ⚠️ Fraca, 🟡 Razoável, 🟠 Moderada, 🟢 Substancial/Quase Perfeita.</p>
<hr>
"""

# Processar cada dimensão
for dimensao, avals in dados_por_dimensao.items():
    df = pd.DataFrame(avals)
    html += f"<h2>📘 Dimensão Avaliada: {dimensao}</h2>\n"
    html += "<table><tr><th>Critério</th><th>Kappa</th><th>Interpretação</th></tr>"

    for crit in criterios:
        if df[crit].nunique() > 1:
            # Comparar todos os pares possíveis
            juizes = df["juiz"].tolist()
            notas = df[crit].tolist()
            pares = list(zip(juizes, notas))

            if len(pares) < 2:
                kappa = "-"
                inter = "Insuficiente"
            else:
                valores = df[crit].tolist()
                metade = len(valores) // 2
                kappa = cohen_kappa_score(valores[:metade], valores[metade:]) if len(valores) >= 2 else 0
                inter = interpretar_kappa(kappa)
                kappa = f"{kappa:.2f}"
        else:
            kappa = "-"
            inter = "Notas idênticas"

        html += f"<tr><td>{criterios_nomes[crit]}</td><td>{kappa}</td><td class='interpretacao'>{inter}</td></tr>"

    html += "</table>\n"

html += "</body></html>"

# Salvar HTML
output_path = "relatorio_kappa_avaliacoes.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

client.close()
print(f"✅ Relatório gerado: {output_path}")

