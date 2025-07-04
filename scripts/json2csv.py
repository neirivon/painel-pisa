import pandas as pd

# Carrega o JSON em formato "linhas por registro"
df = pd.read_json("pisa_pfd_alunos_limpo.json", lines=True)

# Exporta para CSV com separador vírgula e cabeçalho
df.to_csv("pisa_pfd_alunos_limpo.csv", index=False)

