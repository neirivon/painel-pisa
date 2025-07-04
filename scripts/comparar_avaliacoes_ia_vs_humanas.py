import pandas as pd
from pymongo import MongoClient
from pathlib import Path

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
collection = db["avaliacoes_humanas"]

# Carrega os dados da coleção
dados_humanos = list(collection.find({}, {"_id": 0}))  # Ignora o campo _id
df = pd.DataFrame(dados_humanos)

# Fecha a conexão com o banco
client.close()

# Validação e diagnóstico
print("📌 Colunas disponíveis:", list(df.columns))
print("\n📊 Amostra de dados:")
print(df.head())

# Verifica se as colunas esperadas existem
campos_esperados = {"juiz", "dimensao", "nota"}
if not campos_esperados.issubset(df.columns):
    raise ValueError(f"❌ Faltam colunas obrigatórias: {campos_esperados - set(df.columns)}")

# Média das notas humanas por dimensão
media_humanos = df.groupby("dimensao")["nota"].mean().reset_index()
media_humanos.rename(columns={"nota": "nota_humana"}, inplace=True)

# Carrega as notas da IA
caminho_ia = Path("dados_processados/avaliacoes_ia_llama3.json")
if not caminho_ia.exists():
    raise FileNotFoundError(f"❌ Arquivo com avaliações IA não encontrado: {caminho_ia}")

df_ia = pd.read_json(caminho_ia)
df_ia.rename(columns={"nota": "nota_ia"}, inplace=True)

# Merge entre humano e IA
df_comparacao = pd.merge(media_humanos, df_ia, on="dimensao", how="inner")
df_comparacao["diferenca"] = df_comparacao["nota_ia"] - df_comparacao["nota_humana"]

# Exibe o resultado final
print("\n✅ Comparação entre notas médias humanas e IA:")
print(df_comparacao.sort_values("dimensao"))

# Salva o resultado
output_path = Path("dados_processados/comparacao_humano_ia.csv")
df_comparacao.to_csv(output_path, index=False)
print(f"\n📁 Resultado salvo em: {output_path.resolve()}")

