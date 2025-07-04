import os
import json
import csv
import chardet

PASTA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT"
ARQUIVOS = [
    "PISA2009_SPSS_cognitive_item.txt",
    "PISA2009_SPSS_student.txt",
    "PISA2009_SPSS_school.txt",
    "PISA2009_SPSS_parent.txt",
    "PISA2009_SPSS_score_cognitive_item.txt",
]

def detectar_codificacao(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as f:
        resultado = chardet.detect(f.read())
    return resultado['encoding'] or 'utf-8'

def extrair_schema_de_txt(linhas):
    schema = []
    for linha in linhas:
        linha = linha.strip()
        if linha == "." or linha.upper().startswith("EXECUTE"):
            continue
        partes = linha.split()
        if len(partes) >= 4:
            nome = partes[0]
            inicio = int(partes[1].split("-")[0])
            fim = int(partes[3]) if partes[2] == "-" else int(partes[2].split("-")[1])
            tipo = partes[-1].replace("(", "").replace(")", "")
            schema.append({
                "nome": nome,
                "inicio": inicio,
                "fim": fim,
                "tipo": tipo
            })
        else:
            print(f"⚠️ Ignorando linha inválida: {linha}")
    return schema

def salvar_json_csv(schema, nome_base):
    json_path = os.path.join(PASTA, f"{nome_base}.json")
    csv_path = os.path.join(PASTA, f"{nome_base}.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON gerado: {os.path.basename(json_path)}")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "inicio", "fim", "tipo"])
        writer.writeheader()
        writer.writerows(schema)
    print(f"✅ CSV gerado: {os.path.basename(csv_path)}")

print("🔁 Iniciando processamento...")
for arquivo in ARQUIVOS:
    caminho_txt = os.path.join(PASTA, arquivo)
    nome_base = f"schema_{arquivo.replace('PISA2009_SPSS_', '').replace('.txt', '')}_2009"

    if not os.path.exists(caminho_txt) or os.path.getsize(caminho_txt) == 0:
        print(f"❌ Arquivo ausente ou vazio: {arquivo}")
        continue

    codificacao = detectar_codificacao(caminho_txt)
    try:
        with open(caminho_txt, "r", encoding=codificacao) as f:
            linhas = f.readlines()
        schema = extrair_schema_de_txt(linhas)
        salvar_json_csv(schema, nome_base)
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

print("\n✅ Processo concluído com sucesso.")

