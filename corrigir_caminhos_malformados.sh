#!/bin/bash

echo "📁 Verificando arquivos Python em: $(pwd)"

# Caminho raiz do projeto
BASE_DIR="$(pwd)"

# Encontrar todos os arquivos .py
find "$BASE_DIR" -type f -name "*.py" | while read -r file; do
    echo "🔍 Verificando: $file"

    # Correção 1: Substituir uso de "~/algum_caminho" por os.path.join(os.getenv("HOME"), "algum_caminho")
    sed -i.bak 's|["'\'']~/\([^"'\'']*\)["'\'']|os.path.join(os.getenv("HOME"), "\1")|g' "$file"

    # Correção 2: Substituir uso de "/" para concatenar caminhos por os.path.join (versão básica)
    sed -i.bak 's|\([^"'"'"']\)/\([^"'"'"']\)|os.path.join(\1, "\2")|g' "$file"

    # Correção 3: Identificar concatenação de strings com "+" em caminhos (aviso apenas)
    if grep -q '"\s*\+\s*"' "$file"; then
        echo "⚠️  [AVISO] Concatenação com '+' detectada em: $file — verifique manualmente."
    fi
done

echo "✅ Correções aplicadas. Backups .bak foram gerados para cada arquivo modificado."

