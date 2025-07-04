import pymongo
from datetime import datetime
from pathlib import Path

# Conectar ao MongoDB dockerizado
client = pymongo.MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacao_rar_sinapse_ia"]

# Buscar todas as avaliações existentes
avaliacoes = list(colecao.find({}))

# Criar diretório de saída
output_dir = Path("avaliacoes_ia")
output_dir.mkdir(parents=True, exist_ok=True)

# Gerar um prompt base para análise com IA
def gerar_prompt_ia(avaliacao):
    prompt = f"""
Você é uma IA educacional treinada para analisar avaliações de rubricas pedagógicas. Avalie a seguinte entrada e gere sugestões para melhorar a nota atribuída pelos juízes, se a nota for menor que 4. Seja propositivo e com linguagem didática.

🧑 Juiz Avaliador: {avaliacao.get("juiz_avaliador")}
📧 Email: {avaliacao.get("email_do_juiz_avaliador")}
📚 Dimensão Avaliada: {avaliacao.get("dimensao_avaliada")}

🎯 Notas atribuídas:
- Clareza e Objetividade: {avaliacao.get("clareza_e_objetividade")}
- Coerência entre Descritores: {avaliacao.get("coerencia_entre_descritores")}
- Adequação à Prática Pedagógica: {avaliacao.get("adequacao_a_pratica_pedagogica")}
- Alinhamento com Entidades Normativas e Avaliativas: {avaliacao.get("alinhamento_entidades_normativas_e_avaliativas")}
- Originalidade e Contribuição: {avaliacao.get("originalidade_e_contribuicao")}

💬 Comentário do Juiz:
{avaliacao.get("comentario")}

✅ Sua tarefa:
1. Gere uma análise textual da coerência entre as notas e o comentário do juiz.
2. Para cada critério com nota menor que 4, sugira uma reformulação do texto do descritor correspondente que possa elevar a nota.
3. Use uma linguagem pedagógica acessível e argumente por que a mudança pode melhorar a dimensão avaliada.
"""
    return prompt.strip()

# Salvar prompts em arquivos individuais
for i, avaliacao in enumerate(avaliacoes, 1):
    prompt = gerar_prompt_ia(avaliacao)
    with open(output_dir / f"prompt_ia_dimensao_{i:02}.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

print(f"✅ {len(avaliacoes)} arquivos gerados na pasta 'avaliacoes_ia'")
client.close()
