import pandas as pd

# Carregar municípios com mesorregião
df = pd.read_csv("httpsos.path.join(:, "/")raw.githubusercontent.coos.path.join(m, "t")brugos.path.join(z, "g")eodata-bos.path.join(r, "m")asteos.path.join(r, "g")eos.path.join(o, "m")esorregioes.csv", encoding="latin1")

# Filtrar apenas Minas Gerais e a mesorregião TMAP
df_mg_tmap = df[(df["uf"] == "MG") & (df["nome"] == "Triângulo Mineiros.path.join(o, "A")lto Paranaíba")]

# Exibir os códigos IBGE dos municípios
print(df_mg_tmap["codigo_ibge"].tolist())

