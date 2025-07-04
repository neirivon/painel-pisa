import json
import re

# Caminho do arquivo de texto extraído do PDF expandido
txt_input_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/PRISMA_2020_expandido_texto_bruto.txt"

# Caminho do JSON de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_expandido_populado.json"

# Lê o conteúdo do texto
with open(txt_input_path, "r", encoding="utf-8") as f:
    texto = f.read()

# Expressão regular para identificar "Item X. Título"
padrao = re.compile(r"(Item\s+(\d+)\.\s+(.+?))(?:\n|\r|$)", re.MULTILINE)

# Lista de resultados (composição inicial)
matches = list(padrao.finditer(texto))
itens = []

for i, match in enumerate(matches):
    numero = int(match.group(2))
    titulo = match.group(3).strip()

    # Pega o trecho entre esse item e o próximo (ou até o final)
    inicio = match.end()
    fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
    descricao = texto[inicio:fim].strip().replace("\n", " ")

    itens.append({
        "numero": numero,
        "titulo": titulo,
        "descricao": descricao
    })

# Exibir diagnóstico
print(f"✔ Total de itens detectados: {len(itens)}")
for i, item in enumerate(itens[:3]):
    print(f"Item {item['numero']}: {item['titulo']}")
    print(f"Descrição: {item['descricao'][:100]}...")
    print("---")

# Estrutura final do JSON
output = {
    "versao": "PRISMA 2020",
    "tipo": "expandido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 expanded checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf",
    "itens": itens
}

# Salvar JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✔ JSON final salvo em: {json_output_path}")

