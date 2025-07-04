
# 📘 Painel Educacional – PISA OCDE 2022

Este projeto Streamlit apresenta uma análise pedagógica da edição 2022 do PISA OCDE, com foco em rubricas avaliativas, níveis da Taxonomia de Bloom, perfil neuropsicopedagógico, estratégias de aprendizagem e comparações com dados do SAEB.

> **Objetivo:** Servir como modelo replicável para as demais edições (2000 a 2022) e apoiar a construção de políticas educacionais baseadas em dados.

---

## 🧩 Equipe e Instituição

**Projeto desenvolvido por:**  
🧑‍🏫 **EQUIPE PISA**  
🏫 **INSTITUTO FEDERAL DO TRIÂNGULO MINEIRO – CAMPUS UBERABA**  
📚 **Disciplina:** Avaliação nos Espaços Educacionais  
👨‍🏫 **Professor:** Bruno Garcês  
🔗 **GitHub:** [https://github.com/neirivon](https://github.com/neirivon)

---

## 📁 Estrutura do Projeto

```
painel_pisa/
├── Home.py
├── pages/
│   ├── 01_Resumo_Edicao.py
│   ├── 02_Analise_Textual.py
│   └── ...
├── utils/
│   ├── estilo_global.py
│   ├── conexao_mongo.py
├── amostra_rotulagem_pisa2022.json
├── requirements.txt
├── README.md
├── dados_pisa/
│   ├── CY1MDAI_STU_QQQ.sav
│   ├── CY1MDAI_TCH_QQQ.sas7bdat
│   └── ...
├── exports_html/
│   ├── 01_Resumo_Edicao.html
│   ├── 02_Distribuicao_Rubricas_SAEB.html
│   ├── 05_Rubricas_Avaliativas.html
│   └── ...
```

---

## 🚀 Como fazer o deploy no Streamlit Cloud

1. Crie uma conta no [GitHub](https://github.com)
2. Crie um repositório público com os arquivos do projeto
3. Vá para: [https://streamlit.io/cloud](https://streamlit.io/cloud)
4. Faça login com GitHub e clique em **"New App"**
5. Selecione:
   - **Repository:** `seu-usuario/painel-pisa-2022`
   - **Branch:** `main`
   - **Main file path:** `Home.py`
6. Clique em **Deploy**

> O link será algo como: `https://seu-usuario.streamlit.app/`

---

## 📦 Requisitos do Projeto

Exemplo de `requirements.txt`:

```txt
streamlit
pandas
pymongo
plotly
```

---

## 📥 Download da Amostra para Rotulagem

O arquivo `amostra_rotulagem_pisa2022.json` contém trechos do relatório PISA 2022 para rotulagem por juízes pedagógicos.

Você pode habilitar o botão de download no painel:

```python
st.download_button(
    label="📥 Baixar amostra para rotulagem",
    file_name="amostra_rotulagem_pisa2022.json",
    mime="application/json",
    data=json.dumps(amostra_final, ensure_ascii=False, indent=4)
)
```

---

## 🧠 Fundamentos Teóricos Utilizados

- **Taxonomia de Bloom**
- **Neuropsicopedagogia**
- **Metodologias Ativas**
- **Desenho Universal para Aprendizagem (DUA)**
- **Relatórios PISA/OCDE e INEP**
- **Base SAEB para triangulação nacional**

---

## 📧 Contato

Desenvolvido por **Equipe PISA – IFTM Campus Uberaba**  
Orientação do prof. Bruno Garcês  
GitHub: [https://github.com/neirivon](https://github.com/neirivon)
