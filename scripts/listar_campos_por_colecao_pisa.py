from pymongo import MongoClient
import os

# Conexão Mongo
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Coleções que queremos inspecionar
colecoes = [
    "pisa_ocde_2000_medias",
    "pisa_ocde_2022_escs_media",
    "medias_pais_item_escs_2022",
    "pisa_2022_student",
    "pisa_2022_student_cog"
]

# Caminho para salvar o arquivo
caminho_saida = "painel_pisa/dados_cloud/campos_colecoes_pisa.txt"

# Garantir que a pasta existe
os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

# Abrir arquivo para escrita
with open(caminho_saida, "w", encoding="utf-8") as f:
    f.write("📌 Campos disponíveis nas coleções relevantes:\n\n")
    for nome in colecoes:
        doc = db[nome].find_one()
        if doc:
            f.write(f"✔ {nome}:\n")
            for campo in list(doc.keys()):
                f.write(f"   - {campo}\n")
            f.write("\n")
        else:
            f.write(f"⚠️ {nome}: coleção vazia ou não encontrada.\n\n")

client.close()
print(f"✅ Resultado salvo em: {caminho_saida}")

