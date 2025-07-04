import pyreadstat

# Caminho até o arquivo SPSS que deseja explorar
arquivo_sav = "CY1MDAI_STU_QQQ.sav"

# Leitura do arquivo
df, meta = pyreadstat.read_sav(arquivo_sav)

# Visualização inicial
print("✅ Primeiras linhas do arquivo:")
print(df.head())

print("\n🧩 Colunas disponíveis:")
print(df.columns.tolist())

print("\n📊 Tipos de dados:")
print(df.dtypes)

