from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# limpar_paises_ocde_2018.py

from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2018"]  # Coleção que criamos anteriormente

# Lista de palavras-chave que indicam notas e não países reais
palavras_invalidas = [
    "notes", "refers", "Information", "Coverage", "statistical", "terms", "disclaimer",
    "The data", "Data for", "Annex", "OECD", "Partner"
]

# Função para checar se é país real
def eh_pais_valido(nome):
    nome_lower = nome.lower()
    return not any(palavra.lower() in nome_lower for palavra in palavras_invalidas)

# Buscar todos os documentos
documentos = list(colecao.find())

paises_validos = set()

for doc in documentos:
    for campo, valor in doc.items():
        if isinstance(valor, str) and valor.strip():
            if eh_pais_valido(valor):
                paises_validos.add(valor.strip())

# Exibir resultado
paises_validos = sorted(paises_validos)
print(f"\n✅ Número final de países válidos encontrados: {len(paises_validos)}")
print("\n📋 Lista limpa de países:")
for pais in paises_validos:
    print(f"- {pais}")

client.close()

