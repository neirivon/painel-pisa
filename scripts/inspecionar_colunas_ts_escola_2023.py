import pandas as pd

CAMINHO_ESCOLA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
df = pd.read_csv(CAMINHO_ESCOLA, sep=";", encoding="latin1", nrows=5)

print("📋 Colunas disponíveis:")
print(df.columns.tolist())

