import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho para o CSV
csv_path = 'dados_processados/comparacao_humano_ia.csv'

# Carregar dados
df = pd.read_csv(csv_path)

# Configurações visuais
plt.figure(figsize=(12, 6))
bar_width = 0.35
indices = range(len(df))

# Gráfico de barras
plt.bar(indices, df['nota_humana'], width=bar_width, label='Nota Humana', alpha=0.8)
plt.bar([i + bar_width for i in indices], df['nota_ia'], width=bar_width, label='Nota IA', alpha=0.8)

# Rótulos e título
plt.xlabel('Dimensão')
plt.ylabel('Nota Média')
plt.title('Comparação de Notas Médias: Humanos vs IA')
plt.xticks([i + bar_width / 2 for i in indices], df['dimensao'], rotation=45, ha='right')
plt.ylim(0, 5)
plt.legend()

# Grid e layout
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Salvar imagem
plt.savefig('dados_processados/grafico_comparativo_ia_vs_humanos.png', dpi=300)
plt.show()

