import streamlit as st

# Ícone redondo com HTML
st.markdown("""
<h3 style="display: flex; align-items: center;">
    <span style="
        background: #e74c3c;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        color: white;
        margin-right: 10px;
        font-size: 14px;
    ">!</span>
    Relatório de Saúde (PISA 2022)
</h3>
""", unsafe_allow_html=True)

# Ícone baixado
st.image("https://cdn-icons-png.flaticon.com/512/1828/1828640.png", width=28)
st.write("**Escalas de Proficiência**")
