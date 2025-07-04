# Funções para rubricas avaliativas
# utilos.path.join(s, "f")uncoes_rubricas.py

import streamlit as st

def mostrar_diagnostico_pisa_2000():
    st.header("🔎 Diagnóstico Atual - PISA 2000")
    st.markdown("""
Os dados analisados indicam que os estudantes brasileiros participantes do PISA 2000 apresentam desempenho majoritariamente nos níveis **Compreender** e **Aplicar** da Taxonomia de Bloom.
""")

def mostrar_estrategias_pisa_2000():
    st.header("🚀 Estratégias Pedagógicas Recomendadas")
    st.markdown("""
Para elevar o desempenho dos estudantes brasileiros aos níveis **Analisar** e **Criar**, sugerimos a adoção das seguintes práticas:

- **Problematização ativa**: Utilizar questões abertas que desafiem o pensamento crítico.
- **Estudos de Caso**: Trazer problemas reais e interdisciplinares para a sala de aula.
- **Aprendizagem Baseada em Projetos (PBL)**: Incentivar o desenvolvimento de soluções práticas e inovadoras.
- **Gamificação com desafios cognitivos**: Usar jogos que envolvam análise crítica e construção de hipóteses.
- **Metodologia STEAM**: Integrar ciências, tecnologia, engenharia, artes e matemática em projetos práticos.
""")

def mostrar_casos_sucesso_pisa_2000():
    st.header("🌎 Casos de Sucesso Inspiradores")
    st.markdown("""
Exemplos de boas práticas educacionais que promoveram melhorias significativas no desempenho cognitivo de estudantes:

- **Projeto Âncora (Brasil - Cotia-SP)**: Educação baseada em projetos e trilhas autônomas de aprendizagem.
- **Escolas do SESI-SP (Brasil)**: Uso intensivo de metodologias ativas e aprendizagem baseada em projetos.
- **Sistema Educacional da Finlândia**: Ênfase no pensamento crítico, investigação e projetos interdisciplinares.
- **Província de Ontário (Canadá)**: Aprendizagem colaborativa e resolução de problemas reais como estratégia de ensino.
- **Sistema de Singapura**: Treinamento sistemático em análise e raciocínio crítico em matemática.
""")

def mostrar_observacao_final():
    st.info("As rubricas aqui apresentadas são específicas para a edição PISA 2000 e serão expandidas conforme novas edições forem organizadas.")

