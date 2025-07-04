
import os
import time
from TTS.api import TTS
import pysrt
from pydub import AudioSegment

# Configurações
srt_file = "mantra_sinapse_base.srt"
reference_audio = "voz_ana_florence.wav"
output_dir = "saida_blocos_xtts"
final_output = "mantra_voz_ana_sincronizado.wav"

# Inicializa o modelo XTTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=True)

# Cria pasta de saída
os.makedirs(output_dir, exist_ok=True)

# Carrega legendas
subs = pysrt.open(srt_file, encoding="utf-8")

# Gera áudios por bloco
blocos_audio = []
for i, sub in enumerate(subs):
    texto = sub.text.replace("\n", " ").strip()
    bloco_output_path = os.path.join(output_dir, f"bloco_{i+1:02}.wav")

    tts.tts_to_file(
        text=texto,
        speaker_wav=reference_audio,
        language="pt",
        file_path=bloco_output_path
    )

    print(f"✅ Bloco {i+1} gerado: {bloco_output_path}")
    time.sleep(0.2)  # pausa leve entre blocos
    blocos_audio.append(AudioSegment.from_wav(bloco_output_path))

# Junta todos os blocos com silêncio entre eles (ajuste se quiser pausas específicas)
audio_final = AudioSegment.silent(duration=500)
for bloco in blocos_audio:
    audio_final += bloco + AudioSegment.silent(duration=500)

# Exporta áudio final
audio_final.export(final_output, format="wav")
print(f"✅ Áudio final exportado: {final_output}")
