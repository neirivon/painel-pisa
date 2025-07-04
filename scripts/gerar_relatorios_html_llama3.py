from pymongo import MongoClient
import os
from pathlib import Path
import requests
from datetime import datetime

# Diretórios de entrada e saída
input_dir = Path("avaliacoes_ia")
output_dir = Path("relatorios_ia_html")
output_dir.mkdir(exist_ok=True)

# Função para enviar prompt à IA LLaMA3 local (via Ollama)
def gerar_resposta_llama3(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.4,
            "top_k": 40,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"❌ Erro ao processar com LLaMA3: {e}")
        return None

# Execução principal com conexão segura (caso evolua com banco)
def main():
    # (Opcional) Conectar com MongoDB, mesmo que não seja usado agora
    with MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin") as client:
        print("✅ Conexão MongoDB aberta (não utilizada neste script, mas segura para expansão futura).")
        
        arquivos_txt = sorted(input_dir.glob("*.txt"))
        for arquivo in arquivos_txt:
            with open(arquivo, "r", encoding="utf-8") as f:
                prompt = f.read()

            print(f"📤 Gerando resposta para: {arquivo.name}")
            resposta = gerar_resposta_llama3(prompt)

            if resposta:
                nome_arquivo_html = output_dir / f"{arquivo.stem}.html"
                with open(nome_arquivo_html, "w", encoding="utf-8") as f_out:
                    f_out.write(f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório IA - {arquivo.stem}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    pre {{ background-color: #f4f4f4; padding: 15px; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h2>📄 Relatório Gerado por LLaMA3</h2>
  <p><strong>Fonte:</strong> {arquivo.name}</p>
  <p><strong>Data:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <hr>
  <pre>{resposta}</pre>
</body>
</html>
""")
                print(f"✅ Relatório salvo: {nome_arquivo_html.name}")
            else:
                print(f"⚠️ Falha ao gerar relatório para: {arquivo.name}")

if __name__ == "__main__":
    main()

