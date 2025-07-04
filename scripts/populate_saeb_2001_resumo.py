from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
import statistics

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]

# Coleções relevantes
alunos = db["alunos_2001_matematica_8aserie"]
escolas = db["escolas_2001"]
microregioes = db["escolas_1999_microregiao"]
resumo = db["saeb_2001_resumo"]

# Limpa coleção anterior
resumo.drop()

# 1. Indexa escolas por MASCARA
escolas_dict = {e["MASCARA"]: e for e in escolas.find() if "MASCARA" in e}

# 2. Indexa microregiões por MASCARA
micro_dict = {m["MASCARA"]: m for m in microregioes.find() if "MASCARA" in m}

# 3. Agrupar dados
brasil_profic = []
minas_profic = []
triangulo_profic = []

for aluno in alunos.find():
    try:
        profic_str = aluno.get("PROFIC", "").split()[0]
        profic = float(profic_str)
    except:
        continue

    mascara = aluno.get("MASCARA")
    escola = escolas_dict.get(mascara)
    if not escola:
        continue

    uf = escola.get("uf") or escola.get("UF") or escola.get("MASCARA")[:2]
    brasil_profic.append(profic)

    if uf == "31":  # Minas Gerais
        minas_profic.append(profic)

    micro = micro_dict.get(mascara)
    if micro and "microrregiao" in micro:
        if "Triângulo Mineiro" in micro["microrregiao"]:
            triangulo_profic.append(profic)

# 4. Inserir no MongoDB
resumo.insert_many([
    {
        "regiao": "Brasil",
        "estado": None,
        "matematica_media": round(statistics.mean(brasil_profic), 2) if brasil_profic else None,
        "leitura_media": None,
        "ciencias_media": None
    },
    {
        "regiao": "Minas Gerais",
        "estado": "MG",
        "matematica_media": round(statistics.mean(minas_profic), 2) if minas_profic else None,
        "leitura_media": None,
        "ciencias_media": None
    },
    {
        "regiao": "Triângulo Mineiro",
        "estado": "MG",
        "matematica_media": round(statistics.mean(triangulo_profic), 2) if triangulo_profic else None,
        "leitura_media": None,
        "ciencias_media": None
    }
])

client.close()
print("✅ Coleção 'saeb_2001_resumo' populada com dados reais.")

