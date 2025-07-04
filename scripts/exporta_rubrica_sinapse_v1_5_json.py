import pymongo
import json

def exportar_rubrica_v1_5_para_json():
    try:
        cliente = pymongo.MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
        db = cliente["rubricas"]
        colecao = db["rubrica_sinapse"]

        rubrica = colecao.find_one(
            {"nome": "rubrica_sinapse_ia", "versao": "v1.5", "status": "ativa"},
            {"_id": 0}
        )

        if rubrica:
            caminho_arquivo = "/home/neirivon/Downloads/rubrica_sinapse_ia_v1_5.json"
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(rubrica, f, ensure_ascii=False, indent=2)
            print(f"✅ Arquivo '{caminho_arquivo}' gerado com sucesso.")
        else:
            print("⚠️ Rubrica v1.5 ativa não encontrada.")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    exportar_rubrica_v1_5_para_json()

