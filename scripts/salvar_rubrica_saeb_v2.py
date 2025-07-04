# scripts/salvar_rubrica_saeb_v2.py

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import json
import os

rubrica_saeb = {
    "nome": "SAEB",
    "versao": "v2.0",
    "tipo": "Avaliação Nacional",
    "descricao": "Avaliação do SAEB adaptada para a Rubrica SINAPSE, unificando Língua Portuguesa e Matemática em uma única estrutura avaliativa de 4 níveis.",
    "origem": "INEP/MEC, adaptada pela equipe do projeto SINAPSE 2.0",
    "dimensao": "Língua Portuguesa e Matemática (9º ano)",
    "niveis": [
        {
            "nivel": 1,
            "titulo": "Iniciante",
            "descricao": "Dificuldade em compreender textos simples ou resolver problemas básicos. Demonstra domínio limitado de leitura e cálculo elementar.",
            "exemplos": [
                "Lê um pequeno trecho, mas não compreende o sentido global.",
                "Erra operações como adição ou subtração simples.",
                "Confunde o significado de gráficos simples, como de barras."
            ]
        },
        {
            "nivel": 2,
            "titulo": "Básico",
            "descricao": "Compreende ideias principais de textos simples e resolve operações matemáticas básicas em contextos conhecidos.",
            "exemplos": [
                "Identifica o tema principal de um texto narrativo.",
                "Resolve expressões com adição, subtração e multiplicação.",
                "Interpreta gráficos de colunas com apoio de legenda."
            ]
        },
        {
            "nivel": 3,
            "titulo": "Proficiente",
            "descricao": "Compreende e interpreta diferentes tipos de textos. Resolve problemas matemáticos contextualizados com múltiplas etapas.",
            "exemplos": [
                "Faz inferências em textos de opinião ou jornalísticos.",
                "Resolve problemas envolvendo unidades de medida.",
                "Interpreta tabelas e porcentagens em situações reais."
            ]
        },
        {
            "nivel": 4,
            "titulo": "Avançado",
            "descricao": "Analisa criticamente textos e resolve problemas complexos com abstração matemática. Utiliza estratégias autônomas de leitura e cálculo.",
            "exemplos": [
                "Compara argumentos em textos de gêneros diversos.",
                "Aplica propriedades da geometria e álgebra simples.",
                "Resolve problemas com proporção, escalas e probabilidade."
            ]
        }
    ],
    "timestamp": datetime.utcnow().isoformat()
}

# Função para converter ObjectId ao salvar JSON
def converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Não serializável: {type(obj)}")

# Inserção no MongoDB com autenticação
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["rubricas_referenciais"]

# Remove versão anterior (opcional, pode comentar se não quiser sobrescrever)
colecao.delete_many({"nome": "SAEB", "versao": "v2.0"})

# Inserir e recuperar _id
inserido = colecao.insert_one(rubrica_saeb)
print(f"✅ Inserido no MongoDB com _id: {inserido.inserted_id}")

# Salvar como JSON
os.makedirs("dados_processados/bncc", exist_ok=True)
CAMINHO = "dados_processados/bncc/rubrica_saeb_v2.json"

with open(CAMINHO, "w", encoding="utf-8") as f:
    json.dump(rubrica_saeb, f, ensure_ascii=False, indent=2, default=converter)

print(f"✅ JSON salvo em: {CAMINHO}")

# Encerrar conexão
client.close()

