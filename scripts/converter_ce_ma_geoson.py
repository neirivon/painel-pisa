import geopandas as gpd

# === CAMINHOS CORRETOS ===
path_ce = os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "C")E_IBGE_201os.path.join(5, "c")e_microrregioeos.path.join(s, "2")3MIE250GC_SIR.shp")
path_ma = os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp")

# === LEITURA E EXPORTAÇÃO CEARÁ (GeoJSON) ===
gdf_ce = gpd.read_file(path_ce)[["NM_MICRO", "CD_GEOCMI", "geometry"]]
gdf_ce["UF"] = "CE"
gdf_ce.to_file("ce_microrregioes_2015.geojson", driver="GeoJSON")

# === LEITURA E EXPORTAÇÃO MARANHÃO (GeoJSON) ===
gdf_ma = gpd.read_file(path_ma)[["NM_MICRO", "CD_GEOCMI", "geometry"]]
gdf_ma["UF"] = "MA"
gdf_ma.to_file("ma_microrregioes_2015.geojson", driver="GeoJSON")


print("✅ Arquivos GeoJSON gerados com sucesso:")
print(" - ce_microrregioes_2015.geojson")
print(" - ma_microrregioes_2015.geojson")

