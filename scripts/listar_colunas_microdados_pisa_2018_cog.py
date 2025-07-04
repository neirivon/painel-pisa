import pyreadstat

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "C")Oos.path.join(G, "C")Y07_MSU_STU_COG.sav"
LOG_SAIDA = "log_colunas_cog_2018.txt"

try:
    df, meta = pyreadstat.read_sav(CAMINHO_ARQUIVO, metadataonly=True)

    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write("📌 Todas as colunas disponíveis no COG 2018:\n\n")
        for col in meta.column_names:
            log.write(f"{col}\n")

        log.write("\n✅ Fim da listagem.\n")

except Exception as e:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write(f"❌ Erro ao tentar listar colunas: {str(e)}\n")

