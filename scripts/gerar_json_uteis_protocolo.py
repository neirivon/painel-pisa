import pandas as pd

# Carrega o CSV que você gerou com a análise completa
df = pd.read_csv("/home/neirivon/SINAPSE2.0/PISA/scripts/analisar_protocolos_pisa.csv")  # ou outro caminho real

# Filtra apenas os arquivos úteis
df_util = df[df["Usável na Página?"] == "Sim"]

# Exporta para JSON
df_util.to_json(
    "/home/neirivon/dados_processados/protocolos/dados_protocolos_utilizaveis.json",
    orient="records",
    indent=2,
    force_ascii=False
)

