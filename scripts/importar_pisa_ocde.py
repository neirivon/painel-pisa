from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import requests
import os
import json
from pymongo import MongoClient

# Pasta de saída
output_folder = "dados_json_pisa_todos_paises"
os.makedirs(output_folder, exist_ok=True)

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_bruta = db["resultados_brutos"]
colecao_normalizada = db["resultados_normalizados"]

# Domínios do PISA com códigos SDMX
dominios = {
    "READING": "READ",
    "MATHEMATICS": "MATH",
    "SCIENCE": "SCIE"
}

# Parâmetros fixos
idade = "15"
sexo = "_T"
anos = [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022]

total_downloads = 0
falhas = []

# Função para normalizar SDMX para MongoDB
def explodir_sdmx_para_mongodb(dados_json, ano, dominio, codigo_dominio, colecao_destino):
    try:
        estrutura = dados_json.get("structure", {})
        dimensoes = estrutura.get("dimensions", {}).get("observation", [])
        series_dimensoes = estrutura.get("dimensions", {}).get("series", [])

        dimension_index = {dim["id"]: i for i, dim in enumerate(dimensoes)}
        series_index = {dim["id"]: i for i, dim in enumerate(series_dimensoes)}

        paises_pos = {str(i): val["id"] for i, val in enumerate(series_dimensoes[0]["values"])}
        unidades = estrutura.get("attributes", {}).get("observation", [])[0]["values"]
        unidade_map = {str(i): val["name"] for i, val in enumerate(unidades)}

        series = dados_json.get("data", [{}])[0].get("series", {})

        total_inseridos = 0

        for chave_serie, conteudo in series.items():
            cod_pais = paises_pos.get(chave_serie.split(":")[0], "UNKNOWN")
            observacoes = conteudo.get("observations", {})

            for key_obs, valores in observacoes.items():
                valor = valores[0]
                unidade = unidade_map.get(str(valores[1]), "Desconhecida") if len(valores) > 1 else "Desconhecida"

                doc = {
                    "ano": ano,
                    "dominio": dominio,
                    "codigo_dominio": codigo_dominio,
                    "pais": cod_pais,
                    "valor": valor,
                    "unidade": unidade,
                    "sexo": sexo,
                    "idade": idade
                }
                colecao_destino.insert_one(doc)
                total_inseridos += 1

        print(f"✅ Inseridos {total_inseridos} registros normalizados no MongoDB para {dominio} {ano}")
    except Exception as e:
        print(f"❌ Erro ao normalizar dados {dominio}-{ano}: {e}")

# Loop de download e importação
for nome_dominio, codigo_dominio in dominios.items():
    for ano in anos:
        url = (
            f"httpsos.path.join(:, "/")sdmx.oecd.oros.path.join(g, "p")ublios.path.join(c, "r")esos.path.join(t, "d")atos.path.join(a, "P")ISos.path.join(A, "A")LL.{codigo_dominio}.{sexo}.{idadeos.path.join(}, "a")ll"
            f"?startPeriod={ano}&endPeriod={ano}"
        )
        print(f"\n🔄 Baixando: TODOS OS PAÍSES - {nome_dominio} - {ano}")
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                dados = response.json()
                filename = f"{output_folderos.path.join(}, "T")ODOS_{nome_dominio}_{ano}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                print(f"✅ Salvo: {filename}")

                # Inserção bruta
                colecao_bruta.insert_one({
                    "ano": ano,
                    "dominio": nome_dominio,
                    "codigo_dominio": codigo_dominio,
                    "json_original": dados
                })

                # Inserção normalizada
                explodir_sdmx_para_mongodb(
                    dados_json=dados,
                    ano=ano,
                    dominio=nome_dominio,
                    codigo_dominio=codigo_dominio,
                    colecao_destino=colecao_normalizada
                )

                total_downloads += 1
            else:
                msg = f"⚠️ Falha ({response.status_code}) em {url}"
                print(msg)
                falhas.append(msg)
        except Exception as e:
            msg = f"❌ Erro ao baixar {nome_dominio}-{ano}: {str(e)}"
            print(msg)
            falhas.append(msg)

# Finalização
print(f"\n✅ Concluído: {total_downloads} arquivos processados e importados.")
if falhas:
    print(f"\n⚠️ {len(falhas)} falhas:")
    for erro in falhas:
        print(" -", erro)

