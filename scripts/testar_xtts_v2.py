# scripts/testar_xtts_v2.py

from TTS.api import TTS
import os

# Caminho para salvar o áudio gerado
output_path = os.path.expanduser("~/SINAPSE2.0/PISA/modelos_coqui/xtts_v2")
os.makedirs(output_path, exist_ok=True)

# Carrega automaticamente o modelo XTTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Texto a ser sintetizado
texto = "Olá! Este é um teste da voz em português brasileiro usando o modelo Coqui XTTS versão dois."

# Caminho de saída
arquivo_saida = os.path.join(output_path, "teste_vox.wav")

# Gera e salva o áudio
tts.tts_to_file(text=texto, speaker="random", language="pt", file_path=arquivo_saida)

print(f"✅ Áudio salvo com sucesso em: {arquivo_saida}")


