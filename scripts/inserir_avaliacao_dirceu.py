from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
collection = db["avaliacao_rar_sinapse_ia"]

documento_avaliacao = {
    "juiz_avaliador": "Dirceu Nogueira de Sales Duarte Júnior",
    "email_do_juiz_avaliador": "dirceu@ufu.br",
    "dimensao_avaliada": "Progressão Cognitiva Emocional",
    "clareza_e_objetividade": "4",
    "coerencia_entre_descritores": "4",
    "adequacao_a_pratica_pedagogica": "4",
    "alinhamento_entidades_normativas_e_avaliativas": "4",
    "originalidade_e_contribuicao": "4",
    "comentario": "Exemplar",
    "hash": "",
    "data": datetime.utcnow().isoformat(),
    "navegador": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "sistema_operacional": "Linux x86_64",
    "idioma": "pt-BR",
    "ip_publico": "2804:1e68:c211:6b02:8014:e4e4:d387:fa63"
}

inserido = collection.insert_one(documento_avaliacao)
print(f"Documento inserido com ID: {inserido.inserted_id}")
client.close()
