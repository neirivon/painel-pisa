import requests

# Configurações
url = "http://localhost:11434/api/generate"
model_name = "llama3"

# Prompt que você quer enviar ao modelo
prompt = """
Explique como funciona uma rede neural artificial de forma simples.
"""

# Dados da requisição
data = {
    "model": model_name,
    "prompt": prompt,
    "stream": False  # Se quiser ver a resposta completa de uma vez
}

# Fazendo a requisição POST
response = requests.post(url, json=data)

# Verificando a resposta
if response.status_code == 200:
    result = response.json()
    print("🧠 Resposta do LLAMA3:")
    print(result['response'])
else:
    print(f"❌ Erro na requisição. Código HTTP: {response.status_code}")
    print(response.text)
