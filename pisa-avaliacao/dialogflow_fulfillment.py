# dialogflow_fulfillment.py (na raiz do seu projeto ou em utils/ se preferir)

from flask import Flask, request, jsonify
import json
import os
import datetime
from dotenv import load_dotenv

# Importa as configurações e a função de conexão do seu projeto
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

load_dotenv() # Carrega variáveis de ambiente do .env

app = Flask(__name__)

# --- Carregamento de Questões ---
# Caminho para o arquivo de questões
# Ajuste o caminho se 'dialogflow_fulfillment.py' não estiver na raiz do projeto
# ou se o JSON estiver em outro local.
# Alterado para usar questoes_pisa_tri_mineiro_completas.json
QUESTOES_FILE_PATH = os.path.join(CONFIG.get("CAMINHO_DADOS"), "questoes", "questoes_pisa_tri_mineiro_completas.json")

try:
    with open(QUESTOES_FILE_PATH, 'r', encoding='utf-8') as f:
        questoes_list = json.load(f) # Carrega como uma lista diretamente 
    
    # Constrói o dicionário QUESTOES usando 'questao_id' como chave 
    # e armazena o dicionário completo da questão como valor.
    QUESTOES = {q['questao_id']: q for q in questoes_list} # 
    
    # Adicione a instrução inicial como parte das "questões" para fácil acesso.
    # Acessa o texto das instruções pela chave "texto".
    QUESTOES["instrucoes"] = {
        "id": "instrucoes",
        "texto": "Bem-vindo à avaliação PISA para alunos com deficiência visual. Ouça atentamente. Iremos começar com as instruções gerais. As instruções são: [Texto longo e detalhado das instruções da avaliação aqui]. Por favor, você entendeu as instruções? Deseja continuar?"
    }

    # O número total de questões é o tamanho do dicionário menos 1 (para as instruções)
    print(f"✅ {len(QUESTOES) - 1} questões carregadas do arquivo: {QUESTOES_FILE_PATH}")
except FileNotFoundError:
    print(f"❌ Erro: Arquivo de questões não encontrado em {QUESTOES_FILE_PATH}.")
    print("Usando questões de fallback.")
    QUESTOES = {
        "instrucoes": { # Ajustado para ter a chave 'texto'
            "id": "instrucoes",
            "texto": "Instruções de fallback: Bem-vindo à avaliação. Você entendeu? Deseja continuar?"
        },
        "L1": {"area": "Leitura", "pergunta": "Questão de fallback L1: Qual a capital do Brasil? Deseja começar a responder agora?"},
        "M1": {"area": "Matemática", "pergunta": "Questão de fallback M1: Dois mais dois? Deseja começar a responder agora?"}
    }
except json.JSONDecodeError as e:
    print(f"❌ Erro ao decodificar JSON das questões: {e}. Verifique o formato do arquivo {QUESTOES_FILE_PATH}")
    print("Usando questões de fallback.")
    QUESTOES = {
        "instrucoes": { # Ajustado para ter a chave 'texto'
            "id": "instrucoes",
            "texto": "Instruções de fallback: Bem-vindo à avaliação. Você entendeu? Deseja continuar?"
        },
        "L1": {"area": "Leitura", "pergunta": "Questão de fallback L1: Qual a capital do Brasil? Deseja começar a responder agora?"},
        "M1": {"area": "Matemática", "pergunta": "Questão de fallback M1: Dois mais dois? Deseja começar a responder agora?"}
    }


# --- Funções de Interação com MongoDB ---
def get_or_create_session_state(session_id, aluno_id="aluno_generico"):
    db, client = conectar_mongo(uri=CONFIG.get("MONGO_URI"), nome_banco=CONFIG.get("MONGO_BANCO"))
    try:
        respostas_collection = db['respostas_avaliacoes']
        state = respostas_collection.find_one({"session_id": session_id, "status": "em_andamento"})
        if not state:
            state = {
                "session_id": session_id,
                "aluno_id": aluno_id,
                "data_inicio": datetime.datetime.now(),
                "status": "em_andamento",
                "current_question": "0", # 0 para instruções, usar string para IDs de questão 
                "answers": []
            }
            respostas_collection.insert_one(state)
        return state
    finally:
        client.close()

def update_session_state_in_db(session_id, updates):
    db, client = conectar_mongo(uri=CONFIG.get("MONGO_URI"), nome_banco=CONFIG.get("MONGO_BANCO"))
    try:
        respostas_collection = db['respostas_avaliacoes']
        respostas_collection.update_one(
            {"session_id": session_id, "status": "em_andamento"},
            {"$set": updates}
        )
    finally:
        client.close()

def finalize_session_in_db(session_id):
    db, client = conectar_mongo(uri=CONFIG.get("MONGO_URI"), nome_banco=CONFIG.get("MONGO_BANCO"))
    try:
        respostas_collection = db['respostas_avaliacoes']
        respostas_collection.update_one(
            {"session_id": session_id, "status": "em_andamento"},
            {"$set": {"status": "finalizada", "data_fim": datetime.datetime.now()}}
        )
    finally:
        client.close()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req['queryResult']['intent']['displayName']
    session_id = req['session'].split('/')[-1]

    current_state = get_or_create_session_state(session_id)
    fulfillment_text = ""
    output_contexts = []

    # --- Lógica de Boas-Vindas ---
    if intent_name == "BoasVindas":
        fulfillment_text = QUESTOES["instrucoes"]["texto"] # Acessa a chave 'texto' 
        update_session_state_in_db(session_id, {"current_question": "0"}) # Usar string "0"
        output_contexts.append({"name": f"{req['session']}/contexts/InstrucoesLidas", "lifespanCount": 5})

    # --- Lógica de Entendimento das Instruções ---
    elif intent_name == "EntendimentoInstrucoes":
        entendeu = req['queryResult']['parameters'].get('sim_nao')
        if entendeu == "sim":
            # Usar uma lista ordenada de IDs de questões para controle da sequência
            questoes_ids_ordenadas = sorted([q_id for q_id in QUESTOES if q_id != "instrucoes"], key=lambda x: (x[0], int(x[1:]))) # L1, L2, M1, M2, C1, C2, etc.
            
            # Encontra a próxima questão na sequência
            if not current_state['current_question'] or current_state['current_question'] == "0":
                next_question_id = questoes_ids_ordenadas[0]
            else:
                try:
                    current_idx = questoes_ids_ordenadas.index(current_state['current_question'])
                    next_question_id = questoes_ids_ordenadas[current_idx + 1]
                except (ValueError, IndexError):
                    next_question_id = None # Não há próxima questão, ou erro

            if next_question_id:
                fulfillment_text = QUESTOES[next_question_id]["pergunta"] # Acessa a chave 'pergunta' 
                update_session_state_in_db(session_id, {"current_question": next_question_id})
                output_contexts.append({"name": f"{req['session']}/contexts/QuestaoLida", "lifespanCount": 5})
                output_contexts.append({"name": f"{req['session']}/contexts/InstrucoesLidas", "lifespanCount": 0})
            else:
                fulfillment_text = "Não há questões disponíveis para iniciar. Deseja enviar a prova?"
                output_contexts.append({"name": f"{req['session']}/contexts/UltimaQuestaoRespondida", "lifespanCount": 5})
                output_contexts.append({"name": f"{req['session']}/contexts/InstrucoesLidas", "lifespanCount": 0})
        else: # não
            fulfillment_text = QUESTOES["instrucoes"]["texto"] # Acessa a chave 'texto'
            output_contexts.append({"name": f"{req['session']}/contexts/InstrucoesLidas", "lifespanCount": 5})

    # --- Lógica de Iniciar Resposta da Questão ---
    elif intent_name == "IniciarRespostaQuestao":
        quer_responder = req['queryResult']['parameters'].get('sim_nao')
        if quer_responder == "sim":
            fulfillment_text = "Por favor, dite sua resposta. Quando terminar, diga 'terminei' ou 'concluí'."
            update_session_state_in_db(session_id, {"temp_answer": ""}) # Limpa resposta temporária
            output_contexts.append({"name": f"{req['session']}/contexts/AguardandoResposta", "lifespanCount": 5})
            output_contexts.append({"name": f"{req['session']}/contexts/QuestaoLida", "lifespanCount": 0})
        else:
            current_q_id = current_state.get('current_question', '0')
            q_text = QUESTOES.get(current_q_id, {}).get("pergunta", "a questão atual") # Segurança no acesso
            fulfillment_text = f"Ok. Me avise quando estiver pronto para responder {q_text}."
            output_contexts.append({"name": f"{req['session']}/contexts/QuestaoLida", "lifespanCount": 5})

    # --- Lógica de Captura da Resposta (do aluno) ---
    elif intent_name == "CapturaResposta":
        resposta_aluno_texto = req['queryResult']['queryText']
        update_session_state_in_db(session_id, {"temp_answer": resposta_aluno_texto}) # Armazena temporariamente no DB
        fulfillment_text = "Você terminou de responder? Deseja alterar algo?"
        output_contexts.append({"name": f"{req['session']}/contexts/AguardandoResposta", "lifespanCount": 5})

    # --- Lógica de Confirmação de Finalização da Resposta ---
    elif intent_name == "ConfirmarFinalizacaoResposta":
        terminou = req['queryResult']['parameters'].get('sim_nao')
        if terminou == "sim":
            question_id = current_state.get('current_question') # Agora é string 
            resposta_final = current_state.get('temp_answer', '')
            
            answers_list = current_state.get('answers', [])
            found = False
            for ans in answers_list:
                if ans.get('questao_id') == question_id: # Usar 'questao_id' para comparar 
                    ans['resposta_aluno'] = resposta_final
                    ans['horario_resposta'] = datetime.datetime.now()
                    ans['tentativas'] = ans.get('tentativas', 0) + 1
                    found = True
                    break
            if not found:
                answers_list.append({
                    "questao_id": question_id, # Usar 'questao_id' 
                    "texto_questao": QUESTOES.get(question_id, {}).get("pergunta", "Questão não encontrada"), # Acessa 'pergunta' 
                    "resposta_aluno": resposta_final,
                    "horario_resposta": datetime.datetime.now(),
                    "tentativas": 1
                })
            
            update_session_state_in_db(session_id, {
                "answers": answers_list,
                "temp_answer": "" # Limpa a resposta temporária no DB
            })

            output_contexts.append({"name": f"{req['session']}/contexts/AguardandoResposta", "lifespanCount": 0})
            output_contexts.append({"name": f"{req['session']}/contexts/RespostaArmazenada", "lifespanCount": 5})

            # Verifica se é a última questão
            # Para isso, precisamos da lista de IDs ordenadas
            questoes_ids_ordenadas = sorted([q_id for q_id in QUESTOES if q_id != "instrucoes"], key=lambda x: (x[0], int(x[1:])))
            if question_id == questoes_ids_ordenadas[-1]: # Se a ID da questão atual for a última da lista ordenada
                fulfillment_text = "Você finalizou todas as respostas. Deseja enviar a prova?"
                output_contexts.append({"name": f"{req['session']}/contexts/UltimaQuestaoRespondida", "lifespanCount": 5})
            else: # Não é a última questão
                fulfillment_text = "Deseja prosseguir para a próxima questão?"
                output_contexts.append({"name": f"{req['session']}/contexts/ProximaQuestao", "lifespanCount": 5})
        else: # deseja alterar
            fulfillment_text = "Certo. Por favor, dite sua resposta novamente."
            output_contexts.append({"name": f"{req['session']}/contexts/AguardandoResposta", "lifespanCount": 5})

    # --- Lógica de Próxima Questão ---
    elif intent_name == "ProximaQuestao":
        prosseguir = req['queryResult']['parameters'].get('sim_nao')
        if prosseguir == "sim":
            questoes_ids_ordenadas = sorted([q_id for q_id in QUESTOES if q_id != "instrucoes"], key=lambda x: (x[0], int(x[1:])))
            current_idx = questoes_ids_ordenadas.index(current_state['current_question'])
            
            if current_idx < len(questoes_ids_ordenadas) - 1: # Verifica se há uma próxima questão
                next_question_id = questoes_ids_ordenadas[current_idx + 1]
                fulfillment_text = QUESTOES[next_question_id]["pergunta"] # Acessa a chave 'pergunta' 
                update_session_state_in_db(session_id, {"current_question": next_question_id})
                output_contexts.append({"name": f"{req['session']}/contexts/QuestaoLida", "lifespanCount": 5})
                output_contexts.append({"name": f"{req['session']}/contexts/ProximaQuestao", "lifespanCount": 0})
            else: # Não há mais questões
                fulfillment_text = "Não há mais questões disponíveis. Você finalizou todas as respostas. Deseja enviar a prova?"
                output_contexts.append({"name": f"{req['session']}/contexts/UltimaQuestaoRespondida", "lifespanCount": 5})
                output_contexts.append({"name": f"{req['session']}/contexts/ProximaQuestao", "lifespanCount": 0})
        else:
            current_q_id = current_state.get('current_question', '0')
            q_text = QUESTOES.get(current_q_id, {}).get("pergunta", "a questão atual") # Segurança no acesso
            fulfillment_text = f"Ok. Me avise quando estiver pronto para a próxima questão ou para continuar com {q_text}."
            output_contexts.append({"name": f"{req['session']}/contexts/ProximaQuestao", "lifespanCount": 5})

    # --- Lógica de Confirmação de Envio da Prova ---
    elif intent_name == "ConfirmarEnvioProva":
        enviar = req['queryResult']['parameters'].get('sim_nao')
        if enviar == "sim":
            finalize_session_in_db(session_id) # Atualiza o status da sessão para 'finalizada' no DB
            fulfillment_text = "Prova enviada com sucesso! Obrigado por participar."
            # Lógica adicional para feedback ou redirecionamento no Streamlit, se aplicável
        else:
            fulfillment_text = "Certo. Você pode revisar suas respostas se desejar, ou podemos reenviar mais tarde."
            output_contexts.append({"name": f"{req['session']}/contexts/UltimaQuestaoRespondida", "lifespanCount": 5})

    else:
        fulfillment_text = "Desculpe, não entendi. Poderia repetir?"

    return jsonify({
        "fulfillmentText": fulfillment_text,
        "outputContexts": output_contexts
    })

if __name__ == '__main__':
    # Teste de conexão ao MongoDB ao iniciar o Flask
    try:
        # Pega as credenciais do CONFIG para testar
        test_db, test_client = conectar_mongo(uri=CONFIG.get("MONGO_URI"), nome_banco=CONFIG.get("MONGO_BANCO"))
        test_client.close()
        print("✅ Conexão ao MongoDB bem-sucedida ao iniciar o Fulfillment!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB na inicialização do Fulfillment: {e}")
        print("Certifique-se de que seu MongoDB Dockerizado está rodando e as variáveis de ambiente MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORTA, MONGO_BANCO estão corretas no .env.")

    # A porta 5000 é a porta padrão para Flask
    app.run(debug=True, port=5000)
