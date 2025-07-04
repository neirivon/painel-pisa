# utilos.path.join(s, "l")oader_rubricas.py

import os
import json
from utils.config import CONFIG

def carregar_rubricas_bncc_9ano():
    caminho = os.path.join(CONFIG["CAMINHO_DADOS"], "rubricas", "rubricas_bncc_9ano.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

