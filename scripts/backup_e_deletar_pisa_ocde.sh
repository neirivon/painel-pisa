#!/bin/bash

# Variáveis
CONTAINER="sinapse-mongodb"
USUARIO="admin"
SENHA="admin123"
DB="pisa_ocde"
PASTA_BACKUP_HOST="$HOME/SINAPSE2.0/backups/pisa_ocde"
PASTA_BACKUP_CONTAINER="/data/db/backup_$DB"

echo "📦 Iniciando backup do banco '$DB'..."

# Criar pasta local
mkdir -p "$PASTA_BACKUP_HOST"

# Backup dentro do container
docker exec "$CONTAINER" mongodump \
  --db "$DB" \
  --username "$USUARIO" \
  --password "$SENHA" \
  --authenticationDatabase admin \
  --out "$PASTA_BACKUP_CONTAINER"

# Verificar sucesso do backup
if [ $? -eq 0 ]; then
  echo "✅ Backup realizado com sucesso dentro do container."

  # Copiar backup para o host
  docker cp "$CONTAINER:$PASTA_BACKUP_CONTAINER" "$PASTA_BACKUP_HOST"

  if [ $? -eq 0 ]; then
    echo "📁 Backup copiado para $PASTA_BACKUP_HOST"

    # Apagar banco de dados
    echo "🗑️ Deletando banco '$DB' do MongoDB..."
    docker exec -i "$CONTAINER" mongosh -u "$USUARIO" -p "$SENHA" --authenticationDatabase admin --eval "use $DB; db.dropDatabase();"
    echo "✅ Banco '$DB' removido com segurança."

  else
    echo "❌ Erro ao copiar o backup para o host. Cancelando exclusão do banco."
  fi

else
  echo "❌ Erro ao executar mongodump. Backup não realizado."
fi

