# listar_colecoes_saeb.py

from pymongo import MongoClient

def main():
    # Conectar ao MongoDB com autenticação
    MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
    client = MongoClient(MONGO_URI)

    try:
        # Selecionar o banco 'saeb'
        db = client["saeb"]

        # Listar coleções disponíveis
        colecoes = db.list_collection_names()
        print("📚 Coleções no banco 'saeb':\n")
        for nome in colecoes:
            total = db[nome].count_documents({})
            print(f"📁 {nome:<40} → {total} documentos")
    
    except Exception as e:
        print(f"❌ Erro ao acessar o banco: {e}")
    
    finally:
        # Fechar a conexão com o MongoDB
        client.close()
        print("\n🔒 Conexão com MongoDB encerrada com segurança.")

if __name__ == "__main__":
    main()

