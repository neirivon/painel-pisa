import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np
import io

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_buffer = io.BytesIO()
        self.is_recording = True # Começa gravando para teste simples
        self.sample_rate = 16000
        self.channels = 1

    def recv(self, frame):
        if self.is_recording:
            audio_bytes = frame.to_ndarray(format="s16").tobytes()
            self.audio_buffer.write(audio_bytes)
        return frame

st.title("Teste de Microfone Streamlit-WebRTC")

webrtc_ctx = webrtc_streamer(
    key="test_audio_input",
    audio_processor_factory=AudioRecorder,
    async_processing=True,
    desired_playing_state={"playing": True},
    media_stream_constraints={"video": False, "audio": True},
)

if webrtc_ctx.audio_processor:
    st.write("Microfone ativo. Gravando...")
    # Você pode adicionar um botão para parar a gravação e processar aqui
    if st.button("Parar e Mostrar Tamanho do Buffer"):
        webrtc_ctx.audio_processor.stop_recording()
        st.write(f"Tamanho do buffer de áudio: {webrtc_ctx.audio_processor.audio_buffer.tell()} bytes")
else:
    st.warning("Aguardando microfone...")
