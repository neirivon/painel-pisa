from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

try:
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["rubricas"]
    colecao = db["questoes_ordenadas_v6a"]

    questoes = list(colecao.find({}, {"_id": 0}))
    if not questoes:
        print("⚠️ Nenhuma questão encontrada na coleção.")
        exit()

    agrupadas = {"leitura": [], "matematica": [], "ciencias": []}
    for q in questoes:
        area = q.get("area", "desconhecida").lower()
        agrupadas.setdefault(area, []).append(q)

    for area in ["leitura", "matematica", "ciencias"]:
        print(f"\n=== Área: {area.upper()} ===")
        for q in agrupadas.get(area, []):
            print(f"\n🔹 {q['questao_id']} — {q['pergunta']}")
            print(f"✔ Modelo: {q['resposta_modelo']}")

    client.close()

except Exception as e:
    print(f"❌ Erro ao acessar o MongoDB: {e}")
