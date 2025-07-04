import pandas as pd

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "p")isa_2022MS_overall_continuous.xlsx"


df = pd.read_excel(CAMINHO_ARQUIVO)
print("📌 Colunas disponíveis no arquivo:")
print(df.columns.tolist())

