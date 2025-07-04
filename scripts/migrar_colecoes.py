from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# migrar_colecoes.py
from pymongo import MongoClient

# Conexão original
client = conectar_mongo(nome_banco="saeb")[1]
db_original = client["pisa"]

# Novos bancos organizados
db_ocde = client["pisa_ocde"]
db_inep = client["pisa_inep"]

# Mapear coleções para destino correto
migracoes = {
    # OCDE - anos conhecidos
    "pisa_ocde_2000": (db_ocde, "pisa_2000"),
    "pisa_ocde_2018": (db_ocde, "pisa_2018"),
    "pisa_ocde_2018_completo": (db_ocde, "pisa_2018_completo"),
    "pisa_ocde_2018_paises_temp": (db_ocde, "pisa_2018_paises_temp"),
    # Dados pfd (partner for development) que são da OCDE
    "pisa_pfd_alunos": (db_ocde, "pfd_alunos"),
    "pisa_pfd_cognitivo": (db_ocde, "pfd_cognitivo"),
    "pisa_pfd_escolas": (db_ocde, "pfd_escolas"),
    "pisa_pfd_professores": (db_ocde, "pfd_professores"),
    "pisa_pfd_questionario": (db_ocde, "pfd_questionario"),
    "pisa_pfd_tempos": (db_ocde, "pfd_tempos"),
    # Dados cy1mdai (padrão OCDE de estudanteos.path.join(s, "p")rofessoreos.path.join(s, "e")scolas)
    "cy1mdai_sch_qqq": (db_ocde, "cy1mdai_escolas"),
    "cy1mdai_stu_qqq": (db_ocde, "cy1mdai_estudantes"),
    "cy1mdai_stu_cog": (db_ocde, "cy1mdai_cognitivo"),
    "cy1mdai_tch_qqq": (db_ocde, "cy1mdai_professores"),
    # Dados brutos de relatorios do INEP
    "pisa_inep_relatorios": (db_inep, "relatorios"),
    # Dados que precisam ser organizados melhor ainda (raw)
    "pisa_2000": (db_ocde, "pisa_2000_raw"),
    "pisa_2000_tabelas_textuais": (db_ocde, "pisa_2000_texto"),
    "pisa_2003": (db_ocde, "pisa_2003"),
    "pisa_2009": (db_ocde, "pisa_2009"),
    "pisa_2012": (db_ocde, "pisa_2012"),
    "pisa_2015": (db_ocde, "pisa_2015"),
    "pisa_2018": (db_ocde, "pisa_2018_versao2"),
    "pisa_2022": (db_ocde, "pisa_2022"),
}

# Executar migração
def migrar():
    for colecao_origem, (db_destino, colecao_destino) in migracoes.items():
        if colecao_origem not in db_original.list_collection_names():
            print(f"❌ Coleção {colecao_origem} não encontrada.")
            continue

        documentos = list(db_original[colecao_origem].find())

        if documentos:
            db_destino[colecao_destino].insert_many(documentos)
            print(f"✅ Migrado {len(documentos)} documentos de {colecao_origem} para {db_destino.name}.{colecao_destino}")
        else:
            print(f"⚠️ Coleção {colecao_origem} está vazia, não migrada.")

    print("\n✅ Migração concluída!")
    client.close()

if __name__ == "__main__":
    migrar()

