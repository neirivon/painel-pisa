import geopandas as gpd
import matplotlib.pyplot as plt

# === Caminhos corrigidos
shp_micros_2022 = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "D")ADOos.path.join(S, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"
shp_imediatas_2024 = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "d")adoos.path.join(s, "I")BGos.path.join(E, "2")02os.path.join(4, "B")R_Municipios_202os.path.join(4, "B")R_Municipios_2024.shp"

# === Carregar shapefiles
gdf_micros = gpd.read_file(shp_micros_2022)
gdf_imediatas = gpd.read_file(shp_imediatas_2024)

# === Garantir CRS compatível
gdf_micros = gdf_micros.to_crs(epsg=4674)
gdf_imediatas = gdf_imediatas.to_crs(epsg=4674)

# === Plotar lado a lado
fig, axs = plt.subplots(1, 2, figsize=(20, 10))

# Mapa antigo: microrregiões
gdf_micros.boundary.plot(ax=axs[0], linewidth=0.5, color="blue")
axs[0].set_title("Divisão Antiga — Microrregiões (IBGE)", fontsize=14)
axs[0].axis("off")

# Mapa novo: regiões imediatas (por município)
gdf_imediatas.boundary.plot(ax=axs[1], linewidth=0.5, color="green")
axs[1].set_title("Divisão Atual — Regiões Imediatas (IBGE 2024)", fontsize=14)
axs[1].axis("off")

# === Salvar imagem
plt.tight_layout()
output_path = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "a")ssetos.path.join(s, "c")omparacao_divisoes_ibge.png"
plt.savefig(output_path, dpi=300)
print(f"✅ Imagem salva com sucesso em: {output_path}")

