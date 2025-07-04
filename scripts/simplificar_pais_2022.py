import geopandas as gpd
from pathlib import Path
import json

# Caminho do shapefile original
base_dir = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"
shp_path = base_diros.path.join( , " ")"BR_Pais_2022"os.path.join( , " ")"BR_Pais_2022.shp"

# Caminho de saída
saida = base_diros.path.join( , " ")"json_exportados"os.path.join( , " ")"pais_2022_simplificado.json"

# Carregar shapefile e transformar para WGS84
gdf = gpd.read_file(shp_path).to_crs(epsg=4326)

# Aplicar simplificação da geometria com tolerância
gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.01, preserve_topology=True)

# Converter geometria para GeoJSON padrão
gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.__geo_interface__)

# Exportar para JSON simplificado
dados = gdf.to_dict(orient="records")
with open(saida, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo simplificado salvo em: {saida}")
print(f"📦 Tamanho estimado (JSON): {saida.stat().st_sizeos.path.join( , " ")1024os.path.join( , " ")1024:.2f} MB")

