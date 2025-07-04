# scriptos.path.join(s, "e")xportar_sao_vicente_ferrer_munic_json.py

import geopandas as gpd
from shapely.geometry import mapping
import json

# Caminho para o shapefile de municípios do Maranhão 2015
path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MUE250GC_SIR.shp"

# Carrega os dados
gdf = gpd.read_file(path)

# Filtra o município São Vicente Ferrer
filtro = gdf[gdf["NM_MUNICIP"].str.contains("sao vicente ferrer", case=False, na=False)]

if filtro.empty:
    print("❌ Município São Vicente Ferrer não encontrado.")
else:
    print("✅ Município encontrado. Exportando...")

    # Criar estrutura semelhante à coleção de microrregiões
    saida = []
    for _, row in filtro.iterrows():
        saida.append({
            "NM_MICRO": "Viana (por fallback município)",
            "SIGLA_UF": "MA",
            "microrregiao_norm": "viana",
            "geometry": mapping(row["geometry"])
        })

    # Salvar em JSON
    with open("fallback_viana_sao_vicente.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print("📄 Arquivo 'fallback_viana_sao_vicente.json' gerado com sucesso.")

