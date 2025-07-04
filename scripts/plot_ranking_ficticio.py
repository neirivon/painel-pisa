import pandas as pd
import matplotlib.pyplot as plt

# Caminhos
CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "r")anking_saeb2023_codigos_ficticios.csv"
CAMINHO_SAIDA_TOP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")op10_municipios_saeb2023.png"
CAMINHO_SAIDA_BOTTOM = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "b")ottom10_municipios_saeb2023.png"

# Carregar e processar
df = pd.read_csv(CAMINHO_CSV)
top10 = df.sort_values("PROFICIENCIA_MT_SAEB", ascending=False).head(10)
bottom10 = df.sort_values("PROFICIENCIA_MT_SAEB", ascending=True).head(10)

# Gráfico Top 10
plt.figure(figsize=(10, 6))
plt.barh(top10["ID_MUNICIPIO_escola"].astype(str), top10["PROFICIENCIA_MT_SAEB"], color='green')
plt.xlabel("Média de Proficiência em Matemática")
plt.title("🏆 Top 10 Municípios (Códigos Fictícios) - SAEB 2023")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(CAMINHO_SAIDA_TOP)
plt.close()

# Gráfico Bottom 10
plt.figure(figsize=(10, 6))
plt.barh(bottom10["ID_MUNICIPIO_escola"].astype(str), bottom10["PROFICIENCIA_MT_SAEB"], color='red')
plt.xlabel("Média de Proficiência em Matemática")
plt.title("🚨 Piores 10 Municípios (Códigos Fictícios) - SAEB 2023")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(CAMINHO_SAIDA_BOTTOM)
plt.close()

print("✅ Imagens salvas com sucesso!")

