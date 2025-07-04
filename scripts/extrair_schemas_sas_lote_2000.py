import os
import re
import json
import csv

# Caminho da pasta com os arquivos .sas
PASTA_SAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS"
PASTA_SAIDA = os.path.join(PASTA_SAS, "schemas")
os.makedirs(PASTA_SAIDA, exist_ok=True)

def extrair_schema_input(sas_path):
    with open(sas_path, "r", encoding="latin1") as f:
        conteudo = f.read()

    # Captura tudo entre 'input' e ';'
    match = re.search(r'\binput\b(.*?)\s*;', conteudo, re.DOTALL | re.IGNORECASE)
    if not match:
        return []

    bloco = match.group(1).strip()

    linhas = bloco.splitlines()
    variaveis = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        # Ex: st12q01            51-51
        match = re.match(r"(\w+)\s+(\$?)(\d+)-(\d+)", linha)
        if match:
            nome, tipo, ini, fim = match.groups()
            variaveis.append({
                "nome": nome,
                "tipo": "string" if tipo == "$" else "int",
                "inicio": int(ini),
                "fim": int(fim)
            })

    return variaveis

def salvar_json_csv(schema, nome_base):
    json_path = os.path.join(PASTA_SAIDA, f"schema_{nome_base}.json")
    csv_path = os.path.join(PASTA_SAIDA, f"schema_{nome_base}.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "tipo", "inicio", "fim"])
        writer.writeheader()
        writer.writerows(schema)

    print(f"✅ Gerado: {os.path.basename(json_path)} e {os.path.basename(csv_path)}")

def processar_todos():
    print("🔁 Processando arquivos SAS...")
    for nome in os.listdir(PASTA_SAS):
        if nome.lower().endswith(".sas"):
            caminho = os.path.join(PASTA_SAS, nome)
            nome_base = nome.replace("PISA2000_SAS_", "").replace(".sas", "").lower()

            schema = extrair_schema_input(caminho)
            if schema:
                salvar_json_csv(schema, nome_base)
            else:
                print(f"⚠️ Nenhum schema extraído de {nome}")

    print("🏁 Lote concluído.")

if __name__ == "__main__":
    processar_todos()

