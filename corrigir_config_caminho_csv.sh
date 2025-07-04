#!/bin/bash

# Caminho base do projeto
BASE_DIR=~/SINAPSE2.0/PISA

echo "🔍 Iniciando substituição de CONFIG[\"CAMINHO_CSV\"] por CONFIG[\"CAMINHO_DADOS\"] em: $BASE_DIR"
echo "🛑 Arquivos como 'config.py' e 'conexao_mongo.py' serão ignorados para evitar quebra."

# Procura e corrige em arquivos Python
find "$BASE_DIR" -type f -name "*.py" | while read -r file; do

  # Ignora arquivos de configuração
  if [[ "$file" == *"config.py" || "$file" == *"conexao_mongo.py" ]]; then
    echo "⏩ Ignorando: $file"
    continue
  fi

  # Verifica se há uso da chave antiga
  if grep -q 'CONFIG\["CAMINHO_CSV"\]' "$file"; then
    echo "✏️  Corrigindo: $file"

    # Backup de segurança
    cp "$file" "$file.bak"

    # Substituição segura
    sed -i 's/CONFIG\["CAMINHO_CSV"\]/CONFIG["CAMINHO_DADOS"]/g' "$file"

    echo "✅ Corrigido com sucesso."
  fi
done

echo "🎯 Finalizado. Backups .bak foram criados antes de cada alteração."

