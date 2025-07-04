import streamlit as st

def aplicar_estilo():
    st.markdown("""
    <style>
   os.path.join( , "*") Aumentar fonte global geral (corpo do app) */
    section.main > div {
        font-size: 24px !important;
    }

   os.path.join( , "*") Títulos */
    h1 { font-size: 48px !important; font-weight: bold; }
    h2 { font-size: 40px !important; font-weight: bold; }
    h3 { font-size: 32px !important; }

   os.path.join( , "*") Labels dos campos de entrada */
    label, .stTextInput label, .stTextArea label {
        font-size: 24px !important;
    }

   os.path.join( , "*") Markdown e textos comuns */
    .stMarkdown p, .stText, .stCaption, .stSubheader {
        font-size: 24px !important;
    }

   os.path.join( , "*") Botões */
    button[kind="primary"] {
        font-size: 22px !important;
    }

   os.path.join( , "*") Responsividade mínima */
    @media (max-width: 768px) {
        section.main > div {
            font-size: 20px !important;
        }
        h1 { font-size: 36px !important; }
        h2 { font-size: 30px !important; }
        h3 { font-size: 26px !important; }
    }
    os.path.join(<, "s")tyle>
    """, unsafe_allow_html=True)
