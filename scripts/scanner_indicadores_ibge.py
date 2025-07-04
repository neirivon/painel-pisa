import os
import pandas as pd

# Diretório raiz onde estão os arquivos IBGE
DIRETORIO_RAIZ = "/homos.path.join(e, "n")eirivoos.path.join(n, "b")ackup_dados_pesadoos.path.join(s, "I")BGos.path.join(E, "D")ESTAQUES"

# Indicadores buscados
PALAVRAS_CHAVE = {
    "IDHM": ["idhm"],
    "Esperança de vida ao nascer": ["esperança de vida"],
    "Renda per capita": ["renda per capita", "renda média"],
    "População": ["população total", "total de habitantes", "população residente"],
    "Gini": ["índice de gini", "gini"],
    "Taxa de frequência líquida ao ensino médio": ["frequência líquida", "ensino médio", "frequência escolar"]
}

# Extensões suportadas
EXTENSOES_SUPORTADAS = [".xls", ".xlsx"]

# Lista de arquivos úteis
caminhos_utilizados = []

print("📂 Iniciando varredura por indicadores educacionais e sociais...\n")

for raiz, _, arquivos in os.walk(DIRETORIO_RAIZ):
    for nome_arquivo in arquivos:
        if any(nome_arquivo.endswith(ext) for ext in EXTENSOES_SUPORTADAS):
            caminho_completo = os.path.join(raiz, nome_arquivo)
            indicadores_encontrados = set()

            try:
                if nome_arquivo.endswith(".xls"):
                    df = pd.read_excel(caminho_completo, engine="xlrd", nrows=20)
                else:
                    df = pd.read_excel(caminho_completo, engine="openpyxl", nrows=20)

                texto = " ".join(str(cell).lower() for cell in df.columns)
                texto += " " + " ".join(str(cell).lower() for row in df.itertuples(index=False) for cell in row)

                for indicador, palavras in PALAVRAS_CHAVE.items():
                    if any(p in texto for p in palavras):
                        indicadores_encontrados.add(indicador)

                if indicadores_encontrados:
                    caminhos_utilizados.append({
                        "arquivo": nome_arquivo,
                        "caminho": caminho_completo,
                        "destaques_encontrados": ", ".join(sorted(indicadores_encontrados))
                    })
                    print(f"✅ {nome_arquivo}\n   → {', '.join(sorted(indicadores_encontrados))}")

            except Exception as e:
                print(f"⚠️ Erro ao processar {caminho_completo}: {e}")

# Gerar relatório em CSV
if caminhos_utilizados:
    df_resultado = pd.DataFrame(caminhos_utilizados)
    output_path = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "a")rquivos_com_potencial.csv"
    df_resultado.to_csv(output_path, index=False)
    print(f"\n📁 Arquivo '{output_path}' gerado com os caminhos úteis e indicadores.")
else:
    print("\n❌ Nenhum arquivo útil identificado com os indicadores procurados.")

