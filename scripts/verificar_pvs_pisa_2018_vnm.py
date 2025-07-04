import os
import pandas as pd
import pyreadstat
from datetime import datetime

# === Caminho completo fixo do arquivo .sav ===
CAMINHO_ARQUIVO_SAV = os.path.expanduser(
    os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "V")Nos.path.join(M, "C")Y07_VNM_STU_PVS.sav")
)

# === Parâmetros ===
TAMANHO_BLOCO = 10000

# === Geração do caminho absoluto do log ===
BASE_DIR = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "P")ISA_novo"))
PASTA_LOG = os.path.join(BASE_DIR, "logs")
os.makedirs(PASTA_LOG, exist_ok=True)

nome_script = "verificar_pvs_pisa_2018_vnm"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CAMINHO_LOG = os.path.join(PASTA_LOG, f"{nome_script}_{timestamp}.log")

# === Início do processamento ===
with open(CAMINHO_LOG, "w", encoding="utf-8") as log:
    log.write("⏳ Iniciando leitura parcial de PVs do PISA 2018 (VNM)...\n")

    try:
        total_linhas_lidas = 0

        for df, meta in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, CAMINHO_ARQUIVO_SAV, chunksize=TAMANHO_BLOCO):
            total_linhas_lidas += len(df)

            if total_linhas_lidas == len(df):
                colunas_interesse = [col for col in df.columns if col.startswith("PV") or col in ["CNT", "CNTSCHID", "CNTSTUID"]]
                
                log.write("\n📌 Colunas plausíveis encontradas:\n")
                for col in colunas_interesse:
                    log.write(f"- {col}\n")
                
                log.write("\n🧪 Primeiros dados relevantes (10 linhas):\n")
                log.write(df[colunas_interesse].head(10).to_string(index=False))
                log.write("\n\n")

                print("✅ Primeiros dados extraídos com sucesso.")
            
            print(f"🔄 Progresso: {total_linhas_lidas} linhas lidas...")

        log.write(f"\n✅ Leitura parcial segura finalizada ({total_linhas_lidas} linhas lidas).\n")

    except Exception as e:
        erro_msg = f"❌ Erro ao processar o arquivo: {e}"
        print(erro_msg)
        log.write(erro_msg + "\n")

