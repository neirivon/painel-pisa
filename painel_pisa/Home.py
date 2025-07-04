# painel_pisa/Home.py

import streamlit as st  # Sempre primeiro import do Streamlit
import os
import json
from PIL import Image, ImageDraw
from io import BytesIO
import base64

from utils.config import CONFIG
from utils.estilo_global import aplicar_estilo
from utils.componentes import bloco_conclusao
from utils.paths import LOGOS_DIR, IMAGENS_DIR  # NOVO

# Deve ser o primeiro comando do Streamlit
st.set_page_config(
    page_title="Painel Educacional – PISA OCDE INEP",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

#aplicar_estilo()

st.sidebar.info(
    f"""
🔧 Modo de execução: {CONFIG['MODO'].upper()}

{'📦 Usando MongoDB + FAISS (Local)' if CONFIG['MODO'] == 'local' else '☁️ Usando arquivos CSV/JSON (Cloud)'}
    """
)

def imagem_redonda_base64(caminho_img):
    img = Image.open(caminho_img).convert("RGBA").resize((150, 150))
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    img.putalpha(mask)
    output = BytesIO()
    img.save(output, format="PNG")
    return base64.b64encode(output.getvalue()).decode()

def imagem_base64(caminho_img):
    img = Image.open(caminho_img).convert("RGBA")
    output = BytesIO()
    img.save(output, format="PNG")
    return base64.b64encode(output.getvalue()).decode()

# ✅ Usa o novo path centralizado
logo_path = os.path.join(LOGOS_DIR, "IFTM_360.png")
img_logo_sidebar = imagem_base64(logo_path)

st.markdown(f"""
<style>
[data-testid="stSidebarNav"] {{
    background-image: url("data:image/png;base64,{img_logo_sidebar}");
    background-repeat: no-repeat;
    background-position: center 20px;
    background-size: 220px;
    padding-top: 230px;
    transition: background-size 0.3s ease;
}}
[data-testid="stSidebarNav"]:hover {{
    background-size: 240px;
}}
.integrante-container {{
    text-align: center;
}}
.foto-hover {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    object-fit: cover;
}}
.foto-hover:hover {{
    transform: scale(1.1);
}}
.caption-hover {{
    margin-top: 8px;
    font-size: 14px;
    color: #555;
    transition: transform 0.3s ease, color 0.3s ease;
}}
.caption-hover:hover {{
    transform: scale(1.1);
    color: #0D47A1;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🎓 Painel Educacional – PISA OCDE INEP")
st.markdown("📊 *PISA OCDE: Avaliação Global, Análise Local*")

st.subheader("👥 Equipe do Projeto")

integrantes = [
    ("neirivon.png", "Neirivon Elias Cardoso"),
    ("eduardo.png", "Eduardo Denuncio"),
    ("janaina.png", "Janaina Pereira"),
    ("orlando.png", "Orlando Antonio de Melo")
]

col1, col2, col3, col4 = st.columns(4)
for col, (foto, nome) in zip([col1, col2, col3, col4], integrantes):
    img = imagem_redonda_base64(os.path.join(IMAGENS_DIR, foto))
    col.markdown(f'''
    <div class="integrante-container">
        <img src="data:image/png;base64,{img}" class="foto-hover"/>
        <div class="caption-hover">{nome}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

st.subheader("🎓 Orientação Acadêmica")

img_prof = imagem_redonda_base64(os.path.join(IMAGENS_DIR, "bruno.png"))
st.markdown(f'''
<div style="text-align: center;">
    <img src="data:image/png;base64,{img_prof}" class="foto-hover" width="120"/>
    <div class="caption-hover">Prof. Dr. Bruno Pereira Garcês<br><small>Orientador e Professor da disciplina</small></div>
</div>
''', unsafe_allow_html=True)

st.subheader("🎯 Objeto do Estudo")

st.markdown("---")

st.markdown("""
<div style="background-color: #f0f8ff; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4682B4; font-size: 1.05rem; line-height: 1.6; color: #1a1a1a;">

Este painel interativo apresenta uma análise crítica e contextualizada dos dados do <strong>Programa Internacional de Avaliação de Estudantes (PISA)</strong>, conduzido pela <strong>OCDE</strong> desde o ano 2000. O foco está nas competências de <strong>Leitura, Matemática e Ciências</strong>, com o objetivo de compreender e comparar o desempenho educacional entre países.

As análises consideram os <strong>relatórios oficiais da OCDE e do INEP</strong>, cobrindo as seguintes edições do PISA:

<ul style="margin-top: 0.5rem;">
  <li><strong>PISA OCDE</strong>: 2000, 2003, 2006, 2009, 2012, 2015, 2018 e 2022</li>
</ul>

Todos os documentos são armazenados por edição em banco de dados <strong>MongoDB</strong> e processados com apoio de <strong>Inteligência Artificial</strong>, utilizando modelos como o <strong>BERT</strong> para inferência textual.

<p><strong>Validação pedagógica e científica:</strong><br>
As classificações geradas automaticamente são validadas por <strong>especialistas humanos</strong> em <em>Taxonomia de Bloom</em>, <em>metodologias ativas</em> e <em>neuropsicopedagogia</em>.</p>

Todos os resultados são apresentados em <strong>painéis educacionais interativos</strong>, desenvolvidos com <strong>Streamlit</strong>.

</div>
""", unsafe_allow_html=True)

st.markdown("---")

bloco_conclusao()
st.success("✅ Utilize o menu lateral para navegar pelos dashboards e análises.")
st.caption("Seminário Avaliações Externas 2025 | EQUIPE DO PROJETO | Dados extraídos do PISA OCDE e INEP.")

