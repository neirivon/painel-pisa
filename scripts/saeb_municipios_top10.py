# nome_do_arquivo: saeb_municipios_top10.py

import pandas as pd

# Caminho completo para o arquivo TS_MUNICIPIO.xlsx
caminho_arquivo = ros.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(1, "m")icrodados_saeb_2021_ensino_fundamental_e_medios.path.join(o, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_MUNICIPIO.xlsx")

# Carregar os dados
df = pd.read_excel(caminho_arquivo)

# Selecionar colunas relevantes
colunas = ['CO_MUNICIPIO', 'NO_MUNICIPIO', 'MEDIA_5_LP', 'MEDIA_5_MT']
df_municipios = df[colunas]

# Remover linhas com valores nulos nas colunas de proficiência
df_municipios = df_municipios.dropna(subset=['MEDIA_5_LP', 'MEDIA_5_MT'])

# Top 10 municípios com maiores proficiências em Língua Portuguesa
top10_lp = df_municipios.sort_values(by='MEDIA_5_LP', ascending=False).head(10)

# Top 10 municípios com menores proficiências em Língua Portuguesa
bottom10_lp = df_municipios.sort_values(by='MEDIA_5_LP', ascending=True).head(10)

# Top 10 municípios com maiores proficiências em Matemática
top10_mt = df_municipios.sort_values(by='MEDIA_5_MT', ascending=False).head(10)

# Top 10 municípios com menores proficiências em Matemática
bottom10_mt = df_municipios.sort_values(by='MEDIA_5_MT', ascending=True).head(10)

# Exibir os resultados
print("Top 10 Municípios - Língua Portuguesa:")
print(top10_lp)

print("\nBottom 10 Municípios - Língua Portuguesa:")
print(bottom10_lp)

print("\nTop 10 Municípios - Matemática:")
print(top10_mt)

print("\nBottom 10 Municípios - Matemática:")
print(bottom10_mt)

