import geopandas as gpd

# Caminho real
path_ce = os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "C")E_IBGE_201os.path.join(5, "c")e_microrregioeos.path.join(s, "2")3MIE250GC_SIR.shp")

# Carregar sem filtrar colunas
gdf = gpd.read_file(path_ce)

# Mostrar colunas e amostras
print("✅ Colunas disponíveis:")
print(gdf.columns)

print("\n🧪 Primeiras linhas:")
print(gdf.head())
