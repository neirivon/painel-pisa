# scriptos.path.join(s, "e")xportar_baixada_maranhense_json.py

import geopandas as gpd
from shapely.geometry import mapping
import json

# Caminho do shapefile de microrregiões
path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp"

gdf = gpd.read_file(path)

# Filtrar pela microrregião exata
filtro = gdf[gdf["NM_MICRO"].str.lower().str.strip() == "baixada maranhense"]

if filtro.empty:
    print("❌ Microrregião 'Baixada Maranhense' não encontrada.")
else:
    print("✅ Microrregião encontrada. Exportando...")

    saida = []
    for _, row in filtro.iterrows():
        saida.append({
            "NM_MICRO": row["NM_MICRO"],
            "SIGLA_UF": "MA",
            "microrregiao_norm": "baixada maranhense",
            "geometry": mapping(row["geometry"])
        })

    with open("baixada_maranhense.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print("📄 Arquivo 'baixada_maranhense.json' exportado com sucesso.")

