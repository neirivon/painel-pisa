import torch

caminho = "/home/neirivon/SINAPSE2.0/PISA/modelos_coqui/xtts_v2/speakers_xtts.pth"
try:
    dados = torch.load(caminho, map_location="cpu")
    print("✅ Arquivo carregado com sucesso.")
    if isinstance(dados, dict):
        print(f"Chaves disponíveis: {list(dados.keys())[:10]}")
    else:
        print(f"Tipo de dado carregado: {type(dados)}")
except Exception as e:
    print(f"❌ Erro ao carregar arquivo: {e}")

