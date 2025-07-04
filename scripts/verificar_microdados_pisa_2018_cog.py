import pyreadstat

# Caminho para o arquivo .sav de microdados cognitivos
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "C")Oos.path.join(G, "C")Y07_MSU_STU_COG.sav"

try:
    print("⏳ Lendo o arquivo completo. Isso pode levar algum tempo...")

    # Leitura completa do .sav
    df, meta = pyreadstat.read_sav(CAMINHO_ARQUIVO)

    # Filtra colunas com PV (notas) + CNT (país)
    colunas_interesse = [col for col in df.columns if "PV1MATH" in col or "PV1READ" in col or "PV1SCIE" in col or col in ["CNT", "CNTSTUID", "CNTSCHID"]]

    print("\n📌 Colunas relevantes encontradas:")
    print(colunas_interesse)

    # Mostra amostra dos dados
    print("\n🧪 Primeiros dados dessas colunas:")
    print(df[colunas_interesse].head(10))

except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {CAMINHO_ARQUIVO}")
except Exception as e:
    print(f"⚠️ Erro ao ler o arquivo .sav: {e}")

