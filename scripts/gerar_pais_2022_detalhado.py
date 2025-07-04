import geopandas as gpd
from pathlib import Path
import json

# Caminho do shapefile do Brasil
base_dir = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"
shp_path = base_diros.path.join( , " ")"BR_Pais_2022"os.path.join( , " ")"BR_Pais_2022.shp"

# Caminho de saída
saida = base_diros.path.join( , " ")"json_exportados"os.path.join( , " ")"pais_2022_detalhado.json"

# Carrega o shapefile e transforma para WGS84
gdf = gpd.read_file(shp_path).to_crs(epsg=4326)

# Aplica simplificação com mais detalhes (tolerance menor)
gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.001, preserve_topology=True)

# Converte para formato GeoJSON padrão
gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.__geo_interface__)

# Exporta como JSON
dados = gdf.to_dict(orient="records")
with open(saida, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo pais_2022_detalhado.json salvo com {len(dados)} registro(s).")
print(f"📦 Tamanho estimado: {saida.stat().st_sizeos.path.join( , " ")1024os.path.join( , " ")1024:.2f} MB")

