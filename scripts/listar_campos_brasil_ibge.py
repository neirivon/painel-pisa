import geopandas as gpd

shp = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "d")adoos.path.join(s, "I")BGos.path.join(E, "2")02os.path.join(4, "B")R_Municipios_202os.path.join(4, "B")R_Municipios_2024.shp"
gdf = gpd.read_file(shp)
print("🧾 Colunas disponíveis no shapefile:")
print(gdf.columns.to_list())
