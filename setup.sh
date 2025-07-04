#!/bin/bash

echo "🔧 Iniciando verificação do ambiente para execução do PISA/OCDE..."

# Caminhos base
BASE_DIR=$(dirname "$0")
DADOS_CLOUD="$BASE_DIR/painel_pisa/utils/dados_cloud"
FAISS_DIR="$HOME/pisa_faiss"
FAISS_INDEX="$FAISS_DIR/pisa.index"

# 1. Criar diretórios de dados leves
echo "📁 Verificando diretórios de dados JSON/CSV..."

mkdir -p "$DADOS_CLOUD/2022"
mkdir -p "$DADOS_CLOUD/dados_saeb_inep/2021"
mkdir -p "$DADOS_CLOUD/relatorios_inep_pisa/2000"

# 2. Criar arquivos simulados se ainda não existirem
echo "📝 Verificando conteúdo de testes..."

if [ ! -f "$DADOS_CLOUD/2022/dados.json" ]; then
  echo '[{"aluno_id": 1, "pais": "Brasil", "nota_leitura": 420, "nota_matematica": 390}]' > "$DADOS_CLOUD/2022/dados.json"
fi

if [ ! -f "$DADOS_CLOUD/dados_saeb_inep/2021/dados.json" ]; then
  echo '{"media_geral_lp": 205.6, "media_geral_mt": 202.3, "descricao": "Simulado SAEB 2021 9º ano"}' > "$DADOS_CLOUD/dados_saeb_inep/2021/dados.json"
fi

if [ ! -f "$DADOS_CLOUD/relatorios_inep_pisa/2000/relatorio.json" ]; then
  echo '{"resumo": "Este é um relatório textual simulado do INEP sobre o PISA 2000 no Brasil."}' > "$DADOS_CLOUD/relatorios_inep_pisa/2000/relatorio.json"
fi

# 3. Verificar diretório FAISS
echo "🧠 Verificando diretório FAISS..."

if [ ! -d "$FAISS_DIR" ]; then
  mkdir -p "$FAISS_DIR"
  echo "⚠️ Diretório FAISS criado: $FAISS_DIR"
fi

if [ ! -f "$FAISS_INDEX" ]; then
  echo "⚠️ FAISS index ainda não existe. Lembre-se de colocar em: $FAISS_INDEX"
else
  echo "✅ FAISS index encontrado: $FAISS_INDEX"
fi

echo "✅ Setup finalizado com sucesso!"
echo "🌍 Modo atual de execução: ${PISA_MODO:-cloud}"

