import streamlit as st
from google.cloud import texttospeech
from google.cloud import speech_v1p1beta1 as speech # Usamos a versão beta para streaming
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json
import io
import time
# Não precisamos mais de pydub para a transcrição direta de frames do webrtc
# from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, AudioFrame

# --- Carregamento de Credenciais ---
load_dotenv()
gcp_service_account_json_str = os.getenv("GOOGLE_CLOUD_KEY_JSON")

text_to_speech_client = None
speech_to_text_client = None

if gcp_service_account_json_str:
    try:
        gcp_service_account_info = json.loads(gcp_service_account_json_str)
        credentials = service_account.Credentials.from_service_account_info(gcp_service_account_info)
        text_to_speech_client = texttospeech.TextToSpeechClient(credentials=credentials)
        speech_to_text_client = speech.SpeechClient(credentials=credentials)
        st.sidebar.success("Credenciais do Google Cloud carregadas com sucesso via .env!")
    except json.JSONDecodeError as e:
        st.sidebar.error(f"Erro ao decodificar JSON das credenciais no .env: {e}")
        st.stop()
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar clientes do Google Cloud: {e}")
        st.stop()
else:
    # Fallback para Application Default Credentials ou Streamlit Cloud
    try:
        text_to_speech_client = texttospeech.TextToSpeechClient()
        speech_to_text_client = speech.SpeechClient()
        st.sidebar.warning("Variável GOOGLE_CLOUD_KEY_JSON não encontrada. Tentando usar Application Default Credentials (ADC) ou ambiente do Streamlit Cloud.")
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar clientes sem credenciais explícitas: {e}")
        st.stop()

# --- Configuração do WebRTC ---
# Configuração básica de ICE servers para WebRTC
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# --- Função para Sintetizar Texto (mantido igual) ---
@st.cache_data(show_spinner=False)
def synthesize_text_to_speech(text, client):
    if not client:
        st.error("Cliente Text-to-Speech não inicializado.")
        return None

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Neural2-C", # A voz feminina que você quer usar
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return io.BytesIO(response.audio_content)
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o áudio: {e}")
        return None

# --- Interface do Streamlit ---
st.title("Ditado do Aluno e Resposta em Voz")
st.markdown("---")

st.header("1. Dite o Texto do Aluno")
st.info("Pressione 'Start' para começar a ditar e 'Stop' para finalizar. O texto será transcrito em tempo real.")

# Componente WebRTC para gravação de áudio
webrtc_ctx = webrtc_streamer(
    key="speech_input",
    mode=WebRtcMode.SENDONLY,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True, # Importante para receber frames em segundo plano
)

# Armazena o resultado da transcrição no session_state para persistência
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# --- Lógica de Transcrição em Tempo Real ---
# Só processa se o cliente de Speech-to-Text estiver pronto e o stream do webrtc estiver ativo
if speech_to_text_client and webrtc_ctx.state.playing:
    # Gerador para produzir pedaços de áudio para a API de streaming
    # Esta função é executada no loop principal do Streamlit, coletando frames
    def audio_chunks_generator():
        # Continua a fornecer frames enquanto o áudio_receiver estiver ativo
        while webrtc_ctx.audio_receiver:
            try:
                # Pega todos os frames enfileirados desde a última leitura
                frames = webrtc_ctx.audio_receiver.get_queued_frames()
                if frames:
                    # Concatena os dados brutos de áudio de cada AudioFrame
                    # frame.to_ndarray() converte para um array NumPy
                    # .tobytes() converte o array NumPy para bytes brutos (PCM linear)
                    raw_audio_data = b"".join([frame.to_ndarray().tobytes() for frame in frames])
                    yield raw_audio_data
                else:
                    # Se não houver frames, espera um pouco para evitar consumo excessivo de CPU
                    time.sleep(0.01)
            except Exception as e:
                st.warning(f"Erro ao obter frames de áudio: {e}")
