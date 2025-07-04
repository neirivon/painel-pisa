import geopandas as gpd
import json

# === CAMINHOS ===
path_ce = os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "C")E_IBGE_201os.path.join(5, "c")e_microrregioeos.path.join(s, "2")3MIE250GC_SIR.shp")
path_ma = os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp")

# === CEARÁ ===
gdf_ce = gpd.read_file(path_ce)[["NM_MICRO", "CD_GEOCMI", "geometry"]]
gdf_ce["UF"] = "CE"
gdf_ce["geometry"] = gdf_ce["geometry"].apply(lambda g: g.__geo_interface__)
json_ce = gdf_ce.to_dict(orient="records")

with open("ce_microrregioes_2015.json", "w", encoding="utf-8") as f:
    json.dump(json_ce, f, ensure_ascii=False, indent=2)

# === MARANHÃO ===
gdf_ma = gpd.read_file(path_ma)[["NM_MICRO", "CD_GEOCMI", "geometry"]]
gdf_ma["UF"] = "MA"
gdf_ma["geometry"] = gdf_ma["geometry"].apply(lambda g: g.__geo_interface__)
json_ma = gdf_ma.to_dict(orient="records")

with open("ma_microrregioes_2015.json", "w", encoding="utf-8") as f:
    json.dump(json_ma, f, ensure_ascii=False, indent=2)

print("✅ JSONs formatados corretamente como array para mongoimport.")

