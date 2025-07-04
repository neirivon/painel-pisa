from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nspecionar_colunas_ts_municipio_2019.py

import pandas as pd
from pymongo import MongoClient

# Caminho do arquivo Excel com os dados agregados por município
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_201os.path.join(9, "m")icrodados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_MUNICIPIO.xlsx"

# Conectar ao MongoDB apenas para garantir que a estrutura esteja correta (fecha depois)
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]

# Ler Excel
print("📥 Lendo arquivo Excel para inspecionar colunas...")
df = pd.read_excel(CAMINHO_ARQUIVO)

# Listar nomes exatos das colunas
print("\n🧾 Colunas encontradas no arquivo:")
for coluna in df.columns:
    print(f"- {coluna}")

# Encerrar conexão com MongoDB de forma segura
cliente.close()
print("\n✅ Conexão com MongoDB encerrada.")

