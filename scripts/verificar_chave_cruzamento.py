import pandas as pd

# === Caminhos ===
CAMINHO_ALUNOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
CAMINHO_CENSO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "m")icrodados_censo_escolar_202os.path.join(3, "d")adoos.path.join(s, "m")icrodados_ed_basica_2023.csv"

# === Carregar colunas necessárias ===
df_alunos = pd.read_csv(CAMINHO_ALUNOS, sep=";", encoding="latin1", usecols=["ID_ESCOLA"])
df_censo = pd.read_csv(CAMINHO_CENSO, sep=";", encoding="latin1", usecols=["CO_ENTIDADE"])
df_censo = df_censo.rename(columns={"CO_ENTIDADE": "ID_ESCOLA"})

# === Verificar interseção entre IDs ===
print("📊 Linhas SAEB:", len(df_alunos))
print("📊 Linhas CENSO:", len(df_censo))

intersecao = set(df_alunos["ID_ESCOLA"]).intersection(set(df_censo["ID_ESCOLA"]))
print("🔍 Interseção de ID_ESCOLA:", len(intersecao))

# Se desejar ver amostras:
print("\n🔎 Exemplo de IDs comuns (até 10):")
print(list(intersecao)[:10])

