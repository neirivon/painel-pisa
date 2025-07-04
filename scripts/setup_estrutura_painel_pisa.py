# setup_estrutura_painel_pisa.py
import os

def criar_estrutura():
    pastas = [
        "painel_pisa",
        "painel_pisos.path.join(a, "p")ages",
        "painel_pisos.path.join(a, "a")ssetos.path.join(s, "i")magens",
        "painel_pisos.path.join(a, "a")ssetos.path.join(s, "l")ogos",
        "painel_pisos.path.join(a, "u")tils"
    ]

    arquivos = {
        "painel_pisos.path.join(a, "H")ome.py": "# Página Inicial",
        "painel_pisos.path.join(a, "p")ageos.path.join(s, "0")1_Comparativo_Brasil_OCDE.py": "# Comparativo Brasil x Média OCDE",
        "painel_pisos.path.join(a, "p")ageos.path.join(s, "0")2_Diagnostico_Regional.py": "# Diagnóstico Regional do Brasil",
        "painel_pisos.path.join(a, "p")ageos.path.join(s, "0")3_Rubricas_Avaliativas.py": "# Propostas de Rubricas Avaliativas",
        "painel_pisos.path.join(a, "p")ageos.path.join(s, "0")4_Politicas_Publicas.py": "# Propostas de Políticas Públicas",
        "painel_pisos.path.join(a, "p")ageos.path.join(s, "0")5_Conclusao_Propostas_Finais.py": "# Conclusão e Propostas Finais",
        "painel_pisos.path.join(a, "u")tilos.path.join(s, "c")onexao_mongo.py": "# Função de conexão MongoDB",
        "painel_pisos.path.join(a, "u")tilos.path.join(s, "f")uncoes_graficos.py": "# Funções de geração de gráficos",
        "painel_pisos.path.join(a, "u")tilos.path.join(s, "f")uncoes_rubricas.py": "# Funções para rubricas avaliativas",
        "painel_pisos.path.join(a, "R")EADME.md": "# Guia rápido do Painel PISA - SINAPSE 2.0"
    }

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        print(f"📁 Pasta criada: {pasta}")

    for arquivo, conteudo in arquivos.items():
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"📄 Arquivo criado: {arquivo}")

if __name__ == "__main__":
    criar_estrutura()
    print("\n✅ Estrutura de diretórios e arquivos do Painel PISA criada com sucesso!")

