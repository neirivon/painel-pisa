from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

colecoes_verificar = [
    "pisa_ocde_2000_alunos",
    "pisa_2000_school",
    "pisa_2003_school",
    "pisa_2003_student",
    "pisa_2006_student",
    "pisa_2006_cognitive",
    "pisa_2012_int_stq09_dec11",
    "pisa_2012_int_cog09_td_dec11",
    "pisa_2018_vnm_cog_nans"
]

campos_desejados = ["PV1MATH", "PV1READ", "PV1SCIE"]
resultado = []

for colecao in colecoes_verificar:
    if colecao in db.list_collection_names():
        doc = db[colecao].find_one()
        if doc:
            for campo in doc:
                for padrao in campos_desejados:
                    if padrao in campo.upper():
                        resultado.append({
                            "colecao": colecao,
                            "campo_detectado": campo,
                            "campo_equivalente": padrao
                        })

client.close()

df = pd.DataFrame(resultado)
df.to_csv("dados_processados/mapeamento_campos_desempenho_faltantes.csv", index=False, encoding="utf-8")
print("✔ Arquivo salvo: dados_processados/mapeamento_campos_desempenho_faltantes.csv")

