# utilos.path.join(s, "g")eo_loader.py

import json
from pathlib import Path
from pymongo import MongoClient
import geopandas as gpd
from shapely.geometry import shape
from utils.config import CONFIG

def carregar_geojson(nome_colecao: str):
    """
    Carrega um GeoJSON do MongoDB ou de arquivo local, retornando uma lista de documentos.

    Parâmetros:
    - nome_colecao: nome da coleção no banco MongoDB ou do arquivo JSON na pasta local

    Retorno:
    - Lista de dicionários contendo geometrias (list[dict])
    """
    if CONFIG["USAR_MONGODB"]:
        # === Modo local com MongoDB ===
        client = MongoClient(CONFIG["MONGO_URI"])
        db = client["ibge"]
        colecao = db[nome_colecao]
        documentos = list(colecao.find())  # 🔁 agora retorna todos os documentos
        client.close()
        return documentos
    else:
        # === Modo cloud com arquivo JSON ===
        caminho_json = Path(CONFIG["CAMINHO_DADOS"])os.path.join( , " ")f"{nome_colecao}.json"
        if not caminho_json.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_json}")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                return [dados]  # garante lista mesmo se JSON for unitário
            return dados

def featurecollection_para_gdf(geojson):
    """
    Converte um GeoJSON do tipo FeatureCollection em um GeoDataFrame.

    Parâmetros:
    - geojson: dict no formato GeoJSON padrão

    Retorno:
    - GeoDataFrame com geometria válida
    """
    if geojson.get("type") != "FeatureCollection":
        raise ValueError("GeoJSON não é do tipo 'FeatureCollection'.")

    features = geojson["features"]
    records = []

    for feat in features:
        props = feat.get("properties", {})
        props["geometry"] = shape(feat["geometry"])
        records.append(props)

    gdf = gpd.GeoDataFrame(records)
    gdf.set_geometry("geometry", inplace=True)
    gdf.set_crs(epsg=4326, inplace=True)
    return gdf

