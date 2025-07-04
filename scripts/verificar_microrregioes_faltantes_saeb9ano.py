from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# verificar_microrregioes_faltantes_saeb9ano.py

import pandas as pd
from pymongo import MongoClient

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]

# Obter microrregiões distintas da base SAEB 2021 9º ano
micros_saeb = db.saeb_2021_municipios_9ano.distinct("MICRORREGIAO")

# Obter microrregiões distintas da base IBGE com geometria
micros_ibge = db.ibge_microrregioes_geometry.distinct("NM_MICRO")

# Normalizar para comparação (caso-sensitive pode causar erro)
micros_saeb_set = set(m.strip().lower() for m in micros_saeb if m)
micros_ibge_set = set(m.strip().lower() for m in micros_ibge if m)

# Diferença: microrregiões do SAEB que não estão no IBGE
faltantes = sorted(m for m in micros_saeb_set if m not in micros_ibge_set)

# Exibir resultado
print("🔍 Total de microrregiões no SAEB:", len(micros_saeb_set))
print("✅ Total encontradas no IBGE:", len(micros_saeb_set) - len(faltantes))
print("❌ Total faltantes no IBGE:", len(faltantes))

# Mostrar lista
print("\n📌 Microrregiões faltantes:")
for m in faltantes:
    print(f" - {m}")

# Salvar em CSV
df_faltantes = pd.DataFrame(faltantes, columns=["microrregiao_faltante"])
caminho_csv = "outputs_tmaos.path.join(p, "m")icrorregioes_nao_encontradas_ibge.csv"
df_faltantes.to_csv(caminho_csv, index=False)
print(f"\n📁 Relatório exportado: {caminho_csv}")

client.close()

