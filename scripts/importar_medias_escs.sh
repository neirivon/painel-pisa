#!/bin/bash

# Caminho do arquivo JSON
ARQUIVO_JSON="/home/neirivon/SINAPSE2.0/PISA/medias_pais_item_escs_2022.json"

# Nome do banco e coleção
BANCO="pisa"
COLECAO="medias_pais_item_escs_2022"

# Comando de importação
echo "📦 Importando arquivo para MongoDB..."
mongoimport \
  --uri="mongodb://admin:admin123@localhost:27017/?authSource=admin" \
  --db pisa \
  --collection medias_pais_item_escs_2022 \
  --file /home/neirivon/SINAPSE2.0/PISA/medias_pais_item_escs_2022.json \
  --jsonArray

echo "✅ Importação concluída com sucesso."

