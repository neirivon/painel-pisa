import pyreadstat

# Caminho para o arquivo de questionário do estudante
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "S")Tos.path.join(U, "C")Y07_MSU_STU_QQQ.sav"

try:
    # Lê o arquivo com pyreadstat
    df, meta = pyreadstat.read_sav(CAMINHO_ARQUIVO)

    # Exibe os nomes das primeiras 20 colunas
    print("\n📌 Cabeçalho (primeiras 20 colunas):")
    print(list(df.columns[:20]))

    # Exibe os primeiros 10 registros
    print("\n🧪 Primeiros dados (df.head(10)):")
    print(df.head(10))

except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {CAMINHO_ARQUIVO}")
except Exception as e:
    print(f"⚠️ Erro ao ler o arquivo .sav: {e}")

