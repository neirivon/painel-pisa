from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# criar_relatorio_inep_v2.py

from pymongo import MongoClient

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_nova = db["relatorio_inep_pisa_2000_v2"]

# Estrutura do novo documento
documento = {
    "ano": 2000,
    "titulo": "Relatório Nacional do PISA 2000 - Brasil",
    "secoes": [
        {
            "secao": "Análise dos Resultados",
            "elementos": [
                {
                    "tipo": "texto",
                    "conteudo": """Bélgica e a Islândia (nesta ordem)... [bloco 86 completo, já inserido por você acima]"""
                },
                {
                    "tipo": "texto",
                    "conteudo": """magnitude, têm sistemas educativos melhores... [bloco 87 completo]"""
                },
                {
                    "tipo": "texto",
                    "conteudo": """desculpa de que não seria de se esperar... [bloco 88 completo]"""
                }
            ]
        }
    ]
}

# Inserção no banco
colecao_nova.insert_one(documento)
client.close()

print("✅ Documento relatorio_inep_pisa_2000_v2 criado com sucesso!")

