import json
from unidecode import unidecode

CAMINHO_TMAP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap_lista.json"
CAMINHO_MAPEAMENTO_SAEB = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")dmunicipio_nome_saeb2023.json"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_saeb.json"

print("📥 Lendo lista de municípios TMAP...")
with open(CAMINHO_TMAP, "r", encoding="utf-8") as f:
    municipios_tmap = json.load(f)

print("📥 Lendo mapeamento do SAEB 2023...")
with open(CAMINHO_MAPEAMENTO_SAEB, "r", encoding="utf-8") as f:
    mapeamento_saeb = json.load(f)

print("🔁 Normalizando e cruzando nomes...")
def normalizar(nome):
    return unidecode(nome.lower().strip())

tmap_codigos = []

for mun in municipios_tmap:
    nome_normalizado = normalizar(mun["nome"])
    for nome_saeb, id_mun in mapeamento_saeb.items():
        if normalizar(nome_saeb) == nome_normalizado:
            tmap_codigos.append(id_mun)
            break

print(f"✅ {len(tmap_codigos)} códigos encontrados para TMAP no SAEB 2023.")
print(f"📁 IDs salvos em: {CAMINHO_SAIDA}")

with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(sorted(tmap_codigos), f, indent=2, ensure_ascii=False)

