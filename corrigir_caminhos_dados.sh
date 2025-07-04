#!/bin/bash

# Caminho base
PROJETO=~/SINAPSE2.0/PISA

# Caminho hardcoded a ser substituído
ALVO_ANTIGO="/home/neirivon/SINAPSE2.0/PISA/dados_processados"
NOVO_CONFIG="CONFIG[\"CAMINHO_DADOS\"]"

# Linha de import que será garantida
IMPORT_LINE="from painel_pisa.utils.config import CONFIG"

echo "🔧 Iniciando verificação e substituição em: $PROJETO"
echo "🔍 Alvo: $ALVO_ANTIGO  →  $NOVO_CONFIG"
echo "⚙️  Garantindo presença de: $IMPORT_LINE"
sleep 1

# Buscar arquivos .py apenas
find "$PROJETO" -type f -name "*.py" | while read -r arquivo; do
  if grep -q "$ALVO_ANTIGO" "$arquivo"; then
    echo "✏️  Corrigindo: $arquivo"

    # Backup
    cp "$arquivo" "$arquivo.bak"

    # Substituição do caminho fixo pelo uso do CONFIG
    sed -i "s|\"$ALVO_ANTIGO|$NOVO_CONFIG|g" "$arquivo"

    # Garante import do CONFIG se não existir
    if ! grep -q "$IMPORT_LINE" "$arquivo"; then
      echo "🔼 Inserindo import do CONFIG em $arquivo"
      awk -v import_line="$IMPORT_LINE" '
        BEGIN {inserts=0}
        /^[ \t]*import |^[ \t]*from / {print; inserts=1; next}
        inserts == 1 {print import_line; inserts=0}
        {print}
      ' "$arquivo" > "$arquivo.tmp" && mv "$arquivo.tmp" "$arquivo"
    fi
  fi
done

echo "✅ Finalizado! Backups .bak disponíveis para restauração se necessário."

