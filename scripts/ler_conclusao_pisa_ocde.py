import json
from pathlib import Path

CAMINHO_CONCLUSAO = "painel_pisa/dados_cloud/conclusao_pisa_ocde.json"

def ler_conclusao():
    caminho = Path(CAMINHO_CONCLUSAO)
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {CAMINHO_CONCLUSAO}")
        return
    
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    if not dados:
        print("⚠️ Arquivo está vazio.")
        return

    print("\n📘 Conclusão Pedagógica do Brasil no PISA 2022:")
    for item in dados:
        ano = item.get("Ano", "Desconhecido")
        conclusao = item.get("Conclusao", "[Sem texto]")
        print(f"\n🗓️ Ano: {ano}\n\n📜 Texto:\n{conclusao}\n")

if __name__ == "__main__":
    ler_conclusao()

