import geopandas as gpd
import os

shapefile_path = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "A")L_IBGE_201os.path.join(5, "2")7MIE250GC_SIR.shp"))

gdf_micro = gpd.read_file(shapefile_path)
print(gdf_micro.columns)
print(gdf_micro.head())

