# comparar_campos_colecoes.py
# Caminho completo respeitando a estrutura do projeto
import sys
import os

# Garante que o Python encontre o módulo painel_pisa.utils.conexao_mongo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "painel_pisa")))

from utils.conexao_mongo import conectar_mongo

# Conecta ao MongoDB via função reutilizável
db, client = conectar_mongo()

# Coleções a comparar
colecao_a = "pisa2000_medias_oficiais"
colecao_b = "pisa_2000_medias"

def obter_campos(colecao_nome):
    colecao = db[colecao_nome]
    exemplo = colecao.find_one()
    if exemplo:
        return set(exemplo.keys())
    return set()

campos_a = obter_campos(colecao_a)
campos_b = obter_campos(colecao_b)

print(f"\n📂 Comparando campos entre: '{colecao_a}' vs '{colecao_b}'\n")

print("✅ Campos em comum:")
print(sorted(list(campos_a & campos_b)))

print("\n🟥 Exclusivos de", colecao_a + ":")
print(sorted(list(campos_a - campos_b)))

print("\n🟦 Exclusivos de", colecao_b + ":")
print(sorted(list(campos_b - campos_a)))

# Fecha conexão explicitamente
client.close()

