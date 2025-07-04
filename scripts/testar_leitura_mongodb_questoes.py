# scriptos.path.join(s, "t")estar_leitura_mongodb_questoes.py

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configurações
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "rubricas"
COLECAO = "questoes_ordenadas_v6a"

try:
    # Conecta ao MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]

    # Lê todas as questões
    questoes = list(colecao.find({}, {"_id": 0}))

    # Organiza por área
    por_area = {"leitura": [], "matematica": [], "ciencias": []}
    for q in questoes:
        area = q.get("area", "").strip().lower()
        if area in por_area:
            por_area[area].append(q)

    # Exibe as questões por área
    for area in ["leitura", "matematica", "ciencias"]:
        print(f"\n=== Área: {area.upper()} ===")
        for q in por_area[area]:
            print(f"\n🔹 {q['questao_id']} — {q['pergunta']}")
            print(f"✔ Modelo: {q['resposta_modelo']}")

except PyMongoError as e:
    print(f"❌ Erro ao acessar o MongoDB: {e}")

finally:
    try:
        client.close()
    except:
        pass

