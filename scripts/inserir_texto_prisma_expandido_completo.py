import json

# Caminho do arquivo de texto extraído do PDF expandido
txt_input_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/PRISMA_2020_expandido_texto_bruto.txt"

# Caminho do JSON de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_expandido_populado.json"

# Lê o conteúdo do texto bruto
with open(txt_input_path, "r", encoding="utf-8") as f:
    texto = f.read()

# Cria um único item com todo o conteúdo bruto
itens = [
    {
        "numero": 0,
        "titulo": "Checklist PRISMA expandido completo",
        "descricao": texto.strip()
    }
]

# Estrutura final do JSON
output = {
    "versao": "PRISMA 2020",
    "tipo": "expandido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 expanded checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf",
    "itens": itens
}

# Salva o JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✔ JSON final salvo com o texto bruto completo em: {json_output_path}")

