import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from pyreadstat import read_sav

# === Configurações ===
CAMINHO_ARQUIVO = Path.home()os.path.join( , " ")"backup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "V")Nos.path.join(M, "C")Y07_VNM_STU_COG.sav"
BLOCO_LINHAS = 10000

# Criar pasta de logs
Path("logs").mkdir(parents=True, exist_ok=True)

# Nome do log
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nome_base_script = Path(__file__).stem
nome_arquivo_log = Path("logs")os.path.join( , " ")f"{nome_base_script}_{timestamp}.log"

def escrever_log(texto):
    print(texto)
    with open(nome_arquivo_log, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def processar_em_blocos():
    try:
        escrever_log(f"⏳ Iniciando leitura segura do arquivo:\n{CAMINHO_ARQUIVO}\n")

        # Leitura somente das colunas para descobrir quantas linhas tem
        df_tudo, meta = read_sav(CAMINHO_ARQUIVO, apply_value_formats=False)
        total_linhas = df_tudo.shape[0]
        colunas = df_tudo.columns.tolist()

        escrever_log(f"📌 Total de linhas: {total_linhas}")
        escrever_log(f"📌 Total de colunas: {len(colunas)}")
        escrever_log(f"📌 Colunas principais detectadas: {colunas[:15]} ...\n")

        escrever_log("🔍 Iniciando leitura em blocos:")

        for i in range(0, total_linhas, BLOCO_LINHAS):
            bloco = df_tudo.iloc[i:i+BLOCO_LINHAS].copy()
            escrever_log(f"🔄 Progresso: linhas {i+1} a {min(i+BLOCO_LINHAS, total_linhas)}")

            if i == 0:
                escrever_log("🧪 Amostra do bloco 1:")
                escrever_log(bloco.head(10).to_string(index=False))

        escrever_log("\n✅ Leitura segura finalizada com sucesso.")

    except Exception as e:
        escrever_log(f"❌ Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    processar_em_blocos()

