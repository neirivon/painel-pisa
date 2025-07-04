from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# apagar_colecao_inutil.py
from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]

# Acessar banco
db = client["pisa_ocde"]

# Apagar coleção antiga
nome_colecao = "pisa_2018_versao2"
if nome_colecao in db.list_collection_names():
    db.drop_collection(nome_colecao)
    print(f"🗑️ Coleção '{nome_colecao}' apagada com sucesso!")
else:
    print(f"⚠️ Coleção '{nome_colecao}' não encontrada, nada a apagar.")

client.close()

# listar_banco_pisa_ocde.py
from pymongo import MongoClient

# Conectar
client = conectar_mongo(nome_banco="saeb")[1]

# Acessar banco
db = client["pisa_ocde"]

# Função auxiliar para identificar o tipo
def identificar_tipo(nome):
    nome = nome.lower()
    if "aluno" in nome or "stu" in nome:
        return "🎒 Alunos"
    elif "escola" in nome or "sch" in nome:
        return "🏫 Escolas"
    elif "prof" in nome or "tch" in nome:
        return "👩‍🏫 Professores"
    elif "cog" in nome or "cognitivo" in nome:
        return "🧠 Cognitivo"
    elif "relatorio" in nome or "inep" in nome:
        return "🇧🇷 Relatórios INEP"
    elif "temp" in nome or "paises" in nome:
        return "🌍 Países Temporários"
    elif "raw" in nome or "texto" in nome:
        return "📝 Texto Bruto"
    else:
        return "📄 Outros"

print("\n📚 Banco de Dados 'pisa_ocde':")
print("===============================")

for colecao in sorted(db.list_collection_names()):
    tipo = identificar_tipo(colecao)
    quantidade = db[colecao].count_documents({})
    print(f"📌 {colecao} ({tipo}) ➡️ {quantidade} documentos")

client.close()

