from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import json
import csv
from datetime import datetime
from pymongo import MongoClient

PASTA_SAIDA = "dados_processadoos.path.join(s, "b")ncc"
JSON_SAIDA = os.path.join(PASTA_SAIDA, "habilidades_bncc_9ano_matematica.json")
CSV_SAIDA = os.path.join(PASTA_SAIDA, "habilidades_bncc_9ano_matematica.csv")

habilidades_bncc = [
    ("EF09MA01", "Reconhecer que, uma vez fixada uma unidade de comprimento, existem segmentos de reta cujo comprimento não é expresso por número racional (como as medidas de diagonais de um polígono e alturas de um triângulo, quando se toma a medida de cada lado como unidade)."),
    ("EF09MA02", "Reconhecer um número irracional como um número real cuja representação decimal é infinita e não periódica, e estimar a localização de alguns deles na reta numérica."),
    ("EF09MA03", "Efetuar cálculos com números reais, inclusive potências com expoentes fracionários."),
    ("EF09MA04", "Resolver e elaborar problemas com números reais, inclusive em notação científica, envolvendo diferentes operações."),
    ("EF09MA05", "Resolver e elaborar problemas que envolvam porcentagens, com a ideia de aplicação de percentuais sucessivos e a determinação das taxas percentuais, preferencialmente com o uso de tecnologias digitais, no contexto da educação financeira."),
    ("EF09MA06", "Compreender as funções como relações de dependência unívoca entre duas variáveis e suas representações numérica, algébrica e gráfica e utilizar esse conceito para analisar situações que envolvam relações funcionais entre duas variáveis."),
    ("EF09MA07", "Resolver problemas que envolvam a razão entre duas grandezas de espécies diferentes, como velocidade e densidade demográfica."),
    ("EF09MA08", "Resolver e elaborar problemas que envolvam relações de proporcionalidade direta e inversa entre duas ou mais grandezas, inclusive escalas, divisão em partes proporcionais e taxa de variação, em contextos socioculturais, ambientais e de outras áreas."),
    ("EF09MA09", "Compreender os processos de fatoração de expressões algébricas, com base em suas relações com os produtos notáveis, para resolver e elaborar problemas que possam ser representados por equações polinomiais do 2º grau."),
    ("EF09MA10", "Demonstrar relações simples entre os ângulos formados por retas paralelas cortadas por uma transversal."),
    ("EF09MA11", "Resolver problemas por meio do estabelecimento de relações entre arcos, ângulos centrais e ângulos inscritos na circunferência, fazendo uso, inclusive, de softwares de geometria dinâmica."),
    ("EF09MA12", "Reconhecer as condições necessárias e suficientes para que dois triângulos sejam semelhantes."),
    ("EF09MA13", "Demonstrar relações métricas do triângulo retângulo, entre elas o teorema de Pitágoras, utilizando, inclusive, a semelhança de triângulos."),
    ("EF09MA14", "Resolver e elaborar problemas de aplicação do teorema de Pitágoras ou das relações de proporcionalidade envolvendo retas paralelas cortadas por secantes."),
    ("EF09MA15", "Descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um polígono regular cuja medida do lado é conhecida, utilizando régua e compasso, como também softwares."),
    ("EF09MA16", "Determinar o ponto médio de um segmento de reta e a distância entre dois pontos quaisquer, dadas as coordenadas desses pontos no plano cartesiano, sem o uso de fórmulas, e utilizar esse conhecimento para calcular, por exemplo, medidas de perímetros e áreas de figuras planas construídas no plano."),
    ("EF09MA17", "Reconhecer vistas ortogonais de figuras espaciais e aplicar esse conhecimento para desenhar objetos em perspectiva."),
    ("EF09MA18", "Reconhecer e empregar unidades usadas para expressar medidas muito grandes ou muito pequenas, tais como distância entre planetas e sistemas solares, tamanho de vírus ou de células, capacidade de armazenamento de computadores, entre outros."),
    ("EF09MA19", "Resolver e elaborar problemas que envolvam medidas de volumes de prismas e de cilindros retos, inclusive com uso de expressões de cálculo, em situações cotidianas."),
    ("EF09MA20", "Reconhecer, em experimentos aleatórios, eventos independentes e dependentes e calcular a probabilidade de sua ocorrência, nos dois casos."),
    ("EF09MA21", "Analisar e identificar, em gráficos divulgados pela mídia, os elementos que podem induzir, às vezes propositadamente, erros de leitura, como escalas inapropriadas, legendas não explicitadas corretamente, omissão de informações importantes (fontes e datas), entre outros."),
    ("EF09MA22", "Escolher e construir o gráfico mais adequado (colunas, setores, linhas), com ou sem uso de planilhas eletrônicas, para apresentar um determinado conjunto de dados, destacando aspectos como as medidas de tendência central."),
    ("EF09MA23", "Planejar e executar pesquisa amostral envolvendo tema da realidade social e comunicar os resultados por meio de relatório contendo avaliação de medidas de tendência central e da amplitude, tabelas e gráficos adequados, construídos com o apoio de planilhas eletrônicas."),
]

# Adiciona metadados
habilidades_dicts = [{
    "etapa": "EF - Anos Finais",
    "ano": "9º ano",
    "area": "Matemática",
    "componente": "Matemática",
    "codigo": codigo,
    "habilidade": habilidade,
    "fonte": "BNCC",
    "timestamp_extracao": datetime.utcnow()
} for codigo, habilidade in habilidades_bncc]

# Salva como JSON
os.makedirs(PASTA_SAIDA, exist_ok=True)
with open(JSON_SAIDA, "w", encoding="utf-8") as jf:
    json.dump(
        [{**h, "timestamp_extracao": h["timestamp_extracao"].isoformat()} for h in habilidades_dicts],
        jf, ensure_ascii=False, indent=2
    )
print(f"💾 JSON salvo em: {JSON_SAIDA}")

# Salva como CSV
with open(CSV_SAIDA, "w", encoding="utf-8", newline="") as cf:
    writer = csv.DictWriter(cf, fieldnames=["codigo", "habilidade", "etapa", "ano", "area", "componente", "fonte"])
    writer.writeheader()
    for h in habilidades_dicts:
        writer.writerow({k: h[k] for k in writer.fieldnames})
print(f"💾 CSV salvo em: {CSV_SAIDA}")

# Insere no MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["bncc_9ano"]
resultado = colecao.insert_many(habilidades_dicts)
client.close()
print(f"🌐 Inseridos {len(resultado.inserted_ids)} documentos no MongoDB.")
print("🏁 Fim da execução.")

