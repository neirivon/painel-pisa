# gerar_id_municipios_tmap_saeb2023.py

import pandas as pd
import json

# Caminhos
CAMINHO_TMAP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.csv"
CAMINHO_ESCOLAS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_saeb.json"

# 📥 Ler códigos do TMAP
df_tmap = pd.read_csv(CAMINHO_TMAP, dtype=str)
codigos_tmap = df_tmap["codigo_ibge"].str.zfill(7).tolist()

# 📥 Ler microdados SAEB 2023 - ESCOLAS
df_saeb = pd.read_csv(CAMINHO_ESCOLAS, sep=";", encoding="latin1", dtype=str)

# 🔎 Filtrar Minas Gerais
df_saeb_mg = df_saeb[df_saeb["ID_UF"] == "31"].copy()

# 🧠 Garantir que ID_MUNICIPIO está padronizado
df_saeb_mg["ID_MUNICIPIO"] = df_saeb_mg["ID_MUNICIPIO"].str.zfill(7)

# ⚔️ Cruzamento poderoso
ids_encontrados = df_saeb_mg[df_saeb_mg["ID_MUNICIPIO"].isin(codigos_tmap)]["ID_MUNICIPIO"].unique()
ids_encontrados = sorted(ids_encontrados)

# 💾 Salvar JSON
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(ids_encontrados, f, ensure_ascii=False, indent=2)

# ✅ Status
print(f"✅ {len(ids_encontrados)} códigos TMAP encontrados no SAEB 2023.")
print(f"📁 IDs salvos em: {CAMINHO_SAIDA}")

