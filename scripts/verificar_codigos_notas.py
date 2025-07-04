# verificar_codigos_notas.py

import pandas as pd

base_path = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")NEos.path.join(P, "R")ELATORIOos.path.join(S, "2")02os.path.join(2, "P")ISA2022_FinalRelease_Compendia_18thJune24_cog"

arquivos = {
    "matematica": f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_math_compendium.xlsx",
    "leitura": f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_read_compendium.xlsx",
    "ciencias": f"{base_pathos.path.join(}, "p")isa2022_ms_cog_overall_scie_compendium.xlsx"
}

for nome, caminho in arquivos.items():
    df = pd.read_excel(caminho)
    primeira_coluna = df.columns[0]
    print(f"\n📘 {nome.capitalize()} — Primeira coluna: '{primeira_coluna}'")
    print(df[primeira_coluna].dropna().unique()[:10])

