import json
import csv

# Caminhos de entrada e saída
json_path = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/schema_cognitive_item_2009.json"
csv_path = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/schema_cognitive_item_2009.csv"

# Carregar JSON
with open(json_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

# Exportar para CSV
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["campo", "inicio", "fim", "tipo"])
    for item in schema:
        writer.writerow([item["campo"], item["inicio"], item["fim"], item["tipo"]])

print(f"✅ Exportado com sucesso para: {csv_path}")

