import os
import io
import json
from dotenv import load_dotenv
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

# --- Carregamento de Credenciais ---
load_dotenv()
gcp_service_account_json_str = os.getenv("GOOGLE_CLOUD_KEY_JSON")

speech_to_text_client = None

if gcp_service_account_json_str:
    try:
        gcp_service_account_info = json.loads(gcp_service_account_json_str)
        credentials = service_account.Credentials.from_service_account_info(gcp_service_account_info)
        speech_to_text_client = speech.SpeechClient(credentials=credentials)
        print("Credenciais do Google Cloud carregadas com sucesso via .env!")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON das credenciais no .env: {e}")
        exit() # Sai do script se houver erro crítico
    except Exception as e:
        print(f"Erro ao inicializar cliente do Google Cloud: {e}")
        exit()
else:
    try:
        speech_to_text_client = speech.SpeechClient()
        print("Variável GOOGLE_CLOUD_KEY_JSON não encontrada. Tentando usar Application Default Credentials (ADC).")
    except Exception as e:
        print(f"Erro ao inicializar cliente sem credenciais explícitas: {e}")
        exit()

# --- Função para Transcrever Áudio de um Arquivo ---
def transcribe_audio_file(audio_file_path, client):
    """Transcreve um arquivo de áudio usando a API Google Cloud Speech-to-Text."""
    if not os.path.exists(audio_file_path):
        print(f"Erro: Arquivo de áudio não encontrado em '{audio_file_path}'")
        return None

    # Carrega o conteúdo do arquivo de áudio
    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    # Configuração de reconhecimento
    # IMPORTANTE: ajuste sample_rate_hertz e encoding para o formato do seu arquivo de áudio
    # Se for MP3, a API do Google geralmente consegue inferir, mas WAV é mais direto.
    # Para WAV, geralmente é LINEAR16. Para MP3, pode ser MP3.
    # Para simplicidade, vamos usar um modelo "default" que é mais flexível.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Ex: Para WAV. Se for MP3, use MP3
        sample_rate_hertz=16000, # Ex: Para WAV gravado em 16kHz. Ajuste conforme seu áudio
        language_code="pt-BR",
        enable_automatic_punctuation=True,
        model="default", # Use "default" para ser mais flexível, ou "command_and_search" para comandos curtos
    )

    print(f"Enviando '{audio_file_path}' para transcrição...")
    try:
        response = client.recognize(config=config, audio=audio)

        for result in response.results:
            print(f"Transcrição completa: {result.alternatives[0].transcript}")
            return result.alternatives[0].transcript
        return "Nenhum texto reconhecido."
    except Exception as e:
        print(f"Erro ao chamar a API Speech-to-Text: {e}")
        print("Verifique se o 'encoding' e 'sample_rate_hertz' estão corretos para o seu arquivo de áudio.")
        return None

# --- Lógica de Execução de Ações Baseada no Comando ---
def execute_command(command_text):
    """Executa uma ação baseada no texto do comando."""
    command_text_lower = command_text.lower()

    if "abrir navegador" in command_text_lower:
        print("Ação: Abrindo o navegador web...")
        # Você pode adicionar código real aqui para abrir um navegador
        # Ex: import webbrowser; webbrowser.open('http://google.com')
    elif "desligar luzes" in command_text_lower:
        print("Ação: Desligando as luzes...")
        # Adicione lógica para controlar lâmpadas inteligentes
    elif "tocar música" in command_text_lower:
        print("Ação: Iniciando a reprodução de música...")
        # Adicione lógica para tocar música
    elif "qual a hora" in command_text_lower or "que horas são" in command_text_lower:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Ação: A hora atual é {current_time}.")
    else:
        print(f"Ação: Comando '{command_text}' não reconhecido.")

# --- Execução Principal ---
if __name__ == "__main__":
    # Caminho para o seu arquivo de áudio de teste
    # Certifique-se de que este caminho está correto para o seu arquivo de áudio!
    AUDIO_FILE = "audio_testes/comando_navegador.wav" # Exemplo: Crie uma pasta 'audio_testes' e coloque seu WAV/MP3 lá

    if speech_to_text_client:
        transcribed = transcribe_audio_file(AUDIO_FILE, speech_to_text_client)
        if transcribed and transcribed != "Nenhum texto reconhecido.":
            execute_command(transcribed)
        else:
            print("Não foi possível executar o comando pois nenhum texto foi reconhecido.")
    else:
        print("Cliente Speech-to-Text não pôde ser inicializado. Verifique as credenciais.")
