# 🌐 Projeto PISA OCDE — Integrado ao Ecossistema SINAPSE2.0

Este projeto organiza e avalia questões abertas do **PISA OCDE**, adaptadas ao contexto da **mesorregião do Triângulo Mineiro e Alto Paranaíba**, com suporte do **Ecossistema Educacional SINAPSE2.0**, que integra:

- Inteligência Artificial (IA)
- Rubricas Pedagógicas Automatizadas (v6a)
- Taxonomia de Bloom, SOLO, Neuropsicopedagogia e DUA
- Metodologias Ativas e Contextualização Territorial

---

## 📁 Estrutura do Projeto

```
/home/neirivon/SINAPSE2.0/PISA
├── painel_pisa/                  # Aplicativo Streamlit
│   ├── Home.py                   # Página inicial
│   ├── pages/                    # Páginas secundárias
│   └── utils/                    # Estilo, config, conexão Mongo
├── dados_processados/
│   ├── rubricas/                 # Rubrica v6a (.json e .csv)
│   ├── questoes/                 # Questões ordenadas e completas
│   ├── respostas/                # Respostas dos alunos
├── scripts/                      # Scripts auxiliares
├── config/                       # Arquivos de configuração
```

---

## ▶️ Como Executar Localmente

> ⚠️ Sempre execute a partir da raiz do projeto: `/home/neirivon/SINAPSE2.0/PISA`

### 1. Ative o ambiente virtual

```bash
cd ~/SINAPSE2.0/PISA
source ../venv_sinapse/bin/activate
```

### 2. Execute o painel

```bash
streamlit run painel_pisa/Home.py
```

### 3. Acesse no navegador

```
http://localhost:8501
```

---

## ☁️ Deploy no Streamlit Cloud

1. Faça push do repositório para o GitHub
2. Crie o app na plataforma Streamlit Cloud
3. Configure:

```
Main file: painel_pisa/Home.py
Working directory: PISA
```

4. O modo cloud usa os arquivos `.json` e `.csv` em `dados_processados/`. MongoDB e FAISS são desativados.

---

## ⚙️ Configurações

Arquivo: `painel_pisa/utils/config.py`

```python
CONFIG = {
    "MODO": "local",         # ou "cloud"
    "USAR_MONGODB": True,    # apenas no modo local
}
```

---

## 🔧 Scripts úteis

```bash
# Verifica estrutura de pastas
python3 scripts/verificar_estrutura_sinapse.py

# Gera questões organizadas por área
python3 scripts/gerar_questoes_pisa_ordenadas.py

# Insere questões no MongoDB
python3 scripts/inserir_questoes_pisa_ordenadas.py
```

---

## 🧠 Avaliação com IA

As respostas dissertativas dos alunos são avaliadas automaticamente com a **Rubrica SINAPSE v6a**, que contempla:

- Perfil Neuropsicopedagógico
- DUA – Desenho Universal para Aprendizagem
- Metodologias Ativas
- Taxonomia SOLO
- Taxonomia de Bloom
- CTC – Contextualização Territorial e Cultural

Rubrica carregada automaticamente de:

```
dados_processados/rubricas/rubrica_sinapse_v6_adaptada.json
```

---

## 📚 Referências

- **OCDE.** *PISA 2018 Assessment and Analytical Framework*. OECD Publishing, 2019.
- **BRASIL.** *BNCC - Base Nacional Comum Curricular*. MEC, 2017.
- **BLOOM, B. S.** *Taxonomy of Educational Objectives*, 1956.
- **BIGGS, J.; COLLIS, K.** *SOLO Taxonomy*.
- **MORAN, J.** *Metodologias Ativas para uma Educação Inovadora*, 2015.
- **VYGOTSKY, L.** *A Formação Social da Mente*, Martins Fontes, 2001.

---

## ✅ Observações finais

📌 Sempre execute o projeto a partir de:

```
/home/neirivon/SINAPSE2.0/PISA
```

📦 Esse projeto é parte do Ecossistema SINAPSE2.0, mas o foco aqui é a **aplicação educacional do PISA OCDE** com IA e avaliação pedagógica.
# painel-pisa
