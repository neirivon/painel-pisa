# scriptos.path.join(s, "e")xportar_cog_em_blocos.py

import pyreadstat
import pandas as pd
import os

CAMINHO_SAV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "D")ADOos.path.join(S, "2")02os.path.join(2, "C")Y08MSP_STU_COG.SAV"
DIRETORIO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "t")emp_csv_chunks"
CHUNKSIZE = 100_000

# Garante que a pasta de saída existe
os.makedirs(DIRETORIO_SAIDA, exist_ok=True)

# Estima o número de linhas
_, meta = pyreadstat.read_sav(CAMINHO_SAV, metadataonly=True)
total_linhas = meta.number_rows
print(f"📊 Linhas totais estimadas: {total_linhas}")

# Exporta em blocos
for inicio in range(0, total_linhas, CHUNKSIZE):
    fim = min(inicio + CHUNKSIZE, total_linhas)
    print(f"📤 Exportando linhas {inicio} até {fim}...")
    df_chunk, _ = pyreadstat.read_sav(CAMINHO_SAV, row_offset=inicio, row_limit=CHUNKSIZE)
    df_chunk.to_csv(f"{DIRETORIO_SAIDAos.path.join(}, "c")og_chunk_{inicio}_{fim}.csv", index=False)

print("✅ Exportação em blocos finalizada.")

