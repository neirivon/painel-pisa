# 🌐 Projeto PISA OCDE — Streamlit Cloud

Este app avalia questões dissertativas do PISA adaptadas ao contexto do Triângulo Mineiro e Alto Paranaíba, com base na **Rubrica SINAPSE v6a**.

---

## 🚀 Como acessar

Acesse gratuitamente o painel interativo hospedado no Streamlit Cloud:  
🔗 [https://seu-app.streamlit.app](https://seu-app.streamlit.app)

---

## 📁 Organização dos dados

O aplicativo utiliza os seguintes arquivos:

```
dados_processados/
├── rubricas/
│   └── rubrica_sinapse_v6_adaptada.json
├── questoes/
│   └── questoes_pisa_ordenadas.json
```

Esses dados são carregados automaticamente no modo Cloud, sem necessidade de banco de dados.

---

## 🧠 Avaliação com IA

As respostas dos alunos são analisadas com base em 6 dimensões:

- **Perfil Neuropsicopedagógico**
- **DUA – Desenho Universal para Aprendizagem**
- **Metodologias Ativas**
- **Taxonomia SOLO**
- **Taxonomia de Bloom**
- **CTC – Contextualização Territorial e Cultural**

A pontuação vai de 1 a 5 para cada dimensão, com feedback formativo imediato.

---

## 📚 Referências

- **OCDE.** *PISA 2018 Assessment and Analytical Framework*. OECD Publishing.
- **BRASIL.** *BNCC - Base Nacional Comum Curricular*. MEC, 2017.
- **Bloom, B.** *Taxonomy of Educational Objectives*.
- **Biggs & Collis.** *SOLO Taxonomy*.
- **Moran, J.** *Metodologias Ativas para uma Educação Inovadora*.
- **Vygotsky, L.** *A Formação Social da Mente*.

---

## ⚠️ Observações

- Este painel **não usa MongoDB ou FAISS no modo Cloud**
- Todos os dados são locais (JSON/CSV)
- Para execução local completa com IA expandida, consulte o `README.md`
