import os
import pandas as pd

# === Caminhos dos arquivos ===
CAMINHO_ALUNOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
CAMINHO_ESCOLAS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
CAMINHO_CENSO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "m")icrodados_censo_escolar_202os.path.join(3, "d")adoos.path.join(s, "m")icrodados_ed_basica_2023.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "r")anking_saeb2023_municipios_reais.csv"

# === Carregar dados do SAEB (alunos e escolas) ===
print("📥 Lendo dados do SAEB 2023...")
df_alunos = pd.read_csv(CAMINHO_ALUNOS, sep=";", encoding="latin1", usecols=[
    "ID_ESCOLA", "PROFICIENCIA_MT_SAEB", "PROFICIENCIA_LP_SAEB"
])
df_escolas = pd.read_csv(CAMINHO_ESCOLAS, sep=";", encoding="latin1", usecols=["ID_ESCOLA"])

# === Carregar dados do Censo Escolar com nomes reais ===
print("📥 Lendo dados do Censo Escolar 2023...")
df_censo = pd.read_csv(CAMINHO_CENSO, sep=";", encoding="latin1", usecols=[
    "CO_ENTIDADE", "CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF"
])
df_censo = df_censo.rename(columns={"CO_ENTIDADE": "ID_ESCOLA"})

# === Cruzar os dados via ID_ESCOLA ===
print("🔗 Cruzando SAEB com Censo Escolar...")
df_merge = pd.merge(df_alunos, df_censo, on="ID_ESCOLA", how="inner")

# === Remover dados inválidos (nota 0 ou NaN) ===
print("🧹 Limpando dados inválidos...")
df_merge = df_merge.dropna(subset=["PROFICIENCIA_MT_SAEB", "PROFICIENCIA_LP_SAEB"])
df_merge = df_merge[(df_merge["PROFICIENCIA_MT_SAEB"] > 0) & (df_merge["PROFICIENCIA_LP_SAEB"] > 0)]

# === Agrupar por município real ===
print("📊 Calculando médias por município real...")
df_agrupado = df_merge.groupby(["CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF"]).agg({
    "PROFICIENCIA_MT_SAEB": "mean",
    "PROFICIENCIA_LP_SAEB": "mean"
}).reset_index()

# === Ordenar pelo desempenho em matemática (opcional) ===
df_agrupado = df_agrupado.sort_values("PROFICIENCIA_MT_SAEB", ascending=False)

# === Exportar CSV ===
print(f"💾 Salvando arquivo em: {CAMINHO_SAIDA}")
df_agrupado.to_csv(CAMINHO_SAIDA, index=False)

print("\n✅ Arquivo gerado com sucesso: ranking_saeb2023_municipios_reais.csv")

