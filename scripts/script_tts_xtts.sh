#!/bin/bash

# Ativa o ambiente virtual
source ~/SINAPSE2.0/venv_sinapse/bin/activate

# Caminhos
DIR_BASE=~/SINAPSE2.0/PISA/modelos_coqui/XTTS-v2
MODEL_PATH="$DIR_BASE/model.pth"
CONFIG_PATH="$DIR_BASE/config.json"
SPEAKERS_PATH="$DIR_BASE/speakers_xtts.pth"
LANG_IDS_PATH="$DIR_BASE/language_ids.json"
OUT_PATH="$DIR_BASE/voz_ana_florence.wav"

# Texto a ser sintetizado
TEXTO="Olá! Esta é uma demonstração com a voz brasileira Ana Florence. Seja bem-vindo ao painel educacional inclusivo!"

# Executa a síntese
tts \
  --model_path "$MODEL_PATH" \
  --config_path "$CONFIG_PATH" \
  --speakers_file_path "$SPEAKERS_PATH" \
  --language_ids_file_path "$LANG_IDS_PATH" \
  --speaker_idx "voz_ana_florence" \
  --language_idx "pt" \
  --text "$TEXTO" \
  --out_path "$OUT_PATH"

