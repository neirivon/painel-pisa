from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import docx2txt
from pymongo import MongoClient

# 📁 Caminho da pasta de documentos convertidos
pasta = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "c")onvertidos"))

# 🌎 Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2000"]

# 🚀 Varre todos os arquivos .docx
for arquivo in os.listdir(pasta):
    if arquivo.endswith(".docx"):
        caminho_arquivo = os.path.join(pasta, arquivo)
        print(f"📂 Lendo {arquivo}...")
        
        # 📜 Extrair texto
        texto_extraido = docx2txt.process(caminho_arquivo)
        
        # 🧹 Limpeza simples
        texto_extraido = texto_extraido.replace("\n\n", "\n").strip()
        
        # 📥 Monta documento MongoDB
        documento = {
            "ano": 2000,
            "arquivo_origem": arquivo,
            "texto_extraido": texto_extraido
        }
        
        # ➡️ Insere no MongoDB
        colecao.insert_one(documento)

print("✅ Todos os arquivos foram processados e inseridos no MongoDB!")
client.close()

