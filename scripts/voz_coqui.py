# scripts/voz_coqui.py

from TTS.api import TTS
import os

# === Caminho de saída do áudio
output_dir = os.path.expanduser("~/SINAPSE2.0/PISA/modelos_coqui/xtts_v2")
os.makedirs(output_dir, exist_ok=True)

# === Texto a ser sintetizado
texto = """
Olá! Esta é uma demonstração de leitura em voz natural com o modelo Coqui XTTS versão dois.
Se você estiver participando de uma prova adaptada, poderá ouvir cada questão com nitidez, em português brasileiro.
"""

# === Inicializa o modelo XTTS v2 multilingue
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# === Lista de speakers disponíveis no modelo
print("\n🎤 Alto-falantes disponíveis:")
print(tts.speakers)

# === Seleciona o primeiro speaker disponível
speaker = tts.speakers[0]

# === Gera o áudio com idioma pt-BR
arquivo_saida = os.path.join(output_dir, "voz_teste_coqui.wav")
tts.tts_to_file(text=texto, speaker=speaker, language="pt", file_path=arquivo_saida)

print(f"\n✅ Áudio gerado com sucesso em: {arquivo_saida}")

