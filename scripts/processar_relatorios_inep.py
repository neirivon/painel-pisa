import os
import json
from pymongo import MongoClient

# Configurações
CAMINHO_ARQUIVOS = '/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")neos.path.join(p, "e")xtraido'
MONGO_URI = 'mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin'
BANCO = 'pisa'
COLECAO = 'pisa_inep_relatorios'

def detectar_topicos(texto):
    TOPICOS = ['matemática', 'leitura', 'ciências', 'equidade', 'inclusão', 'desempenho', 'escolas']
    encontrados = []
    texto_lower = texto.lower()
    for topico in TOPICOS:
        if topico in texto_lower:
            encontrados.append(topico.capitalize())
    return encontrados

def processar_relatorios():
    with MongoClient(MONGO_URI) as client:
        db = client[BANCO]
        colecao = db[COLECAO]

        documentos = colecao.find({})
        for doc in documentos:
            ano = doc['ano']
            arquivo_nome = doc['arquivo']
            caminho_arquivo = os.path.join(CAMINHO_ARQUIVOS, arquivo_nome)

            if not os.path.exists(caminho_arquivo):
                print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
                continue

            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            trecho_inicial = conteudo.strip()[:500]
            topicos_detectados = detectar_topicos(conteudo)

            colecao.update_one(
                {'_id': doc['_id']},
                {'$set': {
                    'trecho_inicial': trecho_inicial,
                    'topicos_detectados': topicos_detectados
                }}
            )
            print(f"✅ Atualizado relatório {ano}: {arquivo_nome}")

    print("🏁 Processamento concluído e conexão MongoDB fechada automaticamente.")

if __name__ == "__main__":
    processar_relatorios()

