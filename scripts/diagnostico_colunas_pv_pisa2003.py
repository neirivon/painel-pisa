import pandas as pd

# Caminho para o arquivo
ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

print("⏳ Rodando mini-diagnóstico de colunas PV...")

# Ler usando separador inteligente
df = pd.read_csv(
    ARQUIVO_STUDENT,
    sep=r"\s+",
    engine="python",
    header=None,
    encoding="latin1",
    on_bad_lines='skip'
)

# Mostrar colunas em torno das Plausible Values
# Atenção: vamos explorar as colunas próximas às que suspeitamos
colunas_para_ver = [
    90, 91, 92, 93, 94,    # PVREAD
    110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, # PV MATH
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140  # PV SCIE
]

# Vamos mostrar os dados
print("\n🧪 Dados exemplo (primeiras 10 linhas):")
print(df[colunas_para_ver].head(10))

