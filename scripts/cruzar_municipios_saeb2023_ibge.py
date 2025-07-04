# scriptos.path.join(s, "c")ruzar_municipios_saeb2023_ibge.py

import pandas as pd
import json

CAMINHO_SAEB = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
CAMINHO_TMAP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_saeb.json"

print("📥 Lendo dados do SAEB 2023 (TS_ESCOLA)...")
df_saeb = pd.read_csv(CAMINHO_SAEB, sep=";", encoding="latin1", usecols=["ID_UF", "ID_MUNICIPIO"])
df_saeb = df_saeb[df_saeb["ID_UF"] == 31]
df_saeb["ID_MUNICIPIO"] = df_saeb["ID_MUNICIPIO"].astype(str)

print("📥 Lendo lista oficial de municípios da mesorregião TMAP...")
df_tmap = pd.read_csv(CAMINHO_TMAP)
df_tmap["codigo_ibge"] = df_tmap["codigo_ibge"].astype(str)

print("🔍 Cruzando os dados...")
codigos_tmap_saeb = df_saeb[df_saeb["ID_MUNICIPIO"].isin(df_tmap["codigo_ibge"])]["ID_MUNICIPIO"].unique()

print(f"✅ {len(codigos_tmap_saeb)} códigos encontrados para TMAP no SAEB 2023.")

print(f"💾 Salvando em: {CAMINHO_SAIDA}")
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(sorted(codigos_tmap_saeb.tolist()), f, ensure_ascii=False, indent=4)

print("🎯 Pronto! IDs compatíveis com o SAEB 2023 salvos com sucesso.")

