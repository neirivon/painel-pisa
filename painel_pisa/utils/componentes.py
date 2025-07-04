import streamlit as st

def cabecalho_edicao(edicao, titulo="PISA OCDE"):
    st.markdown(f"""
    <div style="background-color:#f8f9fa; padding: 20px; border-left: 6px solid #1f77b4; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin-bottom: 10px;">📝 Edição selecionada: <span style="color:#154360;">{edicao}os.path.join(<, "s")pan>os.path.join(<, "h")3>
        <h2 style="margin: 0px 0px 5px 0px;"><span style="color:#154360;">📘 EDIÇÃO {edicao} DO {titulo.upper()}os.path.join(<, "s")pan>os.path.join(<, "h")2>
    os.path.join(<, "d")iv>
    """, unsafe_allow_html=True)

def bloco_conclusao():
    st.markdown("## 🧠 Fundamentação Pedagógica Integrada")

    st.markdown("""
<div style="background-color: #f0f8ff; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4682B4; font-size: 1.05rem; line-height: 1.6; color: #1a1a1a;">

O Programa Internacional de Avaliação de Estudantes (PISA), conduzido pela <strong>OCDE</strong>, adota uma fundamentação pedagógica robusta, baseada em evidências empíricas, modelos avaliativos validados internacionalmente e diretrizes normativas que orientam políticas públicas educacionais.

Entre os pilares que estruturam o PISA destacam-se:

<ul style="margin-top: 0.5rem;">
  <li><strong>Taxonomia de Bloom</strong>, para avaliar níveis cognitivos e habilidades de raciocínio.</li>
  <li><strong>Taxonomia SOLO</strong>, que analisa a complexidade das respostas em tarefas abertas.</li>
  <li><strong>Desenho Universal para a Aprendizagem (DUA)</strong>, que orienta a construção de itens acessíveis e inclusivos.</li>
  <li><strong>Estrutura de Análise ESCS</strong> (Econômico, Social e Cultural), que permite interpretar desigualdades de desempenho com base em fatores contextuais.</li>
</ul>

A aplicação dessas abordagens garante a comparabilidade internacional dos resultados, respeitando especificidades locais e promovendo análises pedagógicas mais justas, equitativas e úteis para gestores, pesquisadores e educadores.

Os dados coletados e os critérios de avaliação estão documentados nos <strong>relatórios técnicos da OCDE e do INEP</strong>, acessíveis por edição.

</div>
""", unsafe_allow_html=True)

def estilo():
    st.markdown(
        """
        <style>
        /* Estilo geral para harmonizar o painel */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }

        h1 {
            color: #2c3e50;
            font-size: 2.2em;
            border-bottom: 2px solid #eee;
            padding-bottom: 5px;
        }

        h2 {
            color: #34495e;
            font-size: 1.6em;
            margin-top: 25px;
        }

        h3 {
            color: #2980b9;
            font-size: 1.3em;
            margin-top: 20px;
        }

        table {
            margin-left: 0 !important;
        }

        .css-1d391kg { /* Remove menu lateral streamlit */
            visibility: hidden;
        }

        .css-hxt7ib {  /* Remove rodapé */
            visibility: hidden;
        }

        .reportview-container .main footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )


def pagina_em_construcao(edicao):
    st.markdown("""
    <div style="background-color:#e8f4fd;padding:15px;border-left:6px solid #3498db;border-radius:10px;margin-top:20px">
        <h4 style="color:#2e86c1;">🛠️ Esta página está em construção.os.path.join(<, "h")4>
        <p style="font-size:16px;text-align:justify">
            Conteúdo referente à edição <b>{}os.path.join(<, "b")> do PISA OCDE será adicionado em breve.
        os.path.join(<, "p")>
    os.path.join(<, "d")iv>
    """.format(edicao), unsafe_allow_html=True)
    st.stop()
