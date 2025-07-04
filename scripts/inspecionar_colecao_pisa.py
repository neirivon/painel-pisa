from pymongo import MongoClient
import pprint

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

nome_colecoes = [
    "pisa_2022_student", "pisa_2022_student_cog", "pisa_2022_student_qqq",
    "pisa_ocde_2022_escs_media", "medias_pais_item_escs_2022"
]

for nome in nome_colecoes:
    print(f"\n📘 Coleção: {nome}")
    doc = db[nome].find_one()
    pprint.pprint(doc)

client.close()

