import os

# Base do caminho: até os.path.join(~, "S")INAPSE2.0/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DADOS_PATH = os.path.join(BASE_DIR, "PISA", "dados_processados", "respostas")

JSON_PATH = os.path.join(DADOS_PATH, "questoes_pisa_sinapse.json")
FAISS_INDEX_PATH = os.path.join(DADOS_PATH, "faiss_index_pisa_sinapse.index")
FAISS_METADATA_PATH = os.path.join(DADOS_PATH, "faiss_metadata_pisa_sinapse.json")

print("📂 BASE_DIR:", BASE_DIR)
print("📂 DADOS_PATH:", DADOS_PATH)
print("📄 JSON_PATH:", JSON_PATH)
print("📄 FAISS_INDEX_PATH:", FAISS_INDEX_PATH)
print("📄 FAISS_METADATA_PATH:", FAISS_METADATA_PATH)

# Verificação extra: os arquivos existem?
print("\n🔍 Verificações de existência:")
print("JSON existe?", os.path.exists(JSON_PATH))
print("FAISS index existe?", os.path.exists(FAISS_INDEX_PATH))
print("FAISS metadata existe?", os.path.exists(FAISS_METADATA_PATH))

