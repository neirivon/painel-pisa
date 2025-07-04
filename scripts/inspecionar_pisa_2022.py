from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://admin:admin123@localhost:27017")

# === 1. Pontuações cognitivas por aluno ===
print("\n📘 Amostra - pisa_2022_student_cog:")
amostra_cog = client["pisa"]["pisa_2022_student_cog"].find_one()
pprint(amostra_cog)

# === 2. Dados socioeconômicos e questionário ===
print("\n📗 Amostra - pisa_2022_student_qqq:")
amostra_qqq = client["pisa"]["pisa_2022_student_qqq"].find_one()
pprint(amostra_qqq)

# === 3. Médias nacionais por país (cognitivo) ===
print("\n📊 Amostra - pisa_2022_country_cognitive:")
amostra_country = client["pisa"]["pisa_2022_country_cognitive"].find_one()
pprint(amostra_country)

client.close()

