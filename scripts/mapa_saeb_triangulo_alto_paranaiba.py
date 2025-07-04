# mapa_saeb_triangulo_alto_paranaiba.py

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Caminho para o shapefile ===
# Substitua o caminho abaixo com o caminho correto no seu computador
shapefile_path = "dados_shapefilos.path.join(e, "M")G_Triangulo_AltoParanaiba.shp"

# === 2. Carregar o shapefile ===
gdf = gpd.read_file(shapefile_path)

# === 3. Simular valores médios de desempenho (SAEB) em Matemática ===
np.random.seed(42)  # Para resultados reproduzíveis
gdf["desempenho_matematica"] = np.random.uniform(190, 280, size=len(gdf))

# === 4. Criar o mapa temático ===
fig, ax = plt.subplots(figsize=(12, 8))
gdf.plot(
    column="desempenho_matematica",
    cmap="Blues",
    linewidth=0.5,
    edgecolor="black",
    legend=True,
    legend_kwds={"label": "Desempenho Médio - Matemática (SAEB)", "shrink": 0.6},
    ax=ax
)

# === 5. Ajustes visuais ===
ax.set_title("📍 Desempenho em Matemática — SAEB 2021\nMicrorregião: Triângulo Mineiro e Alto Paranaíba", fontsize=16)
ax.axis("off")
plt.tight_layout()

# === 6. Salvar ou exibir o gráfico ===
# plt.savefig("mapa_desempenho_saeb_mg.png", dpi=300)
plt.show()

