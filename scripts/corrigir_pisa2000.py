from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

def corrigir_pisa2000():
    # Conexão com o MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    colecao = db["pisa2000_comparativo_lmc"]

    # Apagar documentos antigos
    resultado_delete = colecao.delete_many({})
    print(f"✅ Documentos apagados: {resultado_delete.deleted_count}")

    # Inserir novos documentos corrigidos
    documentos_corrigidos = [
        {
            "area": "Leitura",
            "tipo": "geral",
            "nota_brasil": 396,
            "nota_ocde": 500,
            "ano": 2000
        },
        {
            "area": "Leitura",
            "tipo": "publica",
            "nota_brasil": 385,
            "nota_ocde": 491,
            "ano": 2000
        },
        {
            "area": "Matemática",
            "tipo": "geral",
            "nota_brasil": 334,
            "nota_ocde": 500,
            "ano": 2000
        },
        {
            "area": "Matemática",
            "tipo": "publica",
            "nota_brasil": 322,
            "nota_ocde": 488,
            "ano": 2000
        },
        {
            "area": "Ciências",
            "tipo": "geral",
            "nota_brasil": 390,
            "nota_ocde": 500,
            "ano": 2000
        },
        {
            "area": "Ciências",
            "tipo": "publica",
            "nota_brasil": 366,
            "nota_ocde": 493,
            "ano": 2000
        }
    ]

    resultado_insert = colecao.insert_many(documentos_corrigidos)
    print(f"✅ Documentos inseridos: {len(resultado_insert.inserted_ids)}")

    # Fechar conexão
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    corrigir_pisa2000()

