import pandas as pd

ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

print("⏳ Rodando diagnóstico FINAL para localizar W_FSTUWT...")

df = pd.read_csv(
    ARQUIVO_STUDENT,
    sep=r"\s+",
    engine="python",
    header=None,
    encoding="latin1",
    on_bad_lines='skip'
)

# Inspecionar de 180 a 200
print(df[[180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]].head(10))

