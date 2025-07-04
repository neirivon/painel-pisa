import pandas as pd
import pycountry
import json

# Caminho do arquivo
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "I")NEos.path.join(P, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune2os.path.join(4, "p")isa2022_ms_bkg_stu_overall_compendium.xlsx"

# Leitura do Excel
df = pd.read_excel(CAMINHO_ARQUIVO)

# Selecionar países com ESCS disponível
df_validos = df[["CNT", "ESCS"]].dropna()
codigos = df_validos["CNT"].unique()

# Mapear nomes usando pycountry (fallback para codificação ISO)
mapa = {}
for codigo in codigos:
    try:
        nome = pycountry.countries.get(alpha_3=codigo.upper()).name
    except:
        nome = "Desconhecido"
    mapa[codigo.upper()] = nome

# Exibir resultado no terminal
print("✅ Países com ESCS disponíveis no PISA 2022:\n")
for k, v in sorted(mapa.items()):
    print(f'"{k}": "{v}",')

# (Opcional) Salvar em JSON
with open("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "s")criptos.path.join(s, "p")aises_com_escs_2022.json", "w", encoding="utf-8") as f:
    json.dump(mapa, f, ensure_ascii=False, indent=2)

print(f"\n✅ Total: {len(mapa)} países salvos em 'paises_com_escs_2022.json'")

