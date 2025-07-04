from flask import Flask, request, send_file
from weasyprint import HTML
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    html = request.form['html']
    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype='application/pdf', download_name='TCLE_Yasmin_Silva.pdf')

if __name__ == '__main__':
    app.run(debug=True)

