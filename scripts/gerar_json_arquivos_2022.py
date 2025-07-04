import os
import json

# Caminho da pasta com os arquivos de 2022
pasta_2022 = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022"

# Lista todos os arquivos válidos (PDF/XLSX, por exemplo)
arquivos_2022 = [
    os.path.join(pasta_2022, f)
    for f in os.listdir(pasta_2022)
    if os.path.isfile(os.path.join(pasta_2022, f))
]

# Caminho completo do JSON de saída
saida_json = os.path.join(pasta_2022, "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/protocolos_pisa_2022.json")

# Salva a lista como JSON
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(arquivos_2022, f, indent=4, ensure_ascii=False)

print(f"✅ JSON gerado com {len(arquivos_2022)} arquivos.")
print(f"📁 Salvo em: {saida_json}")

