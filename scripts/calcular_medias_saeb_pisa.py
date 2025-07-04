from pymongo import MongoClient

# Conectar ao MongoDB local
client = MongoClient("mongodb://admin:admin123@localhost:27017")

# === 1. PISA 2022 - Student Cognitive (somente Brasil)
pisa_cog = client["pisa"]["pisa_2022_student_cog"]
cursor_pisa = pisa_cog.find({"CNT": {"$in": ["BR", "BRA"]}}, {
    "PV1READ": 1, "PV1MATH": 1, "PV1SCIE": 1, "_id": 0
})

read_vals, math_vals, scie_vals = [], [], []
for doc in cursor_pisa:
    if "PV1READ" in doc: read_vals.append(doc["PV1READ"])
    if "PV1MATH" in doc: math_vals.append(doc["PV1MATH"])
    if "PV1SCIE" in doc: scie_vals.append(doc["PV1SCIE"])

# Calcular médias do PISA Brasil
media_read = sum(read_vals) / len(read_vals) if read_vals else None
media_math = sum(math_vals) / len(math_vals) if math_vals else None
media_scie = sum(scie_vals) / len(scie_vals) if scie_vals else None

# === 2. SAEB 2021 - Municípios 9º ano (Brasil completo)
saeb = client["saeb"]["saeb_2021_municipios_9ano"]
cursor_saeb = saeb.find({}, {"MEDIA_9_LP": 1, "MEDIA_9_MT": 1, "_id": 0})

lp_vals, mt_vals = [], []
for doc in cursor_saeb:
    if "MEDIA_9_LP" in doc: lp_vals.append(doc["MEDIA_9_LP"])
    if "MEDIA_9_MT" in doc: mt_vals.append(doc["MEDIA_9_MT"])

# Calcular médias do SAEB Brasil
media_saeb_lp = sum(lp_vals) / len(lp_vals) if lp_vals else None
media_saeb_mt = sum(mt_vals) / len(mt_vals) if mt_vals else None

client.close()

# Exibir resultados
print("\n📊 MÉDIAS - PISA 2022 (Brasil)")
print(f"Leitura (PV1READ):     {round(media_read, 2)}")
print(f"Matemática (PV1MATH):  {round(media_math, 2)}")
print(f"Ciências (PV1SCIE):    {round(media_scie, 2)}")

print("\n📘 MÉDIAS - SAEB 2021 (Brasil)")
print(f"Língua Portuguesa:     {round(media_saeb_lp, 2)}")
print(f"Matemática:            {round(media_saeb_mt, 2)}")

