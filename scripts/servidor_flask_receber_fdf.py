from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "./respostas_pdf"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/receber", methods=["POST"])
def receber_formulario():
    try:
        fdf_data = request.get_data()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        caminho_fdf = os.path.join(UPLOAD_FOLDER, f"resposta_{timestamp}.fdf")
        with open(caminho_fdf, "wb") as f:
            f.write(fdf_data)

        print(f"✅ FDF salvo: {caminho_fdf}")
        return "✔️ Formulário recebido com sucesso!", 200
    except Exception as e:
        print("❌ Erro:", e)
        return "Erro ao processar o formulário", 500

if __name__ == "__main__":
    print("🚀 Servidor Flask aguardando formulários em http://localhost:5000/receber")
    app.run(host="0.0.0.0", port=5000, debug=True)

