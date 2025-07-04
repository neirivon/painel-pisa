import geopandas as gpd
import json
import os

# === Caminho correto para o shapefile de microrregiões do IBGE 2015 ===
CAMINHO_SHAPEFILE = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "B")os.path.join(R, "B")RMEE250GC_SIR.shp"))

# === Carrega o shapefile ===
print("📦 Lendo shapefile do IBGE (microrregiões 2015)...")
gdf = gpd.read_file(CAMINHO_SHAPEFILE)

# === Confere colunas disponíveis ===
print("📋 Colunas disponíveis:", list(gdf.columns))

# === Verifica nomes de colunas ===
nome_coluna_micro = "NM_MICRO" if "NM_MICRO" in gdf.columns else "name"
uf_coluna = "SIGLA_UF" if "SIGLA_UF" in gdf.columns else "UF"

# === Cria lista de documentos JSON com geometria em formato WKT ===
print("🧠 Gerando estrutura JSON para MongoDB...")
documentos = []
for _, row in gdf.iterrows():
    doc = {
        "NM_MICRO": row[nome_coluna_micro],
        "SIGLA_UF": row[uf_coluna] if uf_coluna in row else "",
        "geometry": row["geometry"].wkt  # ou __geo_interface__ para GeoJSON
    }
    documentos.append(doc)

# === Caminho para salvar o JSON final ===
OUTPUT_JSON = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "i")bge_microrregioes_2015.json"))

# === Salvar arquivo JSON ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(documentos, f, ensure_ascii=False, indent=2)

# === Mensagem final ===
print(f"\n✅ JSON salvo com sucesso em: {OUTPUT_JSON}")
print(f"📁 Total de microrregiões exportadas: {len(documentos)}")

