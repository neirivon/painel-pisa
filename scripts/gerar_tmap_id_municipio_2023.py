import pandas as pd
import json

# Caminhos
CAMINHO_TMAP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.csv"
CAMINHO_ESCOLAS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023.json"

# Carrega os dados
df_tmap = pd.read_csv(CAMINHO_TMAP)
df_escola = pd.read_csv(CAMINHO_ESCOLAS, sep=";", encoding="latin1", low_memory=False)

# Normaliza nomes
df_tmap["nome"] = df_tmap["nome"].str.strip().str.upper()

# Filtra só MG e extrai ID_MUNICIPIO onde o nome da cidade coincide com o nome TMAP
df_mg = df_escola[df_escola["ID_UF"] == 31].copy()
df_mg["NOME_NORMALIZADO"] = df_mg["ID_MUNICIPIO"].astype(str)  # referência
df_merged = df_mg.merge(df_tmap, left_on="ID_MUNICIPIO", right_on="codigo_ibge", how="inner")

# Pega os códigos únicos
ids_tmap = sorted(df_merged["ID_MUNICIPIO"].astype(str).unique())

# Salva JSON
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(ids_tmap, f, indent=4, ensure_ascii=False)

print(f"✅ {len(ids_tmap)} códigos de municípios TMAP salvos em {CAMINHO_SAIDA}")

