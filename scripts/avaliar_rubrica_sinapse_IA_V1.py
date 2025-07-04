import pandas as pd
from datetime import datetime
import os

# Caminhos corrigidos
rubrica_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_IA_V1.csv"
avaliacao_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/Rubrica_Avaliacao_de_Rubricas.csv"

# Carregar os dados
rubrica_df = pd.read_csv(rubrica_path)
avaliacao_df = pd.read_csv(avaliacao_path)

# Função de avaliação pedagógica com base em palavras-chave
def avaliar_criterio(descritor):
    texto = str(descritor).lower()

    if any(p in texto for p in ["contexto regional", "tmapi", "exemplos práticos", "relevância pedagógica"]):
        return 4, "4 de 4 — O descritor está claro, contextualizado e com exemplos significativos alinhados ao TMAP."
    elif any(p in texto for p in ["exemplo", "claro", "aprendizagem", "competência"]):
        return 3, "3 de 4 — O descritor é bom, mas pode ganhar mais força com regionalização e intencionalidade pedagógica."
    elif len(descritor.strip()) == 0:
        return 1, "1 de 4 — Descritor ausente ou insuficiente. Insira um critério claro, contextualizado e descritivo."
    else:
        return 2, "2 de 4 — O descritor é vago ou genérico. Precisa ser mais didático, com exemplos relevantes e aplicabilidade educacional."

# Avaliação de cada linha da rubrica
avaliacoes = []
for idx, row in rubrica_df.iterrows():
    nota, justificativa = avaliar_criterio(row.get("descritor", ""))
    avaliacoes.append({
        "dimensao": row.get("dimensao", ""),
        "nivel": row.get("nivel", ""),
        "descritor": row.get("descritor", ""),
        "nota": nota,
        "avaliacao": justificativa
    })

# Salvar em CSV
output_file = "avaliacao_automatica_rubrica_sinapse_IA_V1.csv"
pd.DataFrame(avaliacoes).to_csv(output_file, index=False)
print(f"✅ Avaliação salva em: {output_file}")

