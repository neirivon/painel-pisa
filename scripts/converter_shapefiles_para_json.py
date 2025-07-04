import geopandas as gpd
from pathlib import Path

# Diretório base
base_dir = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"

# Shapefiles a serem processados
shapefiles = {
    "municipios_2022": base_diros.path.join( , " ")"BR_Municipios_2022"os.path.join( , " ")"BR_Municipios_2022.shp",
    "regioes_imediatas_2022": base_diros.path.join( , " ")"BR_RG_Imediatas_2022"os.path.join( , " ")"BR_RG_Imediatas_2022.shp",
    "regioes_intermediarias_2022": base_diros.path.join( , " ")"BR_RG_Intermediarias_2022"os.path.join( , " ")"BR_RG_Intermediarias_2022.shp",
    "ufs_2022": base_diros.path.join( , " ")"BR_UF_2022"os.path.join( , " ")"BR_UF_2022.shp",
    "regioes_2022": base_diros.path.join( , " ")"BR_Regioes_2022"os.path.join( , " ")"BR_Regioes_2022.shp",
    "pais_2022": base_diros.path.join( , " ")"BR_Pais_2022"os.path.join( , " ")"BR_Pais_2022.shp"
}

# Pasta de saída dos arquivos JSON
output_dir = base_diros.path.join( , " ")"json_exportados"
output_dir.mkdir(parents=True, exist_ok=True)

# Processar e salvar cada shapefile como JSON
for nome, caminho in shapefiles.items():
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        continue

    print(f"📄 Processando: {nome}")
    try:
        gdf = gpd.read_file(caminho)
        gdf = gdf.to_crs(epsg=4326)  # Garantir coordenadas em WGS84
        gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.__geo_interface__)
        data = gdf.to_dict(orient="records")

        json_path = output_diros.path.join( , " ")f"{nome}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Exportado: {json_path.name} com {len(data)} registros")
    except Exception as e:
        print(f"❌ Erro ao processar {nome}: {e}")

