# Script de teste atualizado — avalia uma resposta com a versão final do avaliador IA (sem FAISS)

from painel_pisa.utils.avaliador_ia import avaliar_resposta_sinapse

# Exemplo de resposta dissertativa (adaptada ao Triângulo Mineiro)
resposta = """
Na minha cidade, próximo ao rio Paranaíba, observamos poluição causada por esgoto sem tratamento.
A escola criou o projeto Guardiões do Rio, onde alunos pesquisaram, desenharam cartazes e promoveram mutirões.
Isso envolveu famílias, prefeitura e ONGs locais. Criamos infográficos para mostrar o impacto das ações.
"""

avaliacao, media, perfil = avaliar_resposta_sinapse(resposta)

print("=== Avaliação por Dimensão ===\n")
for dim, info in avaliacao.items():
    print(f"[{dim}] Nível {info['nivel']} — {info['titulo']}")
    print(f"✔ Similaridade: {info['similaridade']}")
    print(f"→ {info['descricao']}\n")

print("=== Perfil Final ===")
print(f"Média geral: {media}os.path.join( , " ")5.0")
print(f"Classificação: {perfil['classificacao']}")
print(f"Sugestão: {perfil['sugestao']}")
