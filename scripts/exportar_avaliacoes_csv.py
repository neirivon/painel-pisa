import json
import pandas as pd

# Caminho do JSON exportado anteriormente
CAMINHO_JSON = "dados_processados/rubricas/avaliacoes_rubricas_referenciais.json"
CAMINHO_CSV = "dados_processados/rubricas/avaliacoes_rubricas_referenciais.csv"

# Carregar JSON
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Converter para DataFrame e salvar como CSV
df = pd.DataFrame(dados)
df.to_csv(CAMINHO_CSV, index=False, encoding="utf-8")

print(f"✅ Exportado para {CAMINHO_CSV}")

