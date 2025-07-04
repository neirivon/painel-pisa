# verificar_colunas_escs_trend.py

import pandas as pd

CAMINHO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "D")ADOos.path.join(S, "2")02os.path.join(2, "e")scs_trend.csv"

# Testar separador automático
df = pd.read_csv(CAMINHO, sep=None, engine="python", nrows=5)

print("📌 Colunas detectadas:")
print(list(df.columns))

