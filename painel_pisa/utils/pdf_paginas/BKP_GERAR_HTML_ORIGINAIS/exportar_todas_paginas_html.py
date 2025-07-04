# painel_pisos.path.join(a, "u")tilos.path.join(s, "p")df_paginaos.path.join(s, "e")xportar_todas_paginas_html.py

import os
from pathlib import Path

from gerar_html_01_Mapa_e_Rubricas_TMAP import gerar_html_01
from gerar_html_01_Resumo_Edicao import gerar_html_01_resumo
from gerar_html_02_Distribuicao_Rubricas_SAEB import gerar_html_02
from gerar_html_03_Comparativo_PISA_OCDE import gerar_html_03
from gerar_html_04_politicas_publicas import gerar_html_04
from gerar_html_05_Rubricas_Avaliativas import gerar_html_05
from gerar_html_06_Exemplos_Paragrafos_Analisados import gerar_html_06
from gerar_html_07_Resumo_Geral_INEP_2000 import gerar_html_07
from gerar_html_08_Comparativo_PISA_SAEB import gerar_html_08
from gerar_html_10_Rubricas_Regionais_Contextualizadas import gerar_html_10
from gerar_html_11_Explicacao_Didatica_Integrada import gerar_html_11
from gerar_html_12_Situacoes_Interdisciplinares_2000 import gerar_html_12
from gerar_html_99_Referencias_Bibliograficas import gerar_html_99

# === Lista de funções ===
html_funcoes = [
    ("01_Mapa_e_Rubricas_TMAP", gerar_html_01),
    ("01_Resumo_Edicao", gerar_html_01_resumo),
    ("02_Distribuicao_Rubricas_SAEB", gerar_html_02),
    ("03_Comparativo_PISA_OCDE", gerar_html_03),
    ("04_politicas_publicas", gerar_html_04),
    ("05_Rubricas_Avaliativas", gerar_html_05),
    ("06_Exemplos_Paragrafos_Analisados", gerar_html_06),
    ("07_Resumo_Geral_INEP_2000", gerar_html_07),
    ("08_Comparativo_PISA_SAEB", gerar_html_08),
    ("10_Rubricas_Regionais_Contextualizadas", gerar_html_10),
    ("11_Explicacao_Didatica_Integrada", gerar_html_11),
    ("12_Situacoes_Interdisciplinares_2000", gerar_html_12),
    ("99_Referencias_Bibliograficas", gerar_html_99),
]

# === Caminho absoluto da pasta de saída ===
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".os.path.join(., ".")os.path.join(., ".")os.path.join(., "e")xports_html"))
Path(output_dir).mkdir(parents=True, exist_ok=True)

# === Exportar arquivos HTML ===
for nome, funcao in html_funcoes:
    print(f"📄 Exportando {nome} para {output_diros.path.join(}, "{")nome}.html...")
    html = funcao()
    with open(os.path.join(output_dir, f"{nome}.html"), "w", encoding="utf-8") as f:
        f.write(html)

print("✅ Todos os arquivos HTML exportados com sucesso.")

