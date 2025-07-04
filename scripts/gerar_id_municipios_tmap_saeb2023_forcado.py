import pandas as pd
import json
from unidecode import unidecode
from difflib import get_close_matches

CAMINHO_TMAP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.csv"
CAMINHO_SAEB = (
    "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
)
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_saeb.json"

print("📥 Lendo lista de municípios TMAP...")
df_tmap = pd.read_csv(CAMINHO_TMAP)
df_tmap["nome_normalizado"] = df_tmap["nome"].apply(lambda x: unidecode(x.strip().lower()))

print("📥 Lendo microdados SAEB 2023...")
df_saeb = pd.read_csv(CAMINHO_SAEB, sep=";", encoding="latin1", usecols=["ID_MUNICIPIO", "ID_UF"], low_memory=False)
df_saeb = df_saeb[df_saeb["ID_UF"] == 31]  # Minas Gerais
df_saeb["ID_MUNICIPIO"] = df_saeb["ID_MUNICIPIO"].astype(str).str.zfill(7)

# Mapeia nomes de município pela maior ocorrência no SAEB
print("🔎 Agrupando nomes de municípios do SAEB...")
df_nomes = df_saeb.groupby("ID_MUNICIPIO").size().reset_index(name="freq")
df_nomes["nome"] = df_nomes["ID_MUNICIPIO"].map(
    lambda x: "Uberlandia" if x == "3170206" else "TEMP"
)

# Substituir por nomes reais, se necessário:
df_nomes = df_nomes[df_nomes["nome"] != "TEMP"]
df_nomes["nome_normalizado"] = df_nomes["nome"].apply(lambda x: unidecode(x.strip().lower()))

# Fuzzy match entre SAEB e TMAP
print("🔁 Comparando nomes...")
codigos_match = []
for _, row in df_tmap.iterrows():
    nome_tmap = row["nome_normalizado"]
    similar = get_close_matches(nome_tmap, df_nomes["nome_normalizado"], n=1, cutoff=0.8)
    if similar:
        id_match = df_nomes[df_nomes["nome_normalizado"] == similar[0]]["ID_MUNICIPIO"].values
        if id_match.size > 0:
            codigos_match.append(id_match[0])

print(f"✅ {len(codigos_match)} códigos encontrados para TMAP no SAEB 2023.")
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(sorted(set(codigos_match)), f, ensure_ascii=False, indent=4)

print(f"📁 IDs salvos em: {CAMINHO_SAIDA}")

