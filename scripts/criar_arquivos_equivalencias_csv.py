# scripts/criar_arquivos_equivalencias_csv.py

import os
import pandas as pd

# ===== Caminhos de saída =====
PASTA_DESTINO = "painel_pisa/dados_cloud"
ARQUIVO_EQUIV_PAISES = os.path.join(PASTA_DESTINO, "estrutura_equivalente_pais.csv")
ARQUIVO_EQUIV_PONTOS = os.path.join(PASTA_DESTINO, "estrutura_equivalente_pontuacoes.csv")

# ===== Dados para equivalência de países =====
dados_paises = [
    ["pisa_2000_cognitive_item", "COUNTRY", "CNT"],
    ["pisa_2000_cognitive_item", "CNT", "CNT"],
    ["pisa_2006_cognitive", "Country", "CNT"],
    ["pisa_2022_student", "CNT", "CNT"],
    ["pisa_ocde_2000_medias", "pais", "CNT"],
    ["pisa_ocde_2022_escs_media", "pais", "CNT"],
    ["pisa_ocde_2022_escs_resumo", "pais", "CNT"],
    ["pisa_2009_student_sps", "COUNTRY", "CNT"],
    ["pisa_2009_student_sps", "CNT", "CNT"]
]

# ===== Dados para equivalência de pontuações =====
dados_pontuacoes = [
    ["pisa_2000_cognitive_item", "PV1MATH", "PV1MATH"],
    ["pisa_2000_cognitive_item", "PV1READ", "PV1READ"],
    ["pisa_2000_cognitive_item", "PV1SCIE", "PV1SCIE"],
    ["pisa_2009_student_sps", "PV1MATH", "PV1MATH"],
    ["pisa_2009_student_sps", "PV1READ", "PV1READ"],
    ["pisa_2009_student_sps", "PV1SCIE", "PV1SCIE"],
    ["pisa_2022_student", "PV1MATH", "PV1MATH"],
    ["pisa_2022_student", "PV1READ", "PV1READ"],
    ["pisa_2022_student", "PV1SCIE", "PV1SCIE"]
]

# ===== Criar pasta de destino, se não existir =====
os.makedirs(PASTA_DESTINO, exist_ok=True)

# ===== Salvar equivalências de países =====
df_paises = pd.DataFrame(dados_paises, columns=["colecao", "campo_detectado", "campo_equivalente"])
df_paises.to_csv(ARQUIVO_EQUIV_PAISES, index=False, encoding="utf-8")
print(f"✔ Arquivo salvo: {ARQUIVO_EQUIV_PAISES}")

# ===== Salvar equivalências de pontuações =====
df_pontos = pd.DataFrame(dados_pontuacoes, columns=["colecao", "campo_detectado", "campo_equivalente"])
df_pontos.to_csv(ARQUIVO_EQUIV_PONTOS, index=False, encoding="utf-8")
print(f"✔ Arquivo salvo: {ARQUIVO_EQUIV_PONTOS}")

