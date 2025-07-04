from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import docx2txt
from pymongo import MongoClient

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

# Caminho da pasta
pasta = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")000"))

# Função para limpar o texto
def limpar_texto(texto):
    return ' '.join(texto.split())

# Varredura dos arquivos DOC
for arquivo in os.listdir(pasta):
    if arquivo.endswith(".doc"):
        caminho_arquivo = os.path.join(pasta, arquivo)
        print(f"📂 Lendo {arquivo}...")

        # Extrair texto do arquivo
        texto_extraido = docx2txt.process(caminho_arquivo)
        texto_limpo = limpar_texto(texto_extraido)

        # Aqui vamos decidir para onde vai: escola, estudante ou teste
        if "School_compendium" in arquivo:
            colecao = db["pisa_2000_escolas"]
            tipo = "Escola"
        elif "Student_compendium" in arquivo:
            colecao = db["pisa_2000_estudantes"]
            tipo = "Estudante"
        elif "Test_item_compendium" in arquivo:
            colecao = db["pisa_2000_itens"]
            tipo = "Item"
        else:
            print(f"⚠️ Arquivo {arquivo} não reconhecido.")
            continue

        # Inserir no MongoDB (estrutura inicial básica)
        documento = {
            "arquivo_origem": arquivo,
            "ano": 2000,
            "tipo_documento": tipo,
            "conteudo_textual": texto_limpo
        }
        colecao.insert_one(documento)
        print(f"✅ Inserido no MongoDB na coleção '{colecao.name}'.")

print("🏁 Finalizado!")
client.close()

