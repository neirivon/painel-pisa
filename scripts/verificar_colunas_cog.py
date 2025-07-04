# verificar_colunas_cog.py
import pandas as pd

CAMINHO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_coos.path.join(g, "p")isa2022_ms_cog_overall_math_compendium.xlsx"

df = pd.read_excel(CAMINHO)
print("📌 Colunas detectadas:")
print(df.columns.tolist())
print("\n🧪 Primeiras linhas:")
print(df.head(10))

