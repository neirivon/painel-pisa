#!/bin/bash

# Caminho destino
DESTINO=~/SINAPSE2.0/PISA/modelos_coqui/xtts_v2
mkdir -p "$DESTINO"
cd "$DESTINO"

# Baixar arquivos diretamente do Hugging Face
wget https://huggingface.co/coqui/xtts-v2/resolve/main/config.json
wget https://huggingface.co/coqui/xtts-v2/resolve/main/model.pth
wget https://huggingface.co/coqui/xtts-v2/resolve/main/speakers.pth
wget https://huggingface.co/coqui/xtts-v2/resolve/main/language_ids.json

echo "✅ Modelo XTTS v2 completo baixado para: $DESTINO"

