import pandas as pd
from datetime import datetime

# Caminho de entrada e saída
input_csv = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_IA_V1.csv"
output_txt = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacao_rubrica_sinapse_IA_V2.txt"

# Lê o CSV, pulando o cabeçalho redundante
df = pd.read_csv(input_csv, sep=";", encoding="latin1", skiprows=1)

# Nomes dos níveis
niveis = ["Emergente (1)", "Intermediário (2)", "Proficiente (3)", "Avançado (4)"]

# Função de avaliação pedagógica
def avaliar_descritor(valor):
    texto = str(valor).strip().lower()
    if texto in ("", "nan"):
        return 1, "1 de 4 — Descritor ausente ou insuficiente.", "Adicione um critério claro, contextualizado e com propósito pedagógico."
    elif any(p in texto for p in ["simples", "baixa mobilização", "restrito", "dificuldade"]):
        return 2, "2 de 4 — Genérico ou superficial.", "Aprofunde a formulação e adicione elementos que demonstrem aplicação pedagógica."
    elif any(p in texto for p in ["compreende", "organiza", "planeja", "autonomia", "fluência", "relaciona", "analisa"]):
        return 3, "3 de 4 — Consistente, mas pode evoluir.", "Refine o descritor com maior intencionalidade e vínculo com práticas reais."
    else:
        return 4, "4 de 4 — Descritor sólido e bem articulado.", "Mantém clareza, intencionalidade pedagógica e aplicabilidade concreta."

# Geração do texto de avaliação
linhas = []
linhas.append("🧠 AVALIAÇÃO PEDAGÓGICA — Rubrica SINAPSE IA v1.2")
linhas.append(f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n")

for _, row in df.iterrows():
    dimensao = str(row.get("Dimensao", "")).strip()
    if not dimensao:
        continue

    linhas.append(f"📘 Dimensão: {dimensao}")

    for nivel in niveis:
        descritor_raw = row.get(nivel, "")
        descritor = str(descritor_raw) if not pd.isna(descritor_raw) else ""
        nota, avaliacao, sugestao = avaliar_descritor(descritor)
        linhas.append(f"\n🔹 {nivel}")
        linhas.append(f"• Descritor: {descritor.strip()}")
        linhas.append(f"• Nota: {nota} de 4")
        linhas.append(f"• Avaliação: {avaliacao}")
        if nota < 4:
            linhas.append(f"• Sugestão de Melhoria: {sugestao}")

    exemplos_raw = row.get("exemplos", "")
    if isinstance(exemplos_raw, str) and exemplos_raw.strip():
        exemplos = [ex.strip() for ex in exemplos_raw.strip().split("\n") if ex.strip()]
        if exemplos:
            linhas.append("\n📍 Exemplos TMAP:")
            for ex in exemplos:
                linhas.append(f"– {ex}")

    linhas.append("\n" + "-"*90 + "\n")

# Salva em .txt
with open(output_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print(f"✅ Avaliação concluída e salva em: {output_txt}")

