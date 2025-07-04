import pyreadstat

# Caminho do arquivo de dados
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "C")Oos.path.join(G, "C")Y07_MSU_STU_COG.sav"
LOG_SAIDA = "log_verificacao_cog_2018.txt"

try:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write("⏳ Iniciando leitura do arquivo .sav completo...\n")

        # Lê o arquivo completo
        df, meta = pyreadstat.read_sav(CAMINHO_ARQUIVO)

        log.write("\n📌 Colunas relacionadas às notas e país:\n")
        colunas_interesse = [
            col for col in df.columns 
            if any(pv in col for pv in ["PV1MATH", "PV1READ", "PV1SCIE"]) 
            or col in ["CNT", "CNTSTUID", "CNTSCHID"]
        ]
        for col in colunas_interesse:
            log.write(f"- {col}\n")

        log.write("\n🧪 Primeiros dados das colunas selecionadas:\n")
        log.write(df[colunas_interesse].head(10).to_string(index=False))
        log.write("\n\n✅ Finalizado com sucesso.\n")

except FileNotFoundError:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write(f"❌ Arquivo não encontrado: {CAMINHO_ARQUIVO}\n")
except Exception as e:
    with open(LOG_SAIDA, "w", encoding="utf-8") as log:
        log.write(f"⚠️ Erro ao processar o arquivo: {e}\n")

