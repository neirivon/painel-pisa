import pandas as pd

# === Caminhos absolutos ===
CAMINHO_ALUNOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
CAMINHO_ESCOLAS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "r")anking_saeb2023_codigos_ficticios.csv"

# === Leitura dos dados ===
print("📥 Lendo dados de alunos e escolas do SAEB 2023...")
df_alunos = pd.read_csv(CAMINHO_ALUNOS, sep=";", encoding="latin1", usecols=[
    "ID_ESCOLA", "PROFICIENCIA_MT_SAEB", "PROFICIENCIA_LP_SAEB"
])
df_escolas = pd.read_csv(CAMINHO_ESCOLAS, sep=";", encoding="latin1", usecols=[
    "ID_ESCOLA", "ID_MUNICIPIO", "ID_UF"
])
df_escolas = df_escolas.rename(columns={
    "ID_MUNICIPIO": "ID_MUNICIPIO_escola",
    "ID_UF": "ID_UF_escola"
})

# === Merge entre aluno e escola ===
print("🔗 Relacionando dados por ID_ESCOLA...")
df_merge = pd.merge(df_alunos, df_escolas, on="ID_ESCOLA", how="inner")

# === Filtrar apenas dados válidos de proficiência ===
print("🧹 Filtrando registros com proficiência válida...")
df_merge = df_merge.dropna(subset=["PROFICIENCIA_MT_SAEB", "PROFICIENCIA_LP_SAEB"])
df_merge = df_merge[
    (df_merge["PROFICIENCIA_MT_SAEB"] > 0) &
    (df_merge["PROFICIENCIA_LP_SAEB"] > 0)
]

# === Agrupar por município fictício e UF ===
print("📊 Agrupando por município fictício (ID_MUNICIPIO_escola)...")
df_agrupado = df_merge.groupby(["ID_MUNICIPIO_escola", "ID_UF_escola"]).agg({
    "PROFICIENCIA_MT_SAEB": "mean",
    "PROFICIENCIA_LP_SAEB": "mean"
}).reset_index()

# === Exportar CSV ===
print(f"💾 Salvando em: {CAMINHO_SAIDA}")
df_agrupado.to_csv(CAMINHO_SAIDA, index=False)
print("✅ Arquivo gerado com sucesso!")

