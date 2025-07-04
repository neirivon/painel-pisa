import pandas as pd

CAMINHO_ARQUIVO = (
    "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
)

print("📥 Lendo primeiras linhas para inspecionar colunas...")
df = pd.read_csv(CAMINHO_ARQUIVO, sep=";", encoding="latin1", nrows=5)

print("\n🧾 Colunas disponíveis no arquivo:")
for col in df.columns:
    print(f"- {col}")

