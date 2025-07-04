import streamlit as st
import streamlit.components.v1 as components

# Função para ativar leitura por voz no navegador
def ler_texto_browser(texto):
    js_code = f"""
    <script>
        const texto = `{texto}`;
        const utterance = new SpeechSynthesisUtterance(texto);
        utterance.lang = 'pt-BR';
        speechSynthesis.speak(utterance);
    </script>
    """
    components.html(js_code, height=0)

# Interface do usuário
st.title("🗣️ Leitor de Texto no Navegador")

if st.button("🔊 Ler Mensagem"):
    ler_texto_browser("Olá! Seja muito bem-vindo ao ambiente inclusivo da plataforma SINAPSE.")
