#os.path.join( , "h")omos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "s")criptos.path.join(s, "g")erar_rubricas_pedagogicas_tmap_v4.py

import pandas as pd
import json
import os
from painel_pisa.utils.config import CONFIG

# Caminhos absolutos
json_rubrica = os.path.join(CONFIG["CAMINHO_DADOS"], "bncc", "rubrica_sinapse_9ano_todas_v4.json")
csv_municipios = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap.csv"
csv_saida = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "r")ubricas_pedagogicas_tmap.csv"

# Garante que a pasta exista
os.makedirs("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmap", exist_ok=True)

# === Carrega a rubrica SINAPSE v4 ===
with open(json_rubrica, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Lookup por dimensão → nível "Essencial"
rubricas_por_dimensao = {
    item["dimensao"]: next(
        (n for n in item["niveis"] if n["nivel"] in ["3", 3, "Essencial", "essencial"]),
        item["niveis"][0]
    )
    for item in rubrica
}

# === Carrega os dados dos municípios ===
df_municipios = pd.read_csv(csv_municipios)

# === Aplica as rubricas por linha ===
def aplicar_rubricas(row):
    return {
        "Município": row["Município"],
        "proficiência_simulada": row["proficiência_simulada"],
        "nível_proficiencia": row.get("nível_proficiencia", "—"),
        "sinapse_bloom": rubricas_por_dimensao["Taxonomia de Bloom"]["exemplo"],
        "sinapse_metodologia": rubricas_por_dimensao["Metodologia Ativa"]["exemplo"],
        "sinapse_perfil": rubricas_por_dimensao["Perfil Neuropsicopedagógico"]["exemplo"],
        "sinapse_dua": rubricas_por_dimensao["DUA – Desenho Universal para Aprendizagem"]["exemplo"],
        "sinapse_ctc": rubricas_por_dimensao["CTC – Contextualização Territorial e Cultural"]["exemplo"]
    }

# Aplica em todas as linhas
rubricas_final = df_municipios.apply(aplicar_rubricas, axis=1, result_type="expand")

# Salva como CSV
rubricas_final.to_csv(csv_saida, index=False, encoding="utf-8")
print(f"✅ Rubricas pedagógicas geradas com sucesso.")
print(f"📄 Arquivo salvo: {csv_saida}")

