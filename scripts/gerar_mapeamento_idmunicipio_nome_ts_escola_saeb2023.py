import pandas as pd
import json

CAMINHO_CSV = (
    "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")023/"
    "DADOos.path.join(S, "T")S_ESCOLA.csv"
)
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")dmunicipio_nome_saeb2023.json"

print("📥 Lendo TS_ESCOLA.csv...")
df = pd.read_csv(CAMINHO_CSV, sep=";", encoding="latin1", low_memory=False)

print("🔎 Selecionando colunas 'ID_MUNICIPIO' e 'NOME' (deduzido)...")
if "ID_MUNICIPIO" not in df.columns:
    raise Exception("❌ Coluna 'ID_MUNICIPIO' não encontrada.")

# Tentando detectar automaticamente o nome do município
possiveis_nomes = [col for col in df.columns if "NOME" in col.upper() or "MUNIC" in col.upper()]
print(f"🧾 Colunas candidatas para nome do município: {possiveis_nomes}")
nome_coluna = possiveis_nomes[0] if possiveis_nomes else None

if not nome_coluna:
    raise Exception("❌ Nenhuma coluna de nome de município detectada.")

print(f"✅ Usando coluna '{nome_coluna}' para nomes...")

df_filtrado = df[["ID_MUNICIPIO", nome_coluna]].drop_duplicates()
df_filtrado.columns = ["ID_MUNICIPIO", "NOME"]
df_filtrado["ID_MUNICIPIO"] = df_filtrado["ID_MUNICIPIO"].astype(str)

mapeamento = dict(zip(df_filtrado["NOME"], df_filtrado["ID_MUNICIPIO"]))

print(f"💾 Salvando {len(mapeamento)} pares em: {CAMINHO_SAIDA}")
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(mapeamento, f, ensure_ascii=False, indent=2)

print("✅ Mapeamento finalizado com sucesso.")

