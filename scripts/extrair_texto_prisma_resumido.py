import json

# Caminho do JSON original corrompido
json_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_resumido_populado.json"

# Caminho do TXT de saída
txt_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/PRISMA_2020_resumido_texto_bruto.txt"

# Lê o JSON e extrai o campo 'descricao' ou 'itens'
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

texto = ""
if "itens" in data and isinstance(data["itens"], list):
    for item in data["itens"]:
        texto += f"Item {item.get('numero', '?')}. {item.get('titulo', '').strip()}\n"
        texto += f"{item.get('descricao', '').strip()}\n\n"
else:
    texto = json.dumps(data, ensure_ascii=False, indent=2)

# Salva como .txt
with open(txt_output_path, "w", encoding="utf-8") as f:
    f.write(texto.strip())

print(f"✔ Texto plano exportado para: {txt_output_path}")

