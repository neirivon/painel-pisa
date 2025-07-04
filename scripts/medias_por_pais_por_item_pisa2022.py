# scriptos.path.join(s, "m")edias_por_pais_por_item_pisa2022.py

import pandas as pd
import pyreadstat
from tqdm import tqdm

CAMINHO_SAV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "D")ADOos.path.join(S, "2")02os.path.join(2, "C")Y08MSP_STU_COG.SAV"
ARQUIVO_SAIDA = "medias_por_pais_por_item_pisa2022.csv"

print("📦 Lendo arquivo .SAV... Isso pode levar alguns minutos.")
df, meta = pyreadstat.read_sav(CAMINHO_SAV)

print("🔍 Filtrando colunas...")
colunas_items = [col for col in df.columns if col not in ['CNT', 'STIDSTD', 'BOOKID']]
df_filtrado = df[['CNT'] + colunas_items]

print("📊 Calculando médias por país por item...")
paises = df_filtrado['CNT'].unique()
resultado = {}

for pais in tqdm(paises, desc="Processando países"):
    df_pais = df_filtrado[df_filtrado['CNT'] == pais]
    medias = df_pais[colunas_items].mean(numeric_only=True).round(4).to_dict()
    resultado[pais] = medias

print("💾 Salvando em CSV...")
df_resultado = pd.DataFrame.from_dict(resultado, orient='index')
df_resultado.index.name = "codigo_pais"
df_resultado.reset_index(inplace=True)
df_resultado.to_csv(ARQUIVO_SAIDA, index=False)

print(f"✅ Exportado com sucesso para {ARQUIVO_SAIDA}")

