# painel_pisos.path.join(a, "u")tilos.path.join(s, "p")df_paginaos.path.join(s, "e")xportar_todas_paginas_html.py

import os
from pathlib import Path
import importlib.util

# === Configurações ===
base_dir = os.path.dirname(__file__)
output_dir = os.path.abspath(os.path.join(base_dir, ".os.path.join(., ".")os.path.join(., ".")os.path.join(., "e")xports_html"))
Path(output_dir).mkdir(parents=True, exist_ok=True)

# === Lista de arquivos e funções correspondentes ===
scripts = [
    ("gerar_html_01_Mapa_e_Rubricas_TMAP.py", "gerar_html_01", "01_Mapa_e_Rubricas_TMAP"),
    ("gerar_html_01_Resumo_Edicao.py", "gerar_html_01_resumo", "01_Resumo_Edicao"),
    ("gerar_html_02_Distribuicao_Rubricas_SAEB.py", "gerar_html_02", "02_Distribuicao_Rubricas_SAEB"),
    ("gerar_html_03_Comparativo_PISA_OCDE.py", "gerar_html_03", "03_Comparativo_PISA_OCDE"),
    ("gerar_html_04_politicas_publicas.py", "gerar_html_04", "04_politicas_publicas"),
    ("gerar_html_05_Rubricas_Avaliativas.py", "gerar_html_05", "05_Rubricas_Avaliativas"),
    ("gerar_html_06_Exemplos_Paragrafos_Analisados.py", "gerar_html_06", "06_Exemplos_Paragrafos_Analisados"),
    ("gerar_html_07_Resumo_Geral_INEP_2000.py", "gerar_html_07", "07_Resumo_Geral_INEP_2000"),
    ("gerar_html_08_Comparativo_PISA_SAEB.py", "gerar_html_08", "08_Comparativo_PISA_SAEB"),
    ("gerar_html_10_Rubricas_Regionais_Contextualizadas.py", "gerar_html_10", "10_Rubricas_Regionais_Contextualizadas"),
    ("gerar_html_11_Explicacao_Didatica_Integrada.py", "gerar_html_11", "11_Explicacao_Didatica_Integrada"),
    ("gerar_html_12_Situacoes_Interdisciplinares_2000.py", "gerar_html_12", "12_Situacoes_Interdisciplinares_2000"),
    ("gerar_html_99_Referencias_Bibliograficas.py", "gerar_html_99", "99_Referencias_Bibliograficas"),
]

# === Executar exportação ===
for script_file, func_name, output_name in scripts:
    script_path = os.path.join(base_dir, script_file)
    if not os.path.exists(script_path):
        print(f"❌ Arquivo não encontrado: {script_file}")
        continue

    spec = importlib.util.spec_from_file_location("modulo_temp", script_path)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    if not hasattr(modulo, func_name):
        print(f"❌ Função {func_name} não encontrada em {script_file}")
        continue

    html = getattr(modulo, func_name)()
    output_path = os.path.join(output_dir, f"{output_name}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Exportado: {output_name}.html")

print("🎉 Todos os arquivos HTML foram exportados com sucesso.")

