from pymongo import MongoClient
from pprint import pformat
from pathlib import Path

# Conectar ao MongoDB local
client = MongoClient("mongodb://admin:admin123@localhost:27017")

# === Exportar amostra da coleção pisa_2022_student ===
colecao_student = client["pisa"]["pisa_2022_student"]
docs_student = list(colecao_student.find({}, {"_id": 0}).limit(30))
texto_student = "\n\n".join([pformat(doc) for doc in docs_student])
Path("amostra_pisa_2022_student.txt").write_text(texto_student, encoding="utf-8")

# === Exportar amostra da coleção pisa_2022_student_qqq ===
colecao_student_qqq = client["pisa"]["pisa_2022_student_qqq"]
docs_qqq = list(colecao_student_qqq.find({}, {"_id": 0}).limit(30))
texto_qqq = "\n\n".join([pformat(doc) for doc in docs_qqq])
Path("amostra_pisa_2022_student_qqq.txt").write_text(texto_qqq, encoding="utf-8")

client.close()

print("✅ Arquivos gerados:")
print("→ amostra_pisa_2022_student.txt")
print("→ amostra_pisa_2022_student_qqq.txt")

