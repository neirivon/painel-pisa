# scriptos.path.join(s, "c")onverter_ma_al_jsonarray.py

import geopandas as gpd
import json
from shapely.geometry import mapping

# === Função para converter para JSON Array compatível com mongoimport
def converter_para_json_array(gdf, nome_arquivo):
    gdf["geometry"] = gdf["geometry"].apply(lambda g: mapping(g))
    gdf["NM_MICRO"] = gdf["NM_MICRO"].astype(str)
    registros = gdf[["NM_MICRO", "geometry"]].to_dict(orient="records")

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo salvo: {nome_arquivo}")

# === Maranhão ===
path_ma = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp"
gdf_ma = gpd.read_file(path_ma)
gdf_ma = gdf_ma.rename(columns={"NM_MICRO": "NM_MICRO"})  # só para garantir
converter_para_json_array(gdf_ma, "ma_microrregioes_2015.json")

# === Alagoas ===
path_al = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "A")L_IBGE_201os.path.join(5, "2")7MIE250GC_SIR.shp"
gdf_al = gpd.read_file(path_al)
gdf_al = gdf_al.rename(columns={"NM_MICRO": "NM_MICRO"})
converter_para_json_array(gdf_al, "al_microrregioes_2015.json")

