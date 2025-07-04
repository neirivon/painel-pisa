from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import os
from pymongo import MongoClient

# === Caminhos dos arquivos ===
caminhos = {
    "regiao": "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_201os.path.join(9, "m")icrodados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_REGIAO.xlsx",
    "brasil": "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_201os.path.join(9, "m")icrodados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_BRASIL.xlsx"
}

# === Conectar ao MongoDB com autenticação ===
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]

# === Loop de importação ===
for nome, caminho in caminhos.items():
    if os.path.exists(caminho):
        print(f"📥 Lendo {nome.upper()}...")
        df = pd.read_excel(caminho)
        df = df.where(pd.notnull(df), None)
        colecao = f"saeb_2019_{nome}"
        print(f"🧨 Limpando coleção {colecao} se existir...")
        db[colecao].drop()
        print(f"🚀 Inserindo {len(df)} documentos na coleção {colecao}...")
        db[colecao].insert_many(df.to_dict(orient="records"))
        print(f"✅ {nome.upper()} importado com sucesso.")
    else:
        print(f"❌ Arquivo não encontrado: {caminho}")

cliente.close()

