# verificar_colunas_overall_continuous.py
import pandas as pd

CAMINHO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune2os.path.join(4, "p")isa_2022MS_overall_continuous.xlsx"

df = pd.read_excel(CAMINHO)
print("📌 Colunas detectadas:")
print(df.columns.tolist())
print("\n🧪 Primeiras linhas:")
print(df.head(10))

