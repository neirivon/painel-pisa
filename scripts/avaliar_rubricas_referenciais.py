from pymongo import MongoClient
import json

# Conectando ao MongoDB dockerizado com autenticação
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["rubricas_referenciais"]

# Carregar todas as rubricas da coleção
rubricas = list(colecao.find())

# Critérios da Avaliação de Rubricas
criterios = [
    "Clareza Conceitual",
    "Estrutura Progressiva (níveis)",
    "Aplicabilidade Pedagógica",
    "Exemplos Práticos por Nível"
]

def avaliar_rubrica(rubrica):
    pontuacao = {
        "nome": rubrica.get("nome", ""),
        "versao": rubrica.get("versao", "")
    }

    pontuacao[criterios[0]] = 4 if rubrica.get("descricao") and len(rubrica["descricao"].split()) > 5 else 2

    possui_niveis = any(len(d.get("niveis", [])) >= 3 for d in rubrica.get("dimensoes", []))
    pontuacao[criterios[1]] = 4 if possui_niveis else 2

    aplicabilidade = sum(1 for d in rubrica.get("dimensoes", []) if len(d.get("descricao", "").split()) > 5)
    pontuacao[criterios[2]] = 4 if aplicabilidade >= 1 else 2

    tem_exemplo = sum(1 for d in rubrica.get("dimensoes", []) for n in d.get("niveis", []) if n.get("exemplo") or n.get("exemplos"))
    pontuacao[criterios[3]] = 4 if tem_exemplo > 0 else 1

    pontuacao["Nota Final (média)"] = round(sum(pontuacao[c] for c in criterios) / len(criterios), 2)

    return pontuacao

# Avaliar todas as rubricas
avaliacoes = [avaliar_rubrica(r) for r in rubricas]

# Salvar em JSON
CAMINHO_SAIDA = "dados_processados/rubricas/avaliacoes_rubricas_referenciais.json"
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(avaliacoes, f, ensure_ascii=False, indent=2)

client.close()

print(f"✅ Avaliação concluída e salva em {CAMINHO_SAIDA}")

