#!/bin/bash
echo "🔧 Criando ambiente virtual..."
python3 -m venv venv_pisa
source venv_pisa/bin/activate

echo "⬇ Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Ambiente configurado. Execute com: streamlit run Home.py"