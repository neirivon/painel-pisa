import json

# Caminho para o JSON de entrada
CAMINHO_JSON_ORIGINAL = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022.json"

# Caminho para salvar o novo JSON corrigido
CAMINHO_JSON_CORRIGIDO = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022_prefixado.json"

def aplicar_prefixo_personalizado(json_entrada, json_saida):
    with open(json_entrada, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for item in dados:
        colecao = item.get("colecao_mongodb", "")
        if colecao.startswith("pisa_") and colecao.endswith("_2022"):
            complemento = colecao.replace("pisa_", "").replace("_2022", "")
            item["colecao_mongodb"] = f"protocolo_pisa_2022_{complemento}"

    with open(json_saida, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f"✅ Arquivo salvo com sucesso em: {json_saida}")

# Executar
if __name__ == "__main__":
    aplicar_prefixo_personalizado(CAMINHO_JSON_ORIGINAL, CAMINHO_JSON_CORRIGIDO)

