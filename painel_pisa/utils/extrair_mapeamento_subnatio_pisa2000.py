# utilos.path.join(s, "e")xtrair_mapeamento_subnatio_pisa2000.py

import pandas as pd
import json
from pymongo import MongoClient

# Caminho para o arquivo SPSS escolar
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSos.path.join(S, "P")ISA2000_SPSS_school_questionnaire.txt"

# Parâmetros Mongo
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "pisa"
COLECAO = "pisa2000_school_regioes"

# Dicionário fixo de REGIÕES DO BRASIL (segundo IBGE)
REGIOES_BRASIL = {
    "NORTE": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "NORDESTE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "CENTRO-OESTE": ["DF", "GO", "MT", "MS"],
    "SUDESTE": ["ES", "MG", "RJ", "SP"],
    "SUL": ["PR", "RS", "SC"]
}

def detectar_subnatio():
    print("🔍 Lendo arquivo escolar para detectar SUBNATIO...")
    df = pd.read_fwf(CAMINHO_ARQUIVO, encoding="latin1")
    
    print(f"✅ Arquivo carregado: {len(df)} registros.")

    # Tentar encontrar colunas possíveis
    colunas = [c.lower() for c in df.columns]
    if "subnatio" not in colunas:
        raise Exception("Erro: SUBNATIO não encontrado.")

    df.columns = colunas  # padronizar

    # Filtrar só Brasil
    df_brasil = df[df["subnatio"].notna()]
    
    subnatio_unicos = sorted(df_brasil["subnatio"].unique())
    print(f"✅ Códigos SUBNATIO únicos detectados: {subnatio_unicos}")

    return subnatio_unicos

def construir_mapeamento(subnatio_codigos):
    print("🛠️ Construindo mapeamento manual...")
    mapeamento = []

    for codigo in subnatio_codigos:
        entrada = {
            "subnatio_codigo": int(codigo),
            "estado_sigla": None,   # Vamos deixar manual inicialmente
            "regiao": None,
            "ano": 2000,
            "origem": "SPSS_OFICIAL"
        }
        mapeamento.append(entrada)

    return mapeamento

def salvar_mapeamento(mapeamento):
    caminho_saida = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoeos.path.join(s, "p")isa2000_school_regioes.json"
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=4)
    print(f"✅ Mapeamento salvo em {caminho_saida}")

    # Salvar no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    db[COLECAO].drop()
    db[COLECAO].insert_many(mapeamento)
    client.close()
    print(f"✅ Coleção MongoDB '{COLECAO}' atualizada.")

def extrair_mapeamento_subnatio():
    subnatio_codigos = detectar_subnatio()
    mapeamento = construir_mapeamento(subnatio_codigos)
    salvar_mapeamento(mapeamento)

if __name__ == "__main__":
    extrair_mapeamento_subnatio()

