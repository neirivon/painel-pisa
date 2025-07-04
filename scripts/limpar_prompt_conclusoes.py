import json
from pathlib import Path

# Caminho absoluto do JSON da conclusão do PISA
CAMINHO_JSON = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/conclusao_pisa_ocde.json"

def limpar_prompt_do_arquivo(caminho):
    try:
        conteudo = json.loads(Path(caminho).read_text(encoding="utf-8"))

        # Caso o conteúdo seja uma lista com dicionário(s)
        if isinstance(conteudo, list):
            for item in conteudo:
                item.pop("Prompt", None)
        elif isinstance(conteudo, dict):
            conteudo.pop("Prompt", None)

        Path(caminho).write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ Campo 'Prompt' removido com sucesso de: {caminho}")
    except Exception as e:
        print(f"❌ Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    limpar_prompt_do_arquivo(CAMINHO_JSON)

