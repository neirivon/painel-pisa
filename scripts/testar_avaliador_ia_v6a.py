# Script de teste para avaliar_resposta_sinapse com rubrica v6a
from painel_pisa.utils.avaliador_ia import avaliar_resposta_sinapse

# Resposta de exemplo simulada
resposta = """
A água do rio Paranaíba está muito poluída por conta dos resíduos jogados por indústrias e pelo esgoto doméstico sem tratamento.
A escola da minha cidade desenvolveu um projeto chamado Guardiões da Bacia, envolvendo alunos e moradores na limpeza e monitoramento do rio.
Utilizamos gráficos para mostrar os resultados e tivemos apoio da prefeitura com mutirões.
"""

avaliacao, media, perfil = avaliar_resposta_sinapse(resposta)

print("=== Avaliação por Dimensão ===")
for dim, info in avaliacao.items():
    print(f"[{dim}] Nível {info['nivel']} — {info['titulo']}")
    print(f"→ {info['descricao']}")
    print(f"✔ Similaridade: {info['similaridade']}")
    print("")

print("=== Perfil Final ===")
print(f"Média: {media}os.path.join( , " ")5.0")
print(f"Classificação: {perfil['classificacao']}")
print(f"Sugestão: {perfil['sugestao']}")
