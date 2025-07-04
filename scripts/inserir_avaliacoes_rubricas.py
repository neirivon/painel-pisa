from pymongo import MongoClient
from datetime import datetime
import json

# Conectar ao MongoDB com autenticação
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao_rubricas = db["rubricas_referenciais"]
colecao_avaliacoes = db["avaliacoes_rubricas_referenciais"]

# Carregar as rubricas
rubricas = list(colecao_rubricas.find())

# Critérios
criterios = [
    "Clareza Conceitual",
    "Estrutura Progressiva (níveis)",
    "Aplicabilidade Pedagógica",
    "Exemplos Práticos por Nível"
]

# Função de avaliação
def avaliar_rubrica(r):
    aval = {
        "nome": r.get("nome", ""),
        "versao": r.get("versao", ""),
        "timestamp": datetime.utcnow()
    }
    aval[criterios[0]] = 4 if r.get("descricao") and len(r["descricao"].split()) > 5 else 2
    aval[criterios[1]] = 4 if any(len(d.get("niveis", [])) >= 3 for d in r.get("dimensoes", [])) else 2
    aval[criterios[2]] = 4 if sum(1 for d in r.get("dimensoes", []) if len(d.get("descricao", "").split()) > 5) >= 1 else 2
    aval[criterios[3]] = 4 if sum(1 for d in r.get("dimensoes", []) for n in d.get("niveis", []) if n.get("exemplo") or n.get("exemplos")) > 0 else 1
    aval["Nota Final (média)"] = round(sum(aval[c] for c in criterios) / len(criterios), 2)
    return aval

# Gerar avaliações
avaliacoes = [avaliar_rubrica(r) for r in rubricas]

# Substituir avaliações anteriores e inserir novas
colecao_avaliacoes.delete_many({})
colecao_avaliacoes.insert_many(avaliacoes)

client.close()

print("✅ Avaliações inseridas na coleção 'avaliacoes_rubricas_referenciais'. Total:", len(avaliacoes))

