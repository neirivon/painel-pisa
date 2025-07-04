import os
import pandas as pd

# Caminho onde os JSONs estão (ajustado conforme seu projeto)
PASTA_JSON = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/ocde_json"

# Garante que o diretório existe
if not os.path.exists(PASTA_JSON):
    print(f"❌ Diretório não encontrado: {PASTA_JSON}")
    exit(1)

# Lista os arquivos .json
arquivos = sorted([f for f in os.listdir(PASTA_JSON) if f.endswith(".json")])

# Mostra resultado formatado
if not arquivos:
    print("⚠️ Nenhum arquivo .json encontrado.")
else:
    print(f"📂 Total de arquivos JSON encontrados: {len(arquivos)}\n")
    for f in arquivos:
        caminho_completo = os.path.join(PASTA_JSON, f)
        print(f"- {f}\n  ↳ {caminho_completo}\n")

