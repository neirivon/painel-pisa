import json
import hashlib
from weasyprint import HTML
import os

# Dados do TCLE
dados = {
    "titulo": "📄 Termo de Consentimento Livre e Esclarecido (TCLE)",
    "identificacao": "👩‍⚖️ Identificação da Juíza Avaliadora",
    "nome": "Yasmin Silva Cardoso",
    "area": "Designer Gráfico, área educacional",
    "instituicao": "ESAMC",
    "cidade": "Uberlândia – MG",
    "email": "yasminkatherinevc@gmail.com",
    "whatsapp": "📲 (34) 9.9206-6233",
    "titulo_pesquisa": "“Avaliação dos Descritores da Rubrica SINAPSE IA – Dimensão: Capacidade de Comunicação e Expressão”",
    "responsavel": "Neirivon Elias Cardoso",
    "instituicao_responsavel": "Instituto Federal do Triângulo Mineiro – Campus Uberaba",
    "projeto": "📊 PISA OCDE",
    "objetivo": "🧠 Aprimorar práticas de avaliação pedagógica assistida por Inteligência Artificial (IA)",
    "referenciais": [
        "📘 Taxonomia de Bloom",
        "📙 Taxonomia SOLO",
        "🧠 Neuropsicopedagogia",
        "🎲 Metodologias Ativas",
        "♿ Desenho Universal para Aprendizagem (DUA)",
        "📚 BNCC",
        "🧪 SAEB",
        "🌍 PISA"
    ],
    "forma_consentimento": "📝 Preenchimento online com geração de assinatura digital via HASH",
    "participacao": "🧩 Juíza avaliadora, atribuindo níveis de 1 a 4 para os descritores da rubrica",
    "privacidade": "🔐 Dados anonimizados, uso exclusivamente científico, sem riscos ou benefícios financeiros.",
    "contato": {
        "email": "neirivon.elias@estudante.iftm.edu.br",
        "telefone": "📲 (34) 9 9925-5385"
    }
}

# Gerar o HASH
hash_gerado = hashlib.sha256(json.dumps(dados, sort_keys=True).encode("utf-8")).hexdigest()

# HTML formatado com CSS
html = f"""
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      padding: 30px;
      font-size: 14pt;
      line-height: 1.6;
    }}
    h1 {{
      text-align: center;
      color: #2c3e50;
      font-size: 22pt;
    }}
    h2 {{
      color: #34495e;
      margin-top: 20px;
      font-size: 16pt;
    }}
    ul {{
      margin-left: 20px;
    }}
    .hash {{
      font-size: 10pt;
      margin-top: 30px;
      padding: 10px;
      background-color: #f0f0f0;
      border-left: 5px solid #2c3e50;
    }}
  </style>
</head>
<body>
  <h1>{dados['titulo']}</h1>

  <h2>{dados['identificacao']}</h2>
  <p><strong>Nome:</strong> {dados['nome']}</p>
  <p><strong>Área:</strong> {dados['area']}</p>
  <p><strong>Instituição:</strong> {dados['instituicao']}</p>
  <p><strong>Cidade:</strong> {dados['cidade']}</p>
  <p><strong>Email:</strong> {dados['email']}</p>
  <p><strong>WhatsApp:</strong> {dados['whatsapp']}</p>

  <h2>📌 Detalhes da Pesquisa</h2>
  <p><strong>Título da Pesquisa:</strong> {dados['titulo_pesquisa']}</p>
  <p><strong>Responsável:</strong> {dados['responsavel']}</p>
  <p><strong>Instituição Responsável:</strong> {dados['instituicao_responsavel']}</p>
  <p><strong>Projeto:</strong> {dados['projeto']}</p>
  <p><strong>Objetivo:</strong> {dados['objetivo']}</p>

  <h2>📚 Referenciais Utilizados</h2>
  <ul>
    {''.join([f"<li>{item}</li>" for item in dados['referenciais']])}
  </ul>

  <h2>📝 Consentimento</h2>
  <p><strong>Forma:</strong> {dados['forma_consentimento']}</p>
  <p><strong>Participação:</strong> {dados['participacao']}</p>
  <p><strong>Privacidade:</strong> {dados['privacidade']}</p>

  <h2>📬 Contato</h2>
  <p><strong>Email:</strong> {dados['contato']['email']}</p>
  <p><strong>Telefone:</strong> {dados['contato']['telefone']}</p>

  <div class="hash">
    <strong>🔏 Assinatura digital (HASH):</strong><br>
    {hash_gerado}
  </div>
</body>
</html>
"""

# Gerar e salvar PDF
HTML(string=html).write_pdf("/home/neirivon/Downloads/TCLE_Yasmin_Profissional_HASH.pdf")
print("✅ PDF salvo em /home/neirivon/Downloads/TCLE_Yasmin_Profissional_HASH.pdf")

