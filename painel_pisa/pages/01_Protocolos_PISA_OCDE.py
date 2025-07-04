import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import plotly.express as px
import os
import json

# Identificação do modo
modo = st.secrets["modo"] if "modo" in st.secrets else "local"

if modo == "local":
    from pymongo import MongoClient
    client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
    db = client["pisa"]
else:
    with open("dados_cloud/protocolos_pisa_2022.json", "r", encoding="utf-8") as f:
        dados_cloud = json.load(f)

# 📌 Configurações iniciais
st.set_page_config(layout="wide", page_title="Protocolos PISA OCDE")
# ===============================
# 🎨 Estilo customizado – Aumenta fonte do texto comum
# ===============================
st.markdown("""
    <style>
        /* Aumenta o tamanho da fonte para todo o corpo do texto (exceto títulos) */
        div.block-container p {
            font-size: 1.8em !important;
            line-height: 1.6em;
        }
        /* Ajuste também para listas */
        div.block-container ul, div.block-container ol {
            font-size: 1.8em !important;
        }
        /* Tabelas também */
        .css-1d391kg th, .css-1d391kg td {
            font-size: 1.6em !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 3em;'>📘 Protocolos PISA OCDE</h1>", unsafe_allow_html=True)
st.markdown("### 🔍 Como são definidos os processos, instrumentos e critérios na avaliação internacional do PISA/OCDE?")

# 📌 Conexão com MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# ===============================
# 🔢 1. Distribuição por coleção
# ===============================
# ===============================
# 🔢 1. Distribuição com nomes legíveis
# ===============================
st.markdown("## 📊 Distribuição dos Protocolos por Coleção (com nomes legíveis)")

nomes_amigaveis = {
    "protocolo_pisa_2022_res_vol1": "📘 Volume 1 – Relatório Técnico",
    "protocolo_pisa_2022_booklet_uh": "📄 Booklet – Itens Liberados",
    "protocolo_pisa_2022_health_accounts": "📑 Relatório de Saúde",
    "protocolo_pisa_2022_quest_parent": "👨‍👩‍👧‍👦 Questionário dos Pais",
    "protocolo_pisa_2022_quest_teacher": "👩‍🏫 Questionário dos Professores",
    "protocolo_pisa_2022_quest_school_paper": "🏫 Questionário Escolar",
    "protocolo_pisa_2022_scaling": "📈 Escalas de Proficiência",
    "protocolo_pisa_2022_quest_finance": "💰 Alfabetização Financeira",
    "protocolo_pisa_2022_tech_report": "🧠 Relatório Técnico Detalhado",
    "protocolo_pisa_2022_quest_student_pc": "🖥️ Questionário do Estudante (PC)",
    "protocolo_pisa_2022_quest_student_paper": "📝 Questionário do Estudante (Papel)",
    "protocolo_pisa_2022_quest_wellbeing": "💖 Bem-Estar do Estudante",
    "protocolo_pisa_2022_policy_dialogues": "🏛️ Diálogos de Política Pública",
    "protocolo_pisa_2022_outros": "🗃️ Outros Documentos",
    "protocolo_pisa_2022_items": "🧪 Itens Aplicados",
    "protocolo_pisa_2022_quest_ict": "📱 Tecnologias e Dispositivos (ICT)",
    "protocolo_pisa_2022_privacy": "🔒 Política de Privacidade",
    "protocolo_pisa_2022_quest_school_pc": "🏫 Questionário Escolar (PC)",
    "protocolo_pisa_2022_insights": "🔍 Relatórios de Insights",
    "protocolo_pisa_2022_quest_coop_dev": "🌍 Cooperação e Desenvolvimento",
    "protocolo_pisa_2022_quest_econ_outlook_2025": "📊 Perspectivas Econômicas 2025",
    "protocolo_pisa_2022_revenue_stats_2025": "💸 Estatísticas de Receita 2025",
}

distribuicao = []
if modo == "local":
    colecoes = db.list_collection_names(filter={"name": {"$regex": "^protocolo_pisa_2022"}})
    for col in colecoes:
        count = db[col].count_documents({})
        nome_legivel = nomes_amigaveis.get(col, col)
        distribuicao.append((nome_legivel, count))
else:
    contagem = {}
    for doc in dados_cloud:
        col = doc.get("colecao", "desconhecida")
        contagem[col] = contagem.get(col, 0) + 1
    for col, count in contagem.items():
        nome_legivel = nomes_amigaveis.get(col, col)
        distribuicao.append((nome_legivel, count))

df = pd.DataFrame(distribuicao, columns=["Protocolo", "Documentos"])
df = df.sort_values(by="Documentos", ascending=False)

fig, ax = plt.subplots(figsize=(12, len(df) * 0.45))
bars = ax.barh(df["Protocolo"], df["Documentos"], color="#3498db")
bars[0].set_color("#e74c3c")  # Destaque para o maior

ax.set_xlabel("📄 Número de Documentos")
ax.set_title("📦 Documentos Armazenados por Tipo de Protocolo")
ax.invert_yaxis()
st.pyplot(fig)

st.info("""
🔍 Este gráfico mostra a **quantidade de documentos disponíveis no MongoDB** por tipo de protocolo do PISA/OCDE (edição 2022).

O **Volume 1** se destaca por ser o documento técnico central, onde estão definidos os critérios avaliativos, a TRI e as estratégias metodológicas globais.

Outros documentos complementam a avaliação com questionários, escalas, análises contextuais e políticas.
""")


# ===============================
# ☁️ 2. Nuvem de palavras TRADUZIDA
# ===============================
st.markdown("## ☁️ Nuvem de Palavras dos Protocolos (traduzida para português)")

# 🔄 Traduzindo os textos coletados dos documentos
# 🔄 Coleta e tradução dos textos para nuvem de palavras
textos = []
if modo == "local":
    for col in colecoes:
        docs = db[col].find({"conteudo": {"$exists": True}})
        for d in docs:
            conteudo = d.get("conteudo")
            if isinstance(conteudo, str) and len(conteudo.strip()) > 0:
                textos.append(conteudo.strip())
else:
    for d in dados_cloud:
        conteudo = d.get("conteudo")
        if isinstance(conteudo, str) and len(conteudo.strip()) > 0:
            textos.append(conteudo.strip())

# 🔁 Verifica se há conteúdo antes de tentar traduzir
if len(textos) == 0:
    st.warning("⚠️ Nenhum conteúdo textual encontrado para gerar a nuvem.")
else:
    texto_unificado = " ".join(textos)
    texto_unificado = re.sub(r'\s+', ' ', texto_unificado)

    if modo == "local":
        st.info("🔄 Traduzindo os principais termos para português...")

        try:
            from googletrans import Translator
            translator = Translator()
            texto_traduzido = translator.translate(texto_unificado[:5000], src='en', dest='pt').text
        except Exception as e:
            st.error(f"Erro na tradução automática: {e}")
            texto_traduzido = texto_unificado  # fallback
    else:
        st.info("☁️ Tradução automática desativada no modo cloud. Exibindo texto original (inglês ou multilíngue).")
        texto_traduzido = texto_unificado

    # 🎨 Gerar nuvem de palavras
    wordcloud = WordCloud(width=1200, height=500, background_color="white").generate(texto_traduzido)
    fig_wc, ax_wc = plt.subplots(figsize=(12, 5))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)


# ===============================
# 🧠 3. Painel Interativo: Protocolo mais denso
# ===============================
st.markdown("---")
st.markdown("<h2 style='font-size: 2em;'>🔬 Destaques dos Protocolos PISA OCDE</h2>", unsafe_allow_html=True)
st.markdown("### 💡 Explore os protocolos mais densos, impactantes e invisíveis do PISA/OCDE")

vol1_info = {
    "Título": "📘 Volume 1 – Technical Report (protocolo_pisa_2022_res_vol1)",
    "Documentos": 12,
    "Função": "Cérebro técnico do PISA 2022",
    "Conteúdos-Chave": [
        "✔️ Teoria de Resposta ao Item (TRI)",
        "✔️ Escalas de Proficiência por Área",
        "✔️ Amostragem e Estrutura de Dados",
        "✔️ Design dos Instrumentos Avaliativos",
        "✔️ Estratégias de Validação Estatística"
    ],
    "Impacto": "Define o que é 'saber' em 2022 para a OCDE. É a base metodológica que assegura confiabilidade e comparabilidade global.",
    "Mensagem": "Se você deseja compreender o DNA da avaliação internacional, comece por este protocolo."
}

col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/OECD_logo.svg/512px-OECD_logo.svg.png", width=180)
    st.metric(label="📂 Nº de Documentos", value=vol1_info["Documentos"])
    st.success(vol1_info["Função"])

with col2:
    st.markdown(f"### {vol1_info['Título']}")
    st.markdown(f"<p style='font-size:1.2em'>{vol1_info['Impacto']}</p>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Conteúdos Principais:")
    for item in vol1_info["Conteúdos-Chave"]:
        st.markdown(f"- {item}")
    st.info(f"🧠 {vol1_info['Mensagem']}")


# ===============================
# 📄 4. Destaques com tradução
# ===============================
st.markdown("## 📄 Exemplos de Protocolos Explicados (com tradução)")

exemplos = [
    {
        "titulo": "📋 TECHNICAL REPORT",
        "colecao": "protocolo_pisa_2022_tech_report",
        "descricao": "Documento técnico que define todos os parâmetros, metodologias, amostragem, tratamento estatístico e aplicações da Teoria de Resposta ao Item (TRI). É o coração dos bastidores do PISA.",
        "referencia": "PISA 2022 Technical Report-en.pdf"
    },
    {
        "titulo": "📄 SCHOOL QUESTIONNAIRE",
        "colecao": "protocolo_pisa_2022_quest_school_paper",
        "descricao": "Questionário aplicado à direção escolar, investigando recursos, infraestrutura, liderança e práticas pedagógicas. Crucial para cruzar contexto institucional com desempenho dos alunos.",
        "referencia": "SCHOOL QUESTIONNAIRE paper PISA 2022.pdf"
    },
    {
        "titulo": "📘 WELL-BEING QUESTIONNAIRE",
        "colecao": "protocolo_pisa_2022_scaling",
        "descricao": "Aborda aspectos de bem-estar físico, emocional e social do aluno. Contém itens sobre saúde mental, bullying, estresse, relações com colegas e percepção de pertencimento escolar.",
        "referencia": "WELL-BEING QUESTIONNAIRE PISA 2022.pdf"
    }
]

cols = st.columns(3)
for i, ex in enumerate(exemplos):
    with cols[i]:
        st.markdown(f"### {ex['titulo']}")
        st.markdown(f"**Arquivo**: `{ex['referencia']}`")
        st.markdown(ex["descricao"])
        
# ===============================
# 🧠 5. A Verdade por Trás de “Treinar para a Prova”
# ===============================
st.markdown("## 🧠 A Verdade por Trás de “Treinar para a Prova”")

with st.expander("🔍 Clique para compreender por que estratégias rasas não funcionam"):
    st.markdown("""
### 🎯 1. O PISA não mede apenas conteúdos, mas competências transferíveis
> O PISA avalia a capacidade de aplicar conhecimentos em contextos novos, com foco em resolução de problemas, interpretação, argumentação e pensamento crítico.

---

### 🧠 2. A prova é montada com base em modelos cognitivos complexos
> Os itens são calibrados pela **Teoria de Resposta ao Item (TRI)**. A nota não depende apenas de acertos, mas da **probabilidade de acerto em diferentes níveis de dificuldade**.

---

### ⚖️ 3. O desempenho é cruzado com variáveis socioeconômicas e emocionais
> O índice ESCS (econômico, social e cultural) impacta fortemente os resultados. 
Melhorar implica em **ações sistêmicas**, como:

- Leitura desde a infância  
- Formação docente contínua  
- Redução das desigualdades educacionais

---

### 📘 4. Conhecer os protocolos, critérios e rubricas do PISA permite criar políticas públicas eficazes
> Ex: Criar rubricas como a **SINAPSE**, alinhadas aos descritores do PISA, para promover **avaliação formativa e contextualizada**.

""")

# ===============================
# 🎓 6. Estrutura Cognitiva do PISA (Dimensões e Níveis)
# ===============================
st.markdown("## 📐 Estrutura Cognitiva do PISA – Dimensões, Níveis e Descritores")

with st.expander("🧮 Clique para ver a estrutura de cada área avaliada"):
    st.markdown("### 📚 Leitura")
    st.markdown("- **Dimensões**: Localizar informação, Compreender e interpretar, Avaliar e refletir")
    st.markdown("- **Níveis**: 1b a 6 – de leitura literal à análise crítica de ironias e argumentos")

    st.markdown("### 🧮 Matemática")
    st.markdown("- **Dimensões**: Formulação, Aplicação, Interpretação")
    st.markdown("- **Níveis**: 1 a 6 – de procedimentos simples a modelagens complexas")

    st.markdown("### 🔬 Ciências")
    st.markdown("- **Dimensões**: Explicação, Investigação, Interpretação de dados")
    st.markdown("- **Níveis**: 1 a 6 – de reconhecimento básico a aplicação de modelos científicos")

    st.markdown("### 📌 Exemplo de descritor real (Leitura, Nível 4):")
    st.info("📘 *Interpretar uma ironia sutil em um artigo de opinião e julgar sua relevância para o argumento central.*")

# ===============================
# 💡 7. Reflexão
# ===============================
st.markdown("## 💡 O que quase ninguém percebe sobre os protocolos...")

st.info("""
**Os protocolos do PISA não são apenas burocráticos.**

Eles **definem a confiabilidade da avaliação**, garantem **comparabilidade entre países**, e embutem critérios que afetam diretamente **quais conhecimentos são considerados válidos**, quais perguntas são **escaladas** e como as diferenças **socioeconômicas** são interpretadas.

Por isso, **conhecer os protocolos** é compreender **o DNA da avaliação internacional**.
""")

# ===============================
# 📈 8. Gráfico Longitudinal do Brasil
# ===============================
st.markdown("## 📈 Linha do Tempo: Participação do Brasil no PISA (2000–2022)")

dados_long = {
    "Ano": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022],
    "Leitura": [396, 403, 393, 412, 410, 407, 413, 410],
    "Matemática": [334, 356, 370, 386, 391, 377, 384, 379],
    "Ciências": [None, None, 390, 405, 405, 401, 404, 403]
}

df_long = pd.DataFrame(dados_long)
df_long = df_long.melt(id_vars="Ano", var_name="Área", value_name="Pontuação")

fig_long = px.line(df_long, x="Ano", y="Pontuação", color="Área",
                   markers=True, line_shape="spline",
                   title="Desempenho do Brasil no PISA por Área (2000–2022)",
                   labels={"Pontuação": "Pontuação Média", "Ano": "Ano"},
                   hover_name="Área")

fig_long.update_layout(hovermode="x unified", height=500)
st.plotly_chart(fig_long, use_container_width=True)

# ===============================
# 🏁 9. Conclusão em Destaque
# ===============================
st.markdown("## 🏁 Conclusão Estratégica")

st.success("""
📌 Os protocolos do PISA OCDE são mais do que diretrizes técnicas. Eles:

- Garantem **justiça internacional**, mesmo entre países desiguais.
- Promovem **confiabilidade estatística**, graças à TRI.
- Exigem **transparência** e rigor metodológico.

✅ **Quem compreende os protocolos, compreende o PISA.**
""")

st.markdown("""
### 📣 Se queremos melhorar o desempenho do Brasil:
> Não basta **"treinar para a prova"**.
É preciso compreender os **critérios cognitivos, os modelos avaliativos** e como o desempenho se conecta com **fatores estruturais, pedagógicos e sociais**.

🧭 **Compreensão estratégica + ação pedagógica = transformação educacional duradoura.**
""")

# ===============================
# 🎯 10. Epílogo Crítico: Compreender o jogo
# ===============================
st.markdown("---")

st.markdown("<h2 style='font-size: 2.2em; color: #c0392b;'>🔍 A Verdade por Trás dos Protocolos</h2>", unsafe_allow_html=True)

st.markdown("""
<div style='font-size: 1.4em; line-height: 1.8; text-align: justify;'>

🧭 <strong>“Os Protocolos do PISA não só revelam como se avalia, mas para quem se avalia — e com que propósito político e epistemológico.”</strong>

---

💥 <u>O que isso significa?</u> A maioria dos grupos para por aqui:

> "PISA usa TRI, tem questionários, dados socioeconômicos..."

Mas o <strong>nível avançado</strong> da discussão envolve:

---

🔍 <strong>1. Quem define o que é “saber”?</strong><br>
Os <i>frameworks</i> do PISA são elaborados por especialistas de países da OCDE — a maioria do hemisfério norte.<br><br>
🎯 Isso influencia quais competências são valorizadas (ex: leitura crítica, raciocínio matemático aplicado).<br>
🇧🇷 <strong>E o Brasil?</strong> Quais saberes são ignorados ou subvalorizados nos protocolos internacionais?

---

🌐 <strong>2. O PISA como ferramenta de <i>soft power</i></strong><br>
O PISA é usado para <i>induzir</i> políticas públicas: desde currículos até formação docente.<br>
📊 Protocolos como os questionários contextuais (ESCS, ICT, bem-estar) geram <strong>pressão internacional</strong> para reformas nacionais.

💡 <i>Ao compreendê-los, o Brasil pode responder criticamente — não apenas se submeter.</i>

---

📌 <strong>3. Gráfico Final Interpretativo</strong><br>
<em>(Já mostrado anteriormente)</em><br>
🎯 Mas ao invés de só exibir dados, usamos <u>anotações políticas e pedagógicas</u> que contextualizam cada ponto.

🗒️ <strong>Anotações:</strong>
<ul>
<li>📉 <strong>2003</strong>: Crise de aprendizagem e mudanças no ENEM</li>
<li>📈 <strong>2009</strong>: Impacto do IDEB e políticas de alfabetização</li>
<li>📉 <strong>2015</strong>: Crise institucional e cortes na educação</li>
<li>📈 <strong>2018–2022</strong>: Alinhamento ao PISA sem reformas estruturais</li>
</ul>

---

🧠 <strong>Epílogo Final:</strong><br>
<em>“Compreender os protocolos do PISA é enxergar o jogo por trás do jogo.</em><br>
Eles não apenas medem. <strong>Eles moldam.</strong><br>
Moldam currículos, políticas, investimentos e até a forma como o Brasil enxerga sua própria educação.

🗽 <strong>A leitura crítica dos protocolos não é só um ato técnico. É um ato político. Um ato de soberania epistemológica.”</strong>

</div>
""", unsafe_allow_html=True)

# ✅ Fechar conexão
if modo == "local":
    client.close()

