import streamlit as st
from google.cloud import texttospeech
from google.cloud import speech_v1p1beta1 as speech # Importa a versão beta para recursos avançados se necessário, ou speech_v1p1beta1
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json
import io
from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- Carregamento de Credenciais ---
load_dotenv()
gcp_service_account_json_str = os.getenv("GOOGLE_CLOUD_KEY_JSON")

text_to_speech_client = None
speech_to_text_client = None

if gcp_service_account_json_str:
    try:
        gcp_service_account_info = json.loads(gcp_service_account_json_str)
        # Cria clientes para Text-to-Speech e Speech-to-Text
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

# --- Configuração do WebRTC (para captura de áudio) ---
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# --- Função para Transcrever Áudio ---
@st.cache_data(show_spinner=False) # Cache para evitar re-transcrições desnecessárias
def transcribe_audio_from_bytes(audio_bytes):
    if not speech_to_text_client:
        st.error("Cliente Speech-to-Text não inicializado.")
        return None

    # Converte bytes de áudio para um formato que o Speech-to-Text entenda (ex: FLAC ou WAV)
    # Assumindo que o áudio do WebRTC é mono e PCM linear
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm") # WebRTC geralmente entrega WebM
        # Salva para um buffer WAV (ou FLAC para melhor compressão se for grande)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0) # Volta ao início do buffer
    except Exception as e:
        st.error(f"Erro ao processar áudio (pydub): {e}")
        return None

    audio = speech.RecognitionAudio(content=wav_buffer.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Ou FLAC
        sample_rate_hertz=audio.frame_rate, # Usa a taxa de amostragem do áudio processado
        language_code="pt-BR",
        # Habilita pontuação automática e reconhecimento de fala aprimorado
        enable_automatic_punctuation=True,
        model="default", # Ou "latest_long" para áudios mais longos
    )

    try:
        response = speech_to_text_client.recognize(config=config, audio=audio)
        if response.results:
            return response.results[0].alternatives[0].transcript
        return "Nenhum texto reconhecido."
    except Exception as e:
        st.error(f"Erro ao chamar a API Speech-to-Text: {e}")
        return None

# --- Função para Sintetizar Texto ---
@st.cache_data(show_spinner=False) # Cache para evitar re-sínteses desnecessárias
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
st.info("Pressione 'Start' para começar a ditar e 'Stop' para finalizar. O texto será transcrito abaixo.")

# Componente WebRTC para gravação de áudio
webrtc_ctx = webrtc_streamer(
    key="speech_input",
    mode=WebRtcMode.SENDONLY,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
)

recorded_audio_bytes = None
if webrtc_ctx.audio_receiver:
    try:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        if audio_frames:
            # Concatena todos os bytes dos frames de áudio
            recorded_audio_bytes = b"".join([f.to_bytes() for f in audio_frames])
    except Exception as e:
        st.error(f"Erro ao capturar frames de áudio: {e}")

transcribed_text = ""
if recorded_audio_bytes:
    with st.spinner("Transcrevendo áudio..."):
        transcribed_text = transcribe_audio_from_bytes(recorded_audio_bytes)
        if transcribed_text:
            st.success("Transcrição concluída!")
            st.write(f"**Texto Ditado:** {transcribed_text}")
        else:
            st.warning("Não foi possível transcrever o áudio. Tente novamente.")

st.markdown("---")
st.header("2. Ouça a Transcrição em Voz (pt-BR-Neural2-C)")

if transcribed_text:
    if st.button("Ouvir Transcrição"):
        with st.spinner("Gerando áudio..."):
            audio_buffer = synthesize_text_to_speech(transcribed_text, text_to_speech_client)
            if audio_buffer:
                st.audio(audio_buffer.getvalue(), format="audio/mp3", start_time=0)
                st.download_button(
                    label="Baixar Áudio da Transcrição",
                    data=audio_buffer.getvalue(),
                    file_name="transcricao_aluno.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error("Não foi possível gerar o áudio da transcrição.")
else:
    st.info("Dite um texto acima para poder ouvi-lo.")

st.markdown("---")
st.caption("Desenvolvido com Google Cloud Speech-to-Text e Text-to-Speech")
