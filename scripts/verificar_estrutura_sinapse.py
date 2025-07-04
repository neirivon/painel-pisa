# scriptos.path.join(s, "v")erificar_estrutura_sinapse.py

import os

estruturas_esperadas = {
    "rubricas": {
        "path": os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "r")ubricas/"),
        "arquivos_esperados": [
            "rubrica_sinapse_v6_adaptada.json",
            "rubrica_sinapse_v6_adaptada.csv",
            "avaliar_rubricas_v1.json",
            "avaliar_rubricas_v1.csv"
        ]
    },
    "questoes": {
        "path": os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "q")uestoes/"),
        "arquivos_esperados": [
            "questoes_pisa_tri_mineiro_completas.json",
            "questoes_pisa_ordenadas.json",
            "questoes_pisa_ordenadas.csv"
        ]
    },
    "respostas": {
        "path": os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "r")espostas/"),
        "arquivos_esperados": [
            "respostas_exemplo_por_area.txt"
        ]
    }
}

def verificar_estrutura():
    print("🔍 Verificando estrutura de diretórios do SINAPSE2.0...\n")
    inconsistencias = False

    for categoria, info in estruturas_esperadas.items():
        caminho = os.path.expanduser(info["path"])
        print(f"📁 Pasta: {caminho}")
        if not os.path.exists(caminho):
            print(f"❌ Pasta não encontrada: {caminho}\n")
            inconsistencias = True
            continue

        arquivos_encontrados = os.listdir(caminho)
        for esperado in info["arquivos_esperados"]:
            if esperado not in arquivos_encontrados:
                print(f"⚠️ Arquivo ausente: {esperado}")
                inconsistencias = True
        print("✅ Verificação da pasta concluída.\n")

    if not inconsistencias:
        print("✅ Estrutura do projeto está consistente! Nenhum erro encontrado.")
    else:
        print("⚠️ Foram encontradas inconsistências. Verifique os avisos acima.")

if __name__ == "__main__":
    verificar_estrutura()

