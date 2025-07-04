from gtts import gTTS
from docx import Document

# Caminho do arquivo DOCX da rubrica
caminho_arquivo = "/home/neirivon/Downloads/Rubrica_SINAPSE_IA_v4_COMPLETA_8_DIMENSOES (2).docx"

# Carregar o texto do documento
documento = Document(caminho_arquivo)
texto_completo = "\n".join([paragrafo.text for paragrafo in documento.paragraphs if paragrafo.text.strip() != ""])

# Configurar o TTS com voz feminina educacional (gTTS usa voz do Google padrão)
tts = gTTS(text=texto_completo, lang='pt-br', slow=False)

# Salvar o arquivo de áudio
nome_arquivo_audio = "/home/neirivon/Downloads/rubrica_sinapse_audio.mp3"
tts.save(nome_arquivo_audio)

print(f"✅ Áudio salvo com sucesso como: {nome_arquivo_audio}")

