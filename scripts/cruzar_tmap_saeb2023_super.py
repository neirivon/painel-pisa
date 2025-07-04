# scriptos.path.join(s, "c")ruzar_tmap_saeb2023_super.py

import pandas as pd
import json
from unidecode import unidecode
from pathlib import Path

# Caminhos
CAMINHO_TMAP = Path("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.csv")
CAMINHO_ESCOLA = Path("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv")
CAMINHO_SAIDA = Path("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_saeb_super.json")

# Função para normalizar nomes
def normalizar(nome):
    return unidecode(str(nome)).lower().strip().replace("-", " ").replace("'", "")

# Carrega lista de municípios da mesorregião TMAP
df_tmap = pd.read_csv(CAMINHO_TMAP)
df_tmap["nome_normalizado"] = df_tmap["nome"].apply(normalizar)

# Carrega dados das escolas (onde estão os ID_MUNICIPIO fictícios)
df_saeb = pd.read_csv(CAMINHO_ESCOLA, sep=";", encoding="latin1")
col_nome = next((c for c in df_saeb.columns if "NOME" in c.upper()), None)
col_idmun = "ID_MUNICIPIO"

# Gera nomes fictícios com base no ID_MUNICIPIO para emparelhamento forçado
df_saeb["nome_ficticio"] = "mun_" + df_saeb[col_idmun].astype(str)

# Cruzamento forçado
mapeamento = {}
for nome_tmap in df_tmap["nome_normalizado"]:
    for idx, linha_saeb in df_saeb.iterrows():
        if nome_tmap in linha_saeb["nome_ficticio"]:
            mapeamento[linha_saeb[col_idmun]] = nome_tmap
            break

# Salva como JSON
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(mapeamento, f, ensure_ascii=False, indent=4)

print(f"✅ {len(mapeamento)} códigos mapeados salvos em: {CAMINHO_SAIDA}")

