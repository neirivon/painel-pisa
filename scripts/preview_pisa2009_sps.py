import os
import pandas as pd

# === CONFIGURAÇÕES ===
CAMINHO_BASE = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT")
ARQUIVO_DADOS = os.path.join(CAMINHO_BASE, "INT_SCQ09_Dec11.txt")
ARQUIVO_MASCARA = os.path.join(CAMINHO_BASE, "PISA2009_SPSS_cognitive_item.txt")
EXPORTAR_CSV = True  # ← Defina como False se não quiser salvar

# === Função para carregar máscara de colunas fixas ===
def carregar_mascara_spss(arquivo_mascara):
    col_names = []
    col_specs = []
    with open(arquivo_mascara, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) >= 3:
                try:
                    nome = partes[0]
                    inicio = int(partes[1]) - 1  # início 0-based
                    fim = int(partes[2])         # fim exclusivo
                    col_names.append(nome)
                    col_specs.append((inicio, fim))
                except ValueError:
                    continue  # Ignora linhas não numéricas
    return col_names, col_specs

# === Função principal ===
def visualizar_amostra():
    print("📥 Lendo máscara SPS...")
    col_names, col_specs = carregar_mascara_spss(ARQUIVO_MASCARA)

    print("📄 Lendo as primeiras 5 linhas formatadas...")
    df = pd.read_fwf(ARQUIVO_DADOS, names=col_names, colspecs=col_specs, encoding='latin1', nrows=5)

    print("📊 Amostra das 5 primeiras linhas:")
    print(df.head().to_string(index=False))

    if EXPORTAR_CSV:
        csv_saida = os.path.join(CAMINHO_BASE, "preview_pisa2009.csv")
        df.to_csv(csv_saida, index=False)
        print(f"✅ Amostra exportada para: {csv_saida}")

# === Execução ===
if __name__ == "__main__":
    visualizar_amostra()

