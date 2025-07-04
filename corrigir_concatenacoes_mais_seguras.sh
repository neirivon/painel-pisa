#!/bin/bash

# ================================================================
# 🔧 Script Inteligente para Corrigir Concatenação com '+' em Caminhos
# Somente altera concatenação do tipo:
#   VAR = CONFIG["CAMINHO_DADOS"] + "/subpasta/arquivo.csv"
# para:
#   VAR = os.path.join(CONFIG["CAMINHO_DADOS"], "subpasta", "arquivo.csv")
# ================================================================

BASE_DIR="/home/neirivon/SINAPSE2.0/PISA"
echo "📁 Iniciando varredura em: $BASE_DIR"

find "$BASE_DIR" -type f -name "*.py" | while read -r file; do
    if grep -q 'CONFIG\["CAMINHO_DADOS"\] *\+ *["'\'']' "$file"; then
        echo "✏️  Corrigindo concatenação em: $file"
        cp "$file" "$file.bak"

        awk '
        /CONFIG\["CAMINHO_DADOS"\] *\+ *["'\'']/ {
            original = $0
            gsub(/.*CONFIG\["CAMINHO_DADOS"\] *\+ */, "", original)
            gsub(/ *\+ */, ", ", original)
            gsub(/^["'\'']|["'\'']$/, "", original)
            print "import os"
            print "CAMINHO = os.path.join(CONFIG[\"CAMINHO_DADOS\"]," original ")"
            next
        }
        { print $0 }
        ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        echo "✅ Corrigido: $file"
    fi
done

echo "🎯 Finalizado. Faça diff com os arquivos .bak se necessário."

