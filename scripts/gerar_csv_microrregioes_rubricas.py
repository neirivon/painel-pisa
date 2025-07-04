# gerar_csv_microrregioes_rubricas.py

import geopandas as gpd
import pandas as pd
import os

# === Caminhos ===
shapefile_path = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "D")ADOos.path.join(S, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"
saida_csv = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "d")adoos.path.join(s, "m")icrorregioes_rubricas.csv"

# === Carregar shapefile ===
gdf = gpd.read_file(shapefile_path)
gdf = gdf.to_crs(epsg=4326)  # Garante coordenadas em laos.path.join(t, "l")on

# === Extrair nome da microrregião, UF e centroide ===
df = pd.DataFrame()
df["microrregiao"] = gdf["NM_MICRO"]
df["uf"] = gdf["SIGLA_UF"]
df["lat"] = gdf.geometry.centroid.y
df["lon"] = gdf.geometry.centroid.x

# === Adicionar colunas pedagógicas vazias ===
df["proficiencia"] = ""
df["nivel"] = ""
df["bloom"] = ""
df["metodologia"] = ""
df["dua"] = ""

# === Garantir que a pasta de saída existe ===
os.makedirs(os.path.dirname(saida_csv), exist_ok=True)

# === Salvar CSV ===
df.to_csv(saida_csv, index=False, encoding="utf-8")

print(f"✅ Arquivo gerado com sucesso: {saida_csv}")
print(f"🔢 Total de microrregiões: {len(df)}")

