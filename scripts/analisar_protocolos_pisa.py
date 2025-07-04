import os
import mimetypes
from pathlib import Path
import pandas as pd

# Caminho da pasta que será analisada
folder_path = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022"

# Lista que armazenará os dados
files_info = []

# Função auxiliar para identificar o tipo do arquivo
def get_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        ext = Path(filepath).suffix.lower()
        if ext == ".pdf":
            return "application/pdf"
        elif ext == ".xlsx":
            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif ext == ".csv":
            return "text/csv"
        elif ext in [".png", ".jpg", ".jpeg", ".svg"]:
            return "image"
        else:
            return "unknown"
    return mime_type

# Percorrer os arquivos
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if os.path.isfile(filepath):
        mime = get_mime_type(filepath)
        files_info.append({
            "Arquivo": filename,
            "Caminho": filepath,
            "Tipo": mime,
            "Usável na Página?": "Sim" if mime in [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/csv"
            ] else "Não"
        })

# Criar o DataFrame
df = pd.DataFrame(files_info)

# Filtrar arquivos úteis
df_utilizaveis = df[df["Usável na Página?"] == "Sim"]

# Caminho de saída do JSON
output_dir = "/home/neirivon/dados_processados/protocolos"
os.makedirs(output_dir, exist_ok=True)
json_path = os.path.join(output_dir, "dados_protocolos_utilizaveis.json")

# Salvar o JSON
df_utilizaveis.to_json(json_path, orient="records", indent=2, force_ascii=False)

print(f"✅ JSON com arquivos utilizáveis salvo em:\n{json_path}")

