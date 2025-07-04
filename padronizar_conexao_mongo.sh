#!/bin/bash

# Caminho base do projeto
BASE_DIR=~/SINAPSE2.0/PISA

# Caminho para o padrão que será aplicado
PADRAO_IMPORTS='from painel_pisa.utils.conexao_mongo import conectar_mongo\nfrom painel_pisa.utils.config import CONFIG'

# Evita arquivos sensíveis
EXCLUIR_ARQUIVOS="config.py conexao_mongo.py"

echo "🔍 Procurando conexões fixas de MongoDB em: $BASE_DIR"

# Encontra arquivos Python com MongoClient hardcoded
grep -rl 'MongoClient("mongodb://admin:admin123@localhost:27017' $BASE_DIR | while read arquivo; do
    nome_arquivo=$(basename "$arquivo")
    
    # Verifica se é um dos arquivos a ignorar
    if [[ " $EXCLUIR_ARQUIVOS " =~ " $nome_arquivo " ]]; then
        echo "⚠️  Ignorando: $arquivo"
        continue
    fi

    echo "✏️  Corrigindo: $arquivo"

    # Faz backup
    cp "$arquivo" "$arquivo.bak"

    # Substitui linha de conexão direta por chamada à função conectar_mongo
    sed -i 's|conectar_mongo(nome_banco="saeb")[1]|conectar_mongo(nome_banco="saeb")[1]|g' "$arquivo"

    # Garante que os imports existam no topo
    grep -q "from painel_pisa.utils.conexao_mongo import conectar_mongo" "$arquivo" || \
        sed -i "1i $PADRAO_IMPORTS" "$arquivo"
    
    echo "✅ Corrigido com sucesso."
done

echo "🎯 Finalizado. Backups .bak foram criados antes de cada alteração."

