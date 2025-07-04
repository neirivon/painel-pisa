import os
import csv
from pymongo import MongoClient
from tqdm import tqdm

# Configurações
ARQUIVOS = {
    "math": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_math_v3.txt",
    "read": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_read_v3.txt",
    "scie": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_scie_v3.txt"
}
COLECAO = "pisa_2000_student"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"

# Conectar ao MongoDB
cliente = MongoClient(MONGO_URI)
db = cliente[DB_NAME]
colecao = db[COLECAO]

def detectar_delimitador(filepath):
    with open(filepath, "r", encoding="latin1") as f:
        linha = f.readline()
        if ";" in linha: return ";"
        elif "\t" in linha: return "\t"
        elif "," in linha: return ","
        else: return None

def importar_arquivo(area, caminho):
    print(f"\n📥 Lendo arquivo: {caminho}")
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return

    delimitador = detectar_delimitador(caminho)
    if not delimitador:
        print(f"❌ Delimitador não identificado para: {caminho}")
        return

    with open(caminho, "r", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=delimitador)
        documentos = []
        for linha in leitor:
            doc = {k.strip(): v.strip() for k, v in linha.items()}
            doc["area"] = area
            documentos.append(doc)

    if not documentos:
        print(f"⚠️ Nenhum documento encontrado em: {caminho}")
        return

    print(f"📦 Inserindo {len(documentos):,} documentos na coleção '{COLECAO}'...")
    colecao.insert_many(documentos)
    print(f"✅ Área '{area}' importada com sucesso!")

def verificar_total_por_area():
    print("\n📊 Totais por área:")
    for area in ARQUIVOS.keys():
        count = colecao.count_documents({"area": area})
        print(f"  📁 {area:<6} → {count:,} documentos")

def main():
    for area, caminho in ARQUIVOS.items():
        importar_arquivo(area, caminho)

    verificar_total_por_area()
    cliente.close()
    print("🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

