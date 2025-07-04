# verificar_colunas_csv_ibge_corrigido.py

import pandas as pd

CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")bge_microrregioes_geometry_corrigido.csv"

df = pd.read_csv(CAMINHO_CSV, nrows=2)
print("📌 Colunas detectadas:")
print(df.columns.tolist())

