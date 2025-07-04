# converter_doc_para_docx_corrigido.py
import os
from docx import Document
import subprocess

# Caminho da pasta de origem e destino
pasta_origem = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")000"))
pasta_destino = os.path.join(pasta_origem, 'convertidos')

# Certificar que a pasta de destino existe
os.makedirs(pasta_destino, exist_ok=True)

# Listar arquivos .doc (não .docx) da pasta origem
arquivos_doc = [arq for arq in os.listdir(pasta_origem) if arq.endswith('.doc') and not arq.endswith('.docx')]

for arquivo in arquivos_doc:
    caminho_arquivo_doc = os.path.join(pasta_origem, arquivo)
    nome_novo_docx = os.path.splitext(arquivo)[0] + '.docx'
    caminho_arquivo_docx = os.path.join(pasta_destino, nome_novo_docx)

    print(f"📂 Convertendo {arquivo} para {nome_novo_docx}...")

    try:
        # Usar o LibreOffice em modo headless para conversão real
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "docx",
            "--outdir", pasta_destino,
            caminho_arquivo_doc
        ], check=True)

    except Exception as e:
        print(f"❌ Erro na conversão de {arquivo}: {e}")

print("✅ Conversão de todos os arquivos .doc para .docx concluída corretamente!")

