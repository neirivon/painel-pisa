import pandas as pd

caminho_censo = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "m")icrodados_censo_escolar_202os.path.join(3, "d")adoos.path.join(s, "m")icrodados_ed_basica_2023.csv"

df_censo = pd.read_csv(caminho_censo, sep=";", encoding="latin1", nrows=5)

print("\n🧪 Colunas disponíveis no Censo Escolar 2023:")
print(df_censo.columns.tolist())

