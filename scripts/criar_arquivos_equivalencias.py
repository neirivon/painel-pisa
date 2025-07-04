import os

# Criar conteúdo do CSV de equivalência de país
conteudo_paises = """colecao,campo_detectado,campo_equivalente
pisa_2000_cognitive_item,COUNTRY,CNT
pisa_2000_cognitive_item,CNT,CNT
pisa_ocde_2000_medias,pais,CNT
pisa_ocde_2003_alunos,CNT,CNT
pisa_2003_student,CNT,CNT
pisa_2006_cognitive,Country,CNT
pisa_2006_student,CNT,CNT
pisa_2009_student_sps,CNT,CNT
pisa_2009_student_sps,COUNTRY,CNT
pisa_2015_cy6_ms_cm2_stu_qqq2015,CNT,CNT
pisa_2022_student,CNT,CNT
pisa_2022_student_qqq,CNT,CNT
pisa_2022_teacher,CNT,CNT
pisa_2022_teacher_questionnaire,CNT,CNT
pisa_2022_country_questionnaire,CNT,CNT
"""

# Criar conteúdo do CSV de equivalência de pontuações
conteudo_pontuacoes = """colecao,campo_detectado,campo_equivalente
pisa_2000_cognitive_item,PV1MATH,PV1MATH
pisa_2000_cognitive_item,PV1READ,PV1READ
pisa_2000_cognitive_item,PV1SCIE,PV1SCIE
pisa_ocde_2000_medias,PV1MATH,PV1MATH
pisa_ocde_2000_medias,PV1READ,PV1READ
pisa_ocde_2000_medias,PV1SCIE,PV1SCIE
pisa_ocde_2003_alunos,PV1MATH,PV1MATH
pisa_ocde_2003_alunos,PV1READ,PV1READ
pisa_ocde_2003_alunos,PV1SCIE,PV1SCIE
pisa_2009_student_sps,PV1MATH,PV1MATH
pisa_2009_student_sps,PV1READ,PV1READ
pisa_2009_student_sps,PV1SCIE,PV1SCIE
pisa_2015_cy6_ms_cm2_stu_qqq2015,PV1MATH,PV1MATH
pisa_2015_cy6_ms_cm2_stu_qqq2015,PV1READ,PV1READ
pisa_2015_cy6_ms_cm2_stu_qqq2015,PV1SCIE,PV1SCIE
pisa_2022_student,PV1MATH,PV1MATH
pisa_2022_student,PV1READ,PV1READ
pisa_2022_student,PV1SCIE,PV1SCIE
pisa_2022_student_qqq,PV1MATH,PV1MATH
pisa_2022_student_qqq,PV1READ,PV1READ
pisa_2022_student_qqq,PV1SCIE,PV1SCIE
pisa_2022_teacher_questionnaire,PV1MATH,PV1MATH
pisa_2022_teacher_questionnaire,PV1READ,PV1READ
pisa_2022_teacher_questionnaire,PV1SCIE,PV1SCIE
pisa_2022_country_questionnaire,PV1MATH,PV1MATH
pisa_2022_country_questionnaire,PV1READ,PV1READ
pisa_2022_country_questionnaire,PV1SCIE,PV1SCIE
"""

# Caminhos para salvar os arquivos
path_paises = "scripts/estrutura_equivalente_pais.csv"
path_pontuacoes = "scripts/estrutura_equivalente_pontuacoes.csv"

# Criar e salvar os arquivos
try:
    with open(path_paises, "w", encoding="utf-8") as f:
        f.write(conteudo_paises)
    with open(path_pontuacoes, "w", encoding="utf-8") as f:
        f.write(conteudo_pontuacoes)
    print(f"✔️ Arquivos salvos com sucesso em:\n- {path_paises}\n- {path_pontuacoes}")
except Exception as e:
    print(f"Erro ao salvar arquivos: {e}")

