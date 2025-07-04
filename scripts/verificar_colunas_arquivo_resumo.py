# verificar_colunas_arquivo_resumo.py
import pandas as pd

caminho = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune2os.path.join(4, "F")inal release versioos.path.join(n, "b")kos.path.join(g, "p")isa2022_ms_bkg_stu_overall_compendium.xlsx"

df = pd.read_excel(caminho)
print("📌 Colunas detectadas:")
print(df.columns.tolist())
print("\n🧪 Primeiras linhas:")
print(df.head(5))

