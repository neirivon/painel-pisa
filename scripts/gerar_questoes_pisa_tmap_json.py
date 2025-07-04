import json
import os
from datetime import datetime

# Caminho absoluto de saída
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

questoes_tmap = {
    "versao": "1.0",
    "ano_referencia": 2022,
    "contexto": "PISA OCDE adaptado ao TMAP",
    "gerado_em": datetime.now().isoformat(),
    "questoes": [
        {
            "id": "matematica_001",
            "disciplina": "Matemática",
            "enunciado": "Uma fazenda no Triângulo Mineiro tem um reservatório de água com formato cilíndrico. Ele tem 2 metros de raio e 3 metros de altura. Quantos litros de água cabem nesse reservatório? (1 m³ = 1000 litros)",
            "resposta_modelo": "Use a fórmula do volume do cilindro: V = πr²h. Assim, V = 3.14 × 2² × 3 = 3.14 × 4 × 3 = 37.68 m³, ou seja, 37.680 litros.",
            "fonte": "PISA 2022 OCDE + adaptação local TMAP"
        },
        {
            "id": "ciencias_001",
            "disciplina": "Ciências",
            "enunciado": "Na zona rural do Alto Paranaíba, produtores notaram mudanças na quantidade de abelhas nos últimos anos. Que fatores ambientais podem estar causando isso? O que pode ser feito para proteger essas espécies?",
            "resposta_modelo": "Uso de agrotóxicos, desmatamento e mudanças climáticas podem afetar as abelhas. Ações como reduzir venenos, plantar flores nativas e conservar matas ajudam na preservação.",
            "fonte": "PISA 2022 OCDE + adaptação local TMAP"
        },
        {
            "id": "leitura_001",
            "disciplina": "Leitura",
            "enunciado": "Leia este trecho de uma crônica mineira: 'Na varanda, o cheiro do café passado no coador de pano acordava até as lembranças.' O que o autor quis dizer com essa frase? Qual o efeito desse tipo de linguagem no leitor?",
            "resposta_modelo": "O autor usa linguagem sensorial e afetiva para evocar memórias do leitor. Isso cria um vínculo emocional e cultural com a cena descrita.",
            "fonte": "PISA 2022 OCDE + adaptação local TMAP"
        }
    ]
}

# Escrita do arquivo
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(questoes_tmap, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo salvo com sucesso em:\n{JSON_PATH}")

