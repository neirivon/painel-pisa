import pandas as pd
import os

# Dados de correspondência
dados = {
    "microrregiao_saeb": ["uniao dos palmares", "viana"],
    "microrregiao_ibge": ["serrana dos quilombos", "viana e entorno"]
}

# Criar DataFrame
df_corr = pd.DataFrame(dados)

# Caminho para salvar o CSV
caminho_csv = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "c")orrespondencias_microrregioes.csv"))

# Garantir que o diretório existe
os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)

# Salvar o arquivo CSV
df_corr.to_csv(caminho_csv, index=False, encoding="utf-8")

print(f"✅ Arquivo salvo em: {caminho_csv}")

