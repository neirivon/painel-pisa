from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_regioes_saeb_2021_9ano.py

from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
collection = db["saeb_2021_municipios_9ano"]

# Mapeamento: Nome do município → Região, Mesorregião, Microrregião
informacoes_geograficas = {
    "Cruz": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Acaraú"},
    "Pires Ferreira": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Ipu"},
    "Ararendá": {"REGIAO": "Nordeste", "MESORREGIAO": "Sertões Cearenses", "MICRORREGIAO": "Sertão de Crateús"},
    "Gabriel Monteiro": {"REGIAO": "Sudeste", "MESORREGIAO": "Araçatuba", "MICRORREGIAO": "Birigui"},
    "Moirorá": {"REGIAO": "Centro-Oeste", "MESORREGIAO": "Centro Goiano", "MICRORREGIAO": "Anicuns"},
    "Teotônio Vilela": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Alagoano", "MICRORREGIAO": "União dos Palmares"},
    "Santana do Mundaú": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Alagoano", "MICRORREGIAO": "União dos Palmares"},
    "Uruoca": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Coreaú"},
    "Jijoca de Jericoacoara": {"REGIAO": "Nordeste", "MESORREGIAO": "Noroeste Cearense", "MICRORREGIAO": "Camocim"},
    "Floreal": {"REGIAO": "Sudeste", "MESORREGIAO": "São José do Rio Preto", "MICRORREGIAO": "Auriflama"},
    
    # Bottom municípios
    "Paiva": {"REGIAO": "Sudeste", "MESORREGIAO": "Zona da Mata", "MICRORREGIAO": "Barbacena"},
    "Chiador": {"REGIAO": "Sudeste", "MESORREGIAO": "Zona da Mata", "MICRORREGIAO": "Juiz de Fora"},
    "Afonso Cunha": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Chapadinha"},
    "Milagres do Maranhão": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Chapadinha"},
    "Mirador": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Chapadinha"},
    "Peritoró": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Caxias"},
    "São Vicente Ferrer": {"REGIAO": "Nordeste", "MESORREGIAO": "Norte Maranhense", "MICRORREGIAO": "Viana"},
    "Caldeirão Grande": {"REGIAO": "Nordeste", "MESORREGIAO": "Centro Norte Baiano", "MICRORREGIAO": "Jacobina"},
    "Jacuzinho": {"REGIAO": "Sul", "MESORREGIAO": "Centro Ocidental Rio-Grandense", "MICRORREGIAO": "Cruz Alta"},
    "Urbano Santos": {"REGIAO": "Nordeste", "MESORREGIAO": "Leste Maranhense", "MICRORREGIAO": "Chapadinha"},
}

# Atualizar os documentos com as novas informações
for municipio, info in informacoes_geograficas.items():
    resultado = collection.update_many(
        {"NO_MUNICIPIO": municipio},
        {"$set": info}
    )
    print(f"✅ {municipio}: {resultado.modified_count} documento(s) atualizado(s).")

client.close()
print("🏁 Atualização concluída.")

