import pandas as pd

ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

print("⏳ Testando leitura com separador inteligente...")

df = pd.read_csv(
    ARQUIVO_STUDENT,
    sep=r"\s+",
    engine="python",
    header=None,
    nrows=20,
    encoding="latin1",
    on_bad_lines='skip'   # Novo padrão do pandas!
)

print(df.head(20))

