import os
import io
import json
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

# --- 1. Carregar as variáveis do arquivo .env ---
# Certifique-se de que seu arquivo .env está na mesma pasta que este script
# e que a variável GOOGLE_CLOUD_KEY_JSON está configurada lá.
load_dotenv()
gcp_service_account_json_str = os.getenv("GOOGLE_CLOUD_KEY_JSON")

text_to_speech_client = None

if gcp_service_account_json_str:
    try:
        # Converte a string JSON de volta para um objeto Python (dicionário)
        gcp_service_account_info = json.loads(gcp_service_account_json_str)
        
        # --- 2. Inicializar o cliente com as credenciais da conta de serviço ---
        # A biblioteca google-cloud-texttospeech usará estas credenciais
        credentials = service_account.Credentials.from_service_account_info(gcp_service_account_info)
        text_to_speech_client = texttospeech.TextToSpeechClient(credentials=credentials)
        print("INFO: Credenciais do Google Cloud carregadas com sucesso via .env!")
    except json.JSONDecodeError as e:
        print(f"ERRO: Erro ao decodificar JSON das credenciais no .env: {e}")
        exit(1) # Sai do script se houver erro crítico
    except Exception as e:
        print(f"ERRO: Erro ao inicializar o cliente Text-to-Speech com credenciais do .env: {e}")
        exit(1)
else:
    print("ALERTA: Variável GOOGLE_CLOUD_KEY_JSON não encontrada no .env.")
    print("ALERTA: Tentando usar Application Default Credentials (ADC).")
    try:
        # Tenta usar ADC (se gcloud auth application-default login foi usado)
        text_to_speech_client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print(f"ERRO: Erro ao inicializar o cliente Text-to-Speech sem credenciais explícitas: {e}")
        print("Por favor, configure GOOGLE_CLOUD_KEY_JSON no seu .env ou use 'gcloud auth application-default login'.")
        exit(1)

# --- 3. Definir o texto a ser sintetizado ---
text_to_synthesize = "Olá! Este é um teste para demonstrar que a permissão de Text-to-Speech da sua conta de serviço está funcionando corretamente."

# --- 4. Configurar a requisição de síntese de fala ---
synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)

# Usaremos a mesma voz feminina natural (pt-BR-Neural2-C)
voice = texttospeech.VoiceSelectionParams(
    language_code="pt-BR",
    name="pt-BR-Neural2-C",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

# Configurar o formato de áudio de saída
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# --- 5. Chamar a API Text-to-Speech ---
print(f"\nINFO: Tentando sintetizar a fala: '{text_to_synthesize}'")
try:
    response = text_to_speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # --- 6. Salvar o áudio em um arquivo ---
    output_audio_file = "saida_tts_demo.mp3"
    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)
    
    print(f"SUCESSO: Áudio gerado com sucesso e salvo em '{output_audio_file}'")
    print("SUCESSO: Isso demonstra que o papel 'roles/serviceusage.serviceUsageConsumer' em sua conta de serviço 'streamlit-pisa-service-account' está funcionando para a API Text-to-Speech!")

except Exception as e:
    print(f"ERRO: Ocorreu um erro ao chamar a API Text-to-Speech: {e}")
    print("ERRO: Se você vir 'Permission denied' ou 'Forbidden', o papel pode não estar ativo ou pode haver outro problema de permissão.")
    print("ERRO: Verifique se a API Cloud Text-to-Speech está habilitada no projeto.")
    exit(1)
