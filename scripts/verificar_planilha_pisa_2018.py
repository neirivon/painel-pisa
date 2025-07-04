import pandas as pd

# Caminho para o arquivo Excel
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "b")kos.path.join(g, "p")isa_ms_bkg_overall_stu_compendium.xlsx"

try:
    # Lê a planilha inteira (ou parte, se for muito grande)
    df = pd.read_excel(CAMINHO_ARQUIVO)

    # Exibe o cabeçalho completo (nomes das colunas)
    print("\n📌 Cabeçalho (colunas disponíveis):")
    print(list(df.columns))

    # Exibe as primeiras 10 linhas da planilha
    print("\n🧪 Primeiros dados (df.head(10)):")
    print(df.head(10))

except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {CAMINHO_ARQUIVO}")
except Exception as e:
    print(f"⚠️ Erro ao ler a planilha: {e}")

