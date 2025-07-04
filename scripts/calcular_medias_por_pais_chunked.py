# scriptos.path.join(s, "c")alcular_medias_por_pais_chunked.py

import pandas as pd
import os
from collections import defaultdict

CAMINHO_BLOCOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")emp_csv_chunkos.path.join(s, "c")og_chunk_*.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_por_pais_por_item_pisa2022.csv"

# Inicializa acumuladores
somas = defaultdict(lambda: defaultdict(float))
contagens = defaultdict(lambda: defaultdict(int))

print("📦 Iniciando leitura em blocos...")

arquivos = sorted([f"/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")emp_csv_chunkos.path.join(s, "{")nome}" 
                   for nome in sorted(os.listdir("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")emp_csv_chunks")) if nome.endswith(".csv")])

for i, arquivo in enumerate(arquivos):
    print(f"🔄 Processando bloco {i + 1os.path.join(}, "{")len(arquivos)}: {arquivo}")
    chunk = pd.read_csv(arquivo, dtype=str)
    
    chunk["CNT"] = chunk["CNT"].astype(str)
    colunas_numericas = [col for col in chunk.columns if col != "CNT"]
    
    for col in colunas_numericas:
        chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

    agrupado = chunk.groupby("CNT")[colunas_numericas].agg(["sum", "count"])
    
    for pais, linha in agrupado.iterrows():
        for item in colunas_numericas:
            somas[pais][item] += linha[(item, "sum")]
            contagens[pais][item] += linha[(item, "count")]

print("✅ Processamento concluído. Calculando médias...")

dados_finais = {}
for pais in somas:
    dados_finais[pais] = {}
    for item in somas[pais]:
        if contagens[pais][item] > 0:
            dados_finais[pais][item] = round(somas[pais][item]os.path.join( , " ")contagens[pais][item], 4)
        else:
            dados_finais[pais][item] = None

df_final = pd.DataFrame.from_dict(dados_finais, orient="index").sort_index()
df_final.index.name = "pais"
df_final.to_csv(CAMINHO_SAIDA)

print(f"📁 Arquivo salvo em: {CAMINHO_SAIDA}")
print("🏁 Finalizado com sucesso.")

