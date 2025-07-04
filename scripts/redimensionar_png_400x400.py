from PIL import Image
import numpy as np

def remover_fundo(imagem_rgba, tolerancia=40):
    # Converte imagem para numpy array
    data = np.array(imagem_rgba)
    
    # Estima a cor de fundo pelo pixel superior esquerdo
    fundo = data[0, 0, :3]
    
    # Cria máscara onde a diferença de cor é pequena (considerado fundo)
    diff = np.abs(data[:, :, :3] - fundo)
    mascara_fundo = np.all(diff <= tolerancia, axis=-1)

    # Torna pixels do fundo totalmente transparentes
    data[mascara_fundo, 3] = 0

    # Cria imagem com fundo removido
    return Image.fromarray(data)

def redimensionar_com_transparencia(input_path, output_path, tamanho=(400, 400)):
    # Abre imagem como RGBA (com transparência)
    imagem = Image.open(input_path).convert("RGBA")

    # Remove o fundo automaticamente
    imagem_sem_fundo = remover_fundo(imagem)

    # Redimensiona proporcionalmente
    imagem_sem_fundo.thumbnail(tamanho, Image.Resampling.LANCZOS)

    # Cria novo canvas transparente 400x400
    canvas = Image.new("RGBA", tamanho, (0, 0, 0, 0))

    # Centraliza a imagem
    pos_x = (tamanho[0] - imagem_sem_fundo.width) // 2
    pos_y = (tamanho[1] - imagem_sem_fundo.height) // 2
    canvas.paste(imagem_sem_fundo, (pos_x, pos_y), imagem_sem_fundo)

    # Salva como PNG com transparência
    canvas.save(output_path, format="PNG")
    print(f"✅ Imagem salva com fundo transparente: {output_path}")

# 🖼️ Caminhos locais
entrada = "/home/neirivon/Imagens/neirivon_redimensionar.png"
saida = "/home/neirivon/Imagens/neirivon_400x400_transparente.png"

# 🚀 Executa
redimensionar_com_transparencia(entrada, saida)

