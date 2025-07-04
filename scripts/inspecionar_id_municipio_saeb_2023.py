# inspecionar_id_municipio_saeb_2023.py

import pandas as pd

CAMINHO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"

df = pd.read_csv(CAMINHO, sep=";", encoding="latin1", usecols=["ID_MUNICIPIO"])
df["ID_MUNICIPIO"] = df["ID_MUNICIPIO"].astype(str)

print("🔢 Quantidade de municípios únicos:", df["ID_MUNICIPIO"].nunique())
print("📋 Exemplos:", df["ID_MUNICIPIO"].unique()[:10])

