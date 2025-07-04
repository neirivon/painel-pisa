#!/bin/bash

echo "🔧 Corrigindo nomes das funções em arquivos gerar_html_*.py..."

for file in gerar_html_*.py; do
    if [[ -f "$file" ]]; then
        numero=$(echo "$file" | grep -oP 'gerar_html_\K\d+')
        if [[ -n "$numero" ]]; then
            funcao="gerar_html_$numero"
            echo "📝 Corrigindo função em $file para: def $funcao()"
            # Substitui qualquer linha que começa com def gerar_html_* para o nome correto
            sed -i "s/^def gerar_html_.*:/def $funcao():/" "$file"
        fi
    fi
done

echo "✅ Correção concluída."

