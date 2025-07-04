import os
import sys
import pandas as pd
from painel_pisa.utils.config import CONFIG

# === Caminhos absolutos ===
CAMINHO_RAIZ = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISA"
CAMINHO_UTILS = os.path.join(CAMINHO_RAIZ, "painel_pisa")
CAMINHO_DADOS = os.path.join(CONFIG["CAMINHO_DADOS"], "dados_saeb_inep", "2021")
sys.path.append(CAMINHO_UTILS)

# === Importar conexão Mongo ===
from utils.conexao_mongo import conectar_mongo

# === Conectar ao banco 'saeb' ===
db, client = conectar_mongo(nome_banco="saeb")
colecao = db["saeb_2021_municipios"]

try:
    print("📥 Lendo arquivos CSV do SAEB 2023...")
    alunos = pd.read_csv(os.path.join(CAMINHO_DADOS, "TS_ALUNO_9EF.csv"), sep=";", encoding="latin1", low_memory=False)
    escolas = pd.read_csv(os.path.join(CAMINHO_DADOS, "TS_ESCOLA.csv"), sep=";", encoding="latin1", low_memory=False)


    print("🔗 Relacionando alunos com escolas...")
    dados = pd.merge(alunos, escolas, on="ID_ESCOLA", suffixes=("_aluno", "_escola"))

    print("🧹 Limpando e selecionando colunas...")
    dados = dados[[
        "ID_MUNICIPIO_escola", "ID_UF_escola",
        "PROFICIENCIA_MT_SAEB", "PROFICIENCIA_LP_SAEB"
    ]].dropna()

    dados = dados[
        (dados["PROFICIENCIA_MT_SAEB"] > 0) & 
        (dados["PROFICIENCIA_LP_SAEB"] > 0)
    ]

    print("📊 Calculando médias por município...")
    agrupado = dados.groupby("ID_MUNICIPIO_escola").agg({
        "PROFICIENCIA_MT_SAEB": "mean",
        "PROFICIENCIA_LP_SAEB": "mean",
        "ID_UF_escola": "first"
    }).reset_index()

    # Renomear colunas para padronizar no Mongo
    agrupado = agrupado.rename(columns={
        "ID_MUNICIPIO_escola": "ID_MUNICIPIO",
        "ID_UF_escola": "UF"
    })

    print("💾 Salvando dados no MongoDB...")
    colecao.delete_many({})
    colecao.insert_many(agrupado.to_dict(orient="records"))

    melhor_mt = agrupado.sort_values("PROFICIENCIA_MT_SAEB", ascending=False).head(1)
    pior_mt = agrupado.sort_values("PROFICIENCIA_MT_SAEB").head(1)

    melhor_lp = agrupado.sort_values("PROFICIENCIA_LP_SAEB", ascending=False).head(1)
    pior_lp = agrupado.sort_values("PROFICIENCIA_LP_SAEB").head(1)

    print("\n🏆 Melhor município em Matemática:")
    print(melhor_mt.to_string(index=False))

    print("\n🚨 Pior município em Matemática:")
    print(pior_mt.to_string(index=False))

    print("\n🏆 Melhor município em Língua Portuguesa:")
    print(melhor_lp.to_string(index=False))

    print("\n🚨 Pior município em Língua Portuguesa:")
    print(pior_lp.to_string(index=False))

    caminho_export = os.path.join(CAMINHO_RAIZ, "ranking_municipios_saeb2023.csv")
    agrupado.to_csv(caminho_export, index=False)
    print(f"\n✅ Arquivo exportado com sucesso para: {caminho_export}")

except Exception as e:
    print("❌ Erro durante a execução:", e)

finally:
    client.close()

