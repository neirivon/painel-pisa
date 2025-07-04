import pandas as pd

CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"

df = pd.read_csv(CAMINHO_CSV, sep=";", encoding="latin1", dtype=str, low_memory=False)
print(df["ID_MUNICIPIO"].unique()[:10])  # Mostra os 10 primeiros

