import pyreadstat

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "C")Oos.path.join(G, "C")Y07_MSU_STU_COG.sav"
LOG_SAIDA = "log_verificacao_cog_2018.txt"
CHUNKSIZE = 100  # menor ainda, para mais segurança

try:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write("⏳ Lendo em blocos pequenos (100 linhas)...\n")

        # Lê o primeiro bloco com segurança
        for i, (df_chunk, meta) in enumerate(pyreadstat.read_file_in_chunks(pyreadstat.read_sav, CAMINHO_ARQUIVO, chunksize=CHUNKSIZE)):

            # Extrai colunas desejadas
            colunas_interesse = [
                col for col in df_chunk.columns 
                if any(pv in col for pv in ["PV1MATH", "PV1READ", "PV1SCIE"]) 
                or col in ["CNT", "CNTSTUID", "CNTSCHID"]
            ]

            log.write("\n📌 Colunas relevantes:\n")
            for col in colunas_interesse:
                log.write(f"- {col}\n")

            log.write("\n🧪 Primeiras linhas dos dados relevantes:\n")
            log.write(df_chunk[colunas_interesse].head(10).to_string(index=False))

            log.write("\n\n✅ Leitura parcial segura finalizada.\n")
            break  # encerra após o primeiro bloco

except Exception as e:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write(f"❌ Erro crítico: {str(e)}\n")

