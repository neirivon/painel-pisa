import json
import pandas as pd
from datetime import datetime

rubrica_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"
rubrica_avaliadora_csv = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/Rubrica_Avaliacao_de_Rubricas.csv"
saida_txt = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacao_rubrica_sinapse_IA_V2.txt"

# Carregar arquivos
with open(rubrica_json, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

avaliadora = pd.read_csv(rubrica_avaliadora_csv, encoding="latin1")

# Avaliação simples com base em presença de termos pedagógicos
def avaliar_descritor(texto):
    texto = texto.lower()
    if any(p in texto for p in ["contexto", "transformação", "resolução", "aprendizagem", "autonomia", "reflexão"]):
        return 4, "✔️ Alinhado a práticas pedagógicas significativas e bem contextualizado."
    elif any(p in texto for p in ["exemplo", "explica", "demonstra", "conhece"]):
        return 3, "🔄 Bom, mas pode aprofundar vínculos com situações didáticas contextualizadas ou ampliar intencionalidade pedagógica."
    elif len(texto.strip()) < 10:
        return 1, "❌ Muito vago ou ausente. Reescrever o descritor com foco em clareza, aplicabilidade e profundidade educacional."
    else:
        return 2, "⚠️ Genérico. Poderia ser melhorado com exemplos, clareza conceitual ou vinculação curricular."

# Gerar relatório
linhas = [f"📘 Avaliação Automática — Rubrica SINAPSE IA v1.2\nData: {datetime.now()}\n\n"]

for dim in rubrica["dimensoes"]:
    linhas.append(f"🔹 Dimensão: {dim['dimensao']}")
    if "niveis" in dim:
        for nivel in dim["niveis"]:
            nota, justificativa = avaliar_descritor(nivel["descricao"])
            linhas.append(f"\n◼️ Nível {nivel['nota']} — {nivel['nome']}")
            linhas.append(f"   ➤ Descritor: {nivel['descricao']}")
            linhas.append(f"   📝 Nota: {nota} de 4")
            linhas.append(f"   📌 Justificativa: {justificativa}")
            if nota < 4:
                linhas.append(f"   💡 Sugestão de melhoria: Reescreva com foco em clareza conceitual, contextualização regional (TMAP) e vínculo pedagógico mais explícito.")
    if "exemplos" in dim and dim["exemplos"]:
        linhas.append("\n   📍 Exemplos TMAP:")
        for ex in dim["exemplos"]:
            linhas.append(f"     - {ex}")
    linhas.append("\n" + "-"*70 + "\n")

# Salvar
with open(saida_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print(f"✅ Avaliação salva em: {saida_txt}")

