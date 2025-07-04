# scripts/sobrescrever_rubrica_sinapse_ia_v1_2.py

import json
from datetime import datetime
import os

rubrica = {
    "nome": "rubrica_sinapse_ia",
    "versao": "v1.2",
    "base": "SAEB 2017",
    "modelo": "LLaMA3 8B (Ollama)",
    "timestamp": datetime.now().isoformat(),
    "dimensoes": [
        {
            "dimensao": "Progressão Cognitiva Educacional",
            "origem": "SAEB 2017",
            "finalidade": "Construção de descritores pedagógicos contextualizados via IA",
            "niveis": [
                {
                    "nota": 1,
                    "nome": "Reconhecimento (1)",
                    "descricao": "O aluno reconhece e reproduz informações previamente aprendidas.",
                    "exemplos": [
                        "Identifica e classifica cores em uma pintura escolar.",
                        "Recita as letras do alfabeto na ordem correta.",
                        "Reconhece e escreve os números de 1 a 10."
                    ]
                },
                {
                    "nota": 2,
                    "nome": "Compreensão (2)",
                    "descricao": "O aluno compreende o sentido geral da informação e pode relacionar ideias.",
                    "exemplos": [
                        "Analisa e interpreta imagens da vida cotidiana.",
                        "Compreende o conteúdo de um texto simples sobre história do Brasil.",
                        "Interpreta gráficos sobre crescimento vegetal."
                    ]
                },
                {
                    "nota": 3,
                    "nome": "Análise (3)",
                    "descricao": "O aluno analisa as relações entre ideias e identifica padrões.",
                    "exemplos": [
                        "Avalia informações em texto sobre economia brasileira.",
                        "Analisa causas e consequências do desmatamento na Amazônia.",
                        "Interpreta dados sobre a população brasileira."
                    ]
                },
                {
                    "nota": 4,
                    "nome": "Síntese (4)",
                    "descricao": "O aluno sintetiza conhecimentos e propõe soluções inovadoras.",
                    "exemplos": [
                        "Desenvolve plano de conservação da água na escola.",
                        "Resolve problema real sobre segurança no bairro.",
                        "Elabora relatório sobre uso de energias renováveis."
                    ]
                }
            ]
        },
        {
            "dimensao": "Perfil Socioeconômico e Contextual",
            "origem": "SAEB 2017",
            "finalidade": "Construção de descritores pedagógicos contextualizados via IA",
            "niveis": [
                {
                    "nota": 1,
                    "nome": "Nível Inicial (1)",
                    "descricao": "Situação socioeconômica com restrições severas de acesso a recursos e serviços.",
                    "exemplos": [
                        "Aluna que vive em favela com acesso limitado a serviços básicos.",
                        "Aluno que mora em cidade pequena com pais trabalhadores braçais.",
                        "Turma em situação de vulnerabilidade social extrema."
                    ]
                },
                {
                    "nota": 2,
                    "nome": "Nível Básico (2)",
                    "descricao": "Condições modestas com acesso limitado a recursos escolares e culturais.",
                    "exemplos": [
                        "Aluno de escola pública em bairro periférico com infraestrutura precária.",
                        "Família mora em casa alugada com irmãos e renda informal.",
                        "Turma com acesso irregular à internet e bibliotecas."
                    ]
                },
                {
                    "nota": 3,
                    "nome": "Nível Médio (3)",
                    "descricao": "Condições razoáveis com presença de estabilidade básica e recursos moderados.",
                    "exemplos": [
                        "Aluno vive em casa própria e pais com empregos formais.",
                        "Escola pública com estrutura física adequada e biblioteca.",
                        "Turma com acesso a internet e participação em projetos escolares."
                    ]
                },
                {
                    "nota": 4,
                    "nome": "Nível Avançado (4)",
                    "descricao": "Alta estabilidade socioeconômica com acesso pleno a recursos culturais e educacionais.",
                    "exemplos": [
                        "Aluno mora em residência ampla com pais profissionais liberais.",
                        "Escola pública em centro urbano com laboratórios e atividades extracurriculares.",
                        "Turma com acesso a tecnologia educacional avançada."
                    ]
                }
            ]
        }
    ]
}

# Criar diretório se não existir
output_path = "dados_processados/bncc"
os.makedirs(output_path, exist_ok=True)

# Caminho do arquivo
arquivo_json = os.path.join(output_path, "rubrica_sinapse_ia_v1_2.json")

# Salvar JSON
with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

print(f"✅ Rubrica v1.2 sobrescrita com sucesso em: {arquivo_json}")

