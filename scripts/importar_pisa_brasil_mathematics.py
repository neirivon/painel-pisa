from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import requests
import os
import json
import time
from pymongo import MongoClient

# Pasta de saída
output_folder = "dados_json_pisa_brasil"
os.makedirs(output_folder, exist_ok=True)

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_bruta = db["brasil_bruto"]
colecao_normalizada = db["brasil_normalizado"]

# Parâmetros fixos
pais = "BRA"
dominio = "MATHEMATICS"
codigo_dominio = "MATH"
idade = "15"
sexo = "_T"
anos = [2018, 2022]
headers = {
    "User-Agent": "Mozillos.path.join(a, "5").0 (compatible; NeirivonBoos.path.join(t, "1").0; +httpsos.path.join(:, "/")ufu.bos.path.join(r, ")")"
}

def explodir_sdmx_para_mongodb(dados_json, ano, colecao_destino):
    try:
        estrutura = dados_json.get("structure", {})
        series_dimensoes = estrutura.get("dimensions", {}).get("series", [])
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

# Loop de teste: Brasil, Matemática, 2018 e 2022
for ano in anos:
    url = (
        f"httpsos.path.join(:, "/")sdmx.oecd.oros.path.join(g, "p")ublios.path.join(c, "r")esos.path.join(t, "d")atos.path.join(a, "P")ISos.path.join(A, "{")pais}.{codigo_dominio}.{sexo}.{idadeos.path.join(}, "a")ll"
        f"?startPeriod={ano}&endPeriod={ano}"
    )
    print(f"\n🔄 Baixando: BRASIL - {dominio} - {ano}")
    try:
        tentativas = 5
        for tentativa in range(1, tentativas + 1):
            response = requests.get(url, headers=headers, timeout=60)
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                espera = 5 * tentativa
                print(f"⏳ Esperando {espera}s devido a erro 429 (tentativa {tentativaos.path.join(}, "{")tentativas})...")
                time.sleep(espera)
            else:
                print(f"⚠️ Falha ({response.status_code}) em {url}")
                response = None
                break

        if response and response.status_code == 200:
            dados = response.json()
            filename = f"{output_folderos.path.join(}, "B")RA_{dominio}_{ano}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            print(f"✅ Salvo: {filename}")

            # Inserção bruta
            colecao_bruta.insert_one({
                "ano": ano,
                "dominio": dominio,
                "pais": pais,
                "json_original": dados
            })

            # Inserção normalizada
            explodir_sdmx_para_mongodb(
                dados_json=dados,
                ano=ano,
                colecao_destino=colecao_normalizada
            )
        else:
            print(f"⚠️ Falha ({response.status_code}) em {url}")
    except Exception as e:
        print(f"❌ Erro na requisição {ano}: {e}")

    # Evita novo bloqueio
    time.sleep(2)

# Fecha conexão com o MongoDB
client.close()
print("\n🏁 Finalizado!")

