import os
import subprocess

# Diretório onde estão os arquivos de máscara SPSS (.txt)
PASTA_MASCARAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT"
ARQUIVOS_SPSS = [
    "PISA2009_SPSS_cognitive_item.txt",
    "PISA2009_SPSS_student.txt",
    "PISA2009_SPSS_school.txt",
    "PISA2009_SPSS_parent.txt",
    "PISA2009_SPSS_score_cognitive_item.txt"
]

print("🔁 Extraindo schemas JSON...")
for nome_arquivo in ARQUIVOS_SPSS:
    caminho_completo = os.path.join(PASTA_MASCARAS, nome_arquivo)
    print(f"📄 Extraindo: {nome_arquivo}")
    subprocess.run(["python3", "scripts/gerar_schema_json_mascara_2009.py", caminho_completo])

print("\n🔁 Convertendo todos schemas JSON para CSV...")
subprocess.run(["python3", "scripts/converter_schemas_para_csv.py"])

print("\n✅ Processo concluído com sucesso.")

