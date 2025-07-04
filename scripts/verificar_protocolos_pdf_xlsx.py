import os
import json
import pandas as pd
from PyPDF2 import PdfReader

# Caminho da pasta
pasta = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022"

# Palavras-chave (busca case-insensitive)
palavras_chave = ["protocolo", "protocol", "pisa", "ocde"]

# Lista de arquivos relevantes
arquivos_encontrados = []

# Função de verificação
def contem_palavra_chave(texto):
    texto = str(texto).lower()
    return any(p in texto for p in palavras_chave)

# Processamento
for arquivo in os.listdir(pasta):
    caminho = os.path.join(pasta, arquivo)
    if not os.path.isfile(caminho):
        continue

    try:
        if arquivo.endswith(".pdf"):
            reader = PdfReader(caminho)
            texto = ""
            for page in reader.pages[:5]:  # Limita a 5 páginas
                texto += page.extract_text() or ""
            if contem_palavra_chave(texto):
                arquivos_encontrados.append(caminho)
                print(f"✅ PDF útil: {arquivo}")
            else:
                print(f"🔎 PDF ignorado: {arquivo}")

        elif arquivo.endswith(".xlsx"):
            xls = pd.ExcelFile(caminho)
            encontrou = False
            for aba in xls.sheet_names[:5]:  # Limita a 5 abas
                df = xls.parse(aba, nrows=20)  # Limita a 20 linhas
                if df.astype(str).applymap(contem_palavra_chave).any().any():
                    arquivos_encontrados.append(caminho)
                    encontrou = True
                    print(f"✅ XLSX útil: {arquivo}")
                    break
            if not encontrou:
                print(f"🔎 XLSX ignorado: {arquivo}")

        else:
            print(f"📂 Ignorado (outro tipo): {arquivo}")

    except Exception as e:
        print(f"⚠️ Erro ao processar {arquivo}: {e}")

# Exporta JSON
saida_json = os.path.join(pasta, "arquivos_com_protocolos_detectados.json")
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(arquivos_encontrados, f, indent=4, ensure_ascii=False)

print(f"\n📁 JSON salvo em: {saida_json}")
S
