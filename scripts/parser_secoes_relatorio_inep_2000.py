import pymongo
import re

# Configuração do MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_ORIGINAL = "relatorios_inep_pisa"
COLLECTION_SECOES = "relatorios_inep_pisa_secoes"

# Lista de possíveis títulos de seções principais
PADROES_SECOES = [
    "RESUMO EXECUTIVO",
    "ANÁLISE GLOBAL",
    "ANÁLISE REGIONAL NORTE",
    "ANÁLISE REGIONAL NORDESTE",
    "ANÁLISE REGIONAL CENTRO-OESTE",
    "ANÁLISE REGIONAL SUDESTE",
    "ANÁLISE REGIONAL SUL",
    "COMPARATIVO URBANO X RURAL",
    "INFLUÊNCIA DO NÍVEL SOCIOECONÔMICO",
    "CONCLUSÕES",
    "CONCLUSÃO",
    "PROPOSTAS",
    "REFERÊNCIAS"
]

# Palavras-chave que indicam índiceos.path.join(s, "l")istas que devemos ignorar
PALAVRAS_IGNORAR = [
    "LISTA DE GRÁFICOS",
    "LISTA DE QUADROS",
    "LISTA DE TABELAS",
    "APRESENTAÇÃO"
]

def detectar_secao(texto):
    texto_limpo = texto.strip().upper()
    if any(palavra in texto_limpo for palavra in PALAVRAS_IGNORAR):
        return None
    for padrao in PADROES_SECOES:
        if padrao in texto_limpo:
            return padrao.title()
    return None

def organizar_por_secoes(elementos):
    secoes = []
    secao_atual = {"secao": "Introdução", "elementos": []}

    for elem in elementos:
        if elem.get("tipo") == "texto":
            texto = elem.get("conteudo", "")
            # Dividir o texto em linhas para detectar seções dentro de blocos grandes
            linhas = texto.split("\n")
            novo_texto = ""
            for linha in linhas:
                nova_secao = detectar_secao(linha)
                if nova_secao:
                    if novo_texto.strip():
                        secao_atual["elementos"].append({"tipo": "texto", "conteudo": novo_texto.strip()})
                    if secao_atual["elementos"]:
                        secoes.append(secao_atual)
                    secao_atual = {"secao": nova_secao, "elementos": []}
                    novo_texto = ""
                else:
                    novo_texto += linha + "\n"
            if novo_texto.strip():
                secao_atual["elementos"].append({"tipo": "texto", "conteudo": novo_texto.strip()})
        else:
            secao_atual["elementos"].append(elem)

    if secao_atual["elementos"]:
        secoes.append(secao_atual)

    return secoes

def processar_relatorio():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    doc = db[COLLECTION_ORIGINAL].find_one({"ano": 2000})
    if not doc:
        print("❌ Relatório INEP 2000 não encontrado.")
        return

    elementos = doc.get("elementos", [])
    secoes = organizar_por_secoes(elementos)

    novo_documento = {
        "ano": 2000,
        "tipo": "relatorio_inep_secoes",
        "titulo": doc.get("titulo", "Relatório"),
        "secoes": secoes
    }

    db[COLLECTION_SECOES].delete_many({"ano": 2000})
    db[COLLECTION_SECOES].insert_one(novo_documento)
    client.close()
    print(f"✅ Relatório INEP 2000 processado em {len(secoes)} seções e salvo no MongoDB!")

if __name__ == "__main__":
    print("🚀 Iniciando processamento do Relatório INEP 2000...")
    processar_relatorio()

