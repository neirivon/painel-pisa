#!/bin/bash

echo "🔐 Salvando token do GitHub permanentemente com segurança..."

# Solicita o token do usuário
read -s -p "👉 Cole aqui seu token do GitHub (invisível): " TOKEN
echo

# Salva no arquivo de credenciais
echo "https://neirivon:${TOKEN}@github.com" > ~/.git-credentials

# Configura o Git para usar armazenamento permanente
git config --global credential.helper store

# Protege o arquivo contra leitura por outros usuários
chmod 600 ~/.git-credentials

echo "✅ Token salvo com sucesso e protegido em ~/.git-credentials"

