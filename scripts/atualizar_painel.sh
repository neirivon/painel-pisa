#!/bin/bash

echo "🚀 Adicionando arquivos do painel ao Git..."

git add \
  painel_pisa/pages/01_Protocolos_PISA_OCDE.py \
  painel_pisa/pages/02_Entidade_Internacional_Organiza_PISA.py \
  painel_pisa/pages/03_O_que_e_o_PISA.py \
  painel_pisa/pages/04_Alunos_Viagem_Prova.py \
  painel_pisa/pages/05_Selecao_Candidatos.py \
  painel_pisa/pages/06_Tipos_de_Provas.py \
  painel_pisa/pages/07_Analise_Economica_Social.py \
  painel_pisa/pages/08_Rubrica_Correcao.py \
  painel_pisa/pages/09_Armazenamento_Dados_Representacao.py \
  painel_pisa/pages/10_Analise_Longitudinal_MongoDB_Streamlit.py \
  painel_pisa/pages/11_Analise_Longitudinal_Brasil.py \
  painel_pisa/pages/12_Questoes_PISA_SINAPSE.py \
  painel_pisa/pages/13_Gamificacao_Desempenho.py \
  painel_pisa/utils/config.py \
  painel_pisa/assets/imagens/grafico_protocolo_pisa_2022.png \
  painel_pisa/assets/imagens/nuvem_palavras_protocolo.png \
  .gitignore

echo "✅ Arquivos adicionados com sucesso."

git status

echo "📝 Pronto para commit. Use: git commit -m 'Sua mensagem'"

