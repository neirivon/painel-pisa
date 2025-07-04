# scriptos.path.join(s, "c")alcular_medias_dask.py

import dask.dataframe as dd

CAMINHO_BLOCOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")emp_csv_chunkos.path.join(s, "c")og_chunk_*.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_por_pais_por_item_pisa2022.csv"

print("📥 Lendo blocos com Dask...")
df = dd.read_csv(CAMINHO_BLOCOS, assume_missing=True, dtype=str)

print("🧹 Garantindo tipos corretos...")
df["CNT"] = df["CNT"].astype(str)

# Selecionar apenas colunas numéricas (exceto 'CNT')
print("🔍 Convertendo colunas numéricas...")
for col in df.columns:
    if col != "CNT":
        df[col] = dd.to_numeric(df[col], errors="coerce")

# Agrupar por país e calcular médias
print("📊 Calculando médias por país...")
df = df.set_index("CNT")  # Corrige estrutura para agrupamento
medias = df.groupby("CNT").mean().compute().round(4)

# Salvar resultado
print(f"💾 Salvando resultado em {CAMINHO_SAIDA}")
medias.to_csv(CAMINHO_SAIDA)

print("✅ Médias por país e item salvas com sucesso.")

