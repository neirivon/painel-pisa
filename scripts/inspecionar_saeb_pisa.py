from pymongo import MongoClient
from pprint import pprint

# Conexão com MongoDB local
client = MongoClient("mongodb://admin:admin123@localhost:27017")

# Acessar SAEB
db_saeb = client["saeb"]
doc_saeb = db_saeb["saeb_2021_municipios_9ano"].find_one()
print("\n📘 Amostra - SAEB 2021 (municípios 9º ano):")
pprint(doc_saeb)

# Acessar PISA
db_pisa = client["pisa"]
doc_pisa = db_pisa["cy1mdai_stu_qqq"].find_one()
print("\n📗 Amostra - PISA 2022 (cy1mdai_stu_qqq):")
pprint(doc_pisa)

client.close()

