import json
import re

# Caminho do TXT de entrada (conteúdo do checklist PRISMA 2020 resumido)
txt_input_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/PRISMA_2020_resumido_texto_bruto.txt"

# Caminho do JSON de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_resumido_populado.json"

# Lê o texto
with open(txt_input_path, "r", encoding="utf-8") as f:
    texto = f.read()

# Usa expressão regular para identificar os blocos "Item X. Título"
blocos = re.split(r"(?=Item\s+\d+\.)", texto)
itens = []

for bloco in blocos:
    bloco = bloco.strip()
    if not bloco:
        continue
    try:
        # Separa a primeira linha (Item X. Título) do restante
        primeira_linha, *resto = bloco.split("\n", 1)
        numero = int(re.search(r"Item\s+(\d+)\.", primeira_linha).group(1))
        titulo = primeira_linha.split(".", 1)[1].strip()
        descricao = resto[0].strip() if resto else ""
        itens.append({
            "numero": numero,
            "titulo": titulo,
            "descricao": descricao
        })
    except Exception as e:
        print(f"⚠ Erro ao processar bloco:\n{bloco}\nErro: {e}\n")

# Estrutura final
output = {
    "versao": "PRISMA 2020",
    "tipo": "resumido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf",
    "itens": itens
}

# Salva o JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✔ JSON PRISMA 2020 resumido salvo em: {json_output_path}")
print(f"✔ Total de itens inseridos: {len(itens)}")

