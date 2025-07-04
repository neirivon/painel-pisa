from moviepy import AudioFileClip, TextClip, CompositeVideoClip, ColorClip
import pysrt

# === Caminhos dos arquivos ===
audio_path = "mantra_voz_ana_sincronizado.wav"
srt_path = "/home/neirivon/SINAPSE2.0/PISA/mantra_sinapse_base.srt"
saida_video = "/home/neirivon/SINAPSE2.0/PISA/video_mantra_sinapse_legenda.mp4"

# === Carregar áudio ===
audio_clip = AudioFileClip(audio_path)
duracao_total = audio_clip.duration

# === Fundo preto com áudio ===
video_fundo = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duracao_total).with_audio(audio_clip)

# === Carrega legendas do SRT ===
subtitulos = pysrt.open(srt_path, encoding="utf-8")

# === Legendas sincronizadas ===
clipes_legenda = []
for sub in subtitulos:
    start = sub.start.ordinal / 1000
    end = sub.end.ordinal / 1000
    duracao = end - start

    texto = sub.text.replace("\n", " ").strip()

    txt_clip = TextClip(
        text=texto,
        method="caption",
        size=(1600, 1080),
        color="yellow"  # 👈 Aqui define a cor
    ).with_start(start).with_duration(duracao).with_position("center")

    clipes_legenda.append(txt_clip)

# === Composição final ===
video_final = CompositeVideoClip([video_fundo, *clipes_legenda])
video_final.write_videofile(saida_video, fps=24, codec="libx264", audio_codec="aac")

