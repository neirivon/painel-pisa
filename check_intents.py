import os
import json
import tempfile # Adicione esta importação
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
GOOGLE_CLOUD_KEY_JSON_STR = os.getenv('GOOGLE_CLOUD_KEY_JSON') # Pega a string JSON do .env

def list_intents_with_training_phrases(project_id):
    """Lista todas as intenções de um dado projeto, incluindo suas frases de treinamento."""

    temp_key_file_path = None # Inicializa para o finally

    # --- Bloco de autenticação usando a chave de serviço do .env ---
    if GOOGLE_CLOUD_KEY_JSON_STR:
        try:
            # Cria um arquivo temporário para a chave de serviço
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_key_file:
                temp_key_file.write(GOOGLE_CLOUD_KEY_JSON_STR)
                temp_key_file_path = temp_key_file.name

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key_file_path
            print("Credenciais carregadas via GOOGLE_CLOUD_KEY_JSON temporário.")
            print(f"Caminho do arquivo temporário: {temp_key_file_path}") # Adicione para depuração

            # Opcional: Para verificar o conteúdo do arquivo temporário
            # with open(temp_key_file_path, 'r') as f:
            #     print("Conteúdo do arquivo temporário:")
            #     print(f.read()[:200]) # Mostra os primeiros 200 caracteres

        except Exception as e:
            print(f"Erro ao processar GOOGLE_CLOUD_KEY_JSON: {e}")
            print("Tentando prosseguir com as credenciais padrão do ambiente.")
    # --- Fim do bloco de autenticação ---

    # Inicializa o IntentsClient (para listar intenções)
    intents_client = dialogflow.IntentsClient()

    # Inicializa o AgentsClient (para obter o caminho do agente)
    agents_client = dialogflow.AgentsClient()

    # Constrói o caminho completo do agente usando o AgentsClient
    parent = agents_client.agent_path(project_id)

    print(f"Cliente Dialogflow inicializado para o projeto: {project_id}")

    try:
        intents = intents_client.list_intents(parent=parent)

        print(f"Intenções para o projeto '{project_id}':")
        for intent in intents:
            print(f"\n  Nome de Exibição da Intenção: {intent.display_name}")
            print(f"  Frases de Treinamento:")
            if intent.training_phrases:
                for training_phrase in intent.training_phrases:
                    phrase_text = "".join([part.text for part in training_phrase.parts])
                    print(f"    - {phrase_text}")
            else:
                print("    (Nenhuma frase de treinamento configurada)")

    except Exception as e:
        print(f"Erro ao listar intenções: {e}")
    finally:
        # Limpeza: remove o arquivo temporário de credenciais se ele foi criado
        if temp_key_file_path and os.path.exists(temp_key_file_path):
            os.remove(temp_key_file_path)
            print(f"Arquivo temporário de credenciais removido: {temp_key_file_path}")


if __name__ == '__main__':
    if PROJECT_ID:
        print("Credenciais do Google Cloud carregadas do .env!")
        list_intents_with_training_phrases(PROJECT_ID)
    else:
        print("Erro: A variável de ambiente GOOGLE_CLOUD_PROJECT não está definida.")
        print("Por favor, defina-a no seu arquivo .env ou diretamente no ambiente.")
