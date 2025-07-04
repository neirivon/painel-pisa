import os
import re
from pymongo import MongoClient
import pandas as pd
import textract

# === CONFIGURAÇÕES ===
DATA_DIR = '/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "D")OC'
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "pisa_2000_medias"
CSV_OUTPUT = '/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "s")aida_pisa_2000_medias.csv'

# === FUNÇÕES AUXILIARES ===

def extrair_texto_doc(file_path):
    """Extrai texto bruto de um .doc"""
    print(f"📚 Extraindo texto de: {file_path}")
    text = textract.process(file_path).decode('utf-8')
    return text

def extrair_medias(texto, area_nome):
    """Extrai médias por país de um texto bruto"""
    linhas = texto.splitlines()
    registros = []
    
    # Regex para capturar linhas com país e média
    padrao = re.compile(r'^\s*([A-Z]{3})\s+[\d\.\s]+(?:\|\s+)?(?:[\.\d]+\s+\(\s*[\.\d]*\s*\)\s+){0,6}([\.\d]+)\s+\(\s*[\.\d]*\s*\)')

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        m = padrao.match(linha)
        if m:
            pais_codigo = m.group(1)
            media_valor = m.group(2)
            
            try:
                media = float(media_valor)
            except ValueError:
                continue
            
            registros.append({
                "pais": pais_codigo,
                "area": area_nome,
                "media": media
            })
    return registros

def organizar_por_pais(registros):
    """Organiza o resultado final por país"""
    df = pd.DataFrame(registros)
    tabela = {}
    
    for pais in df['pais'].unique():
        dados_pais = df[df['pais'] == pais]
        tabela[pais] = {
            "ano": 2000,
            "pais": pais,
            "areas": {}
        }
        for _, row in dados_pais.iterrows():
            tabela[pais]["areas"][row['area']] = {
                "media": row['media']
            }
    return list(tabela.values()), df

def inserir_mongodb(documentos):
    """Insere documentos no MongoDB e cria índices"""
    print("🚀 Conectando ao MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    collection.delete_many({})  # Limpa a coleção
    print(f"📥 Inserindo {len(documentos)} documentos...")
    collection.insert_many(documentos)
    
    print("🔧 Criando índices...")
    collection.create_index([("pais", 1)])
    collection.create_index([("ano", 1)])
    
    client.close()  # ✅ FECHA o MongoClient corretamente
    
    print("✅ Inserção e indexação concluídas.")
    
def salvar_csv(df, output_path):
    """Salva os dados em CSV organizado"""
    print(f"💾 Salvando CSV em: {output_path}")
    
    # Remove duplicados caso existam (pais, area)
    df = df.drop_duplicates(subset=["pais", "area"])
    
    # Usa pivot_table para maior robustez
    df_pivot = df.pivot_table(index="pais", columns="area", values="media", aggfunc="first").reset_index()
    
    # Salva o CSV
    df_pivot.to_csv(output_path, index=False)
    print("✅ CSV salvo com sucesso.")

# === MAIN ===

if __name__ == "__main__":
    registros = []
    
    arquivos = {
        'matematica': 'Student_compendium_(mathematics).doc',
        'leitura': 'Student_compendium_(reading).doc',
        'ciencias': 'Student_compendium_(science).doc'
    }
    
    for area_nome, arquivo_nome in arquivos.items():
        caminho = os.path.join(DATA_DIR, arquivo_nome)
        texto = extrair_texto_doc(caminho)
        registros.extend(extrair_medias(texto, area_nome))
    
    documentos, df = organizar_por_pais(registros)
    inserir_mongodb(documentos)
    salvar_csv(df, CSV_OUTPUT)

