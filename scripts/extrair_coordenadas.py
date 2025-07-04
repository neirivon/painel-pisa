import pdfplumber
import os

# Caminho completo do arquivo PDF
input_pdf = os.path.expanduser("~/SINAPSE2.0/PISA/TCLE_IFTM_Autorizor_Menor_Idade_Representante_Legal.pdf")

# Verifica se o arquivo existe
if not os.path.exists(input_pdf):
    raise FileNotFoundError(f"Arquivo não encontrado: {input_pdf}")

print("🔍 Iniciando extração das coordenadas dos traços...\n")


# Função para detectar traços e suas coordenadas com segurança
def extrair_coordenadas_tracos(pdf_path):
    tracos_encontrados = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extrair palavras com coordenadas (se disponíveis)
            try:
                words = page.extract_words()
            except Exception as e:
                print(f"⚠️ Erro ao extrair palavras da página {page_num + 1}: {e}")
                continue

            for word_info in words:
                # Garantir que 'text' exista
                if "text" not in word_info:
                    continue

                text = word_info["text"]

                # Procurar traços longos (apenas sublinhados)
                if len(text) >= 5 and set(text) == {"_"}:
                    # Garantir que as coordenadas existam
                    if all(k in word_info for k in ["x0", "top", "x1", "bottom"]):
                        x0, top, x1, bottom = word_info["x0"], word_info["top"], word_info["x1"], word_info["bottom"]
                        width = x1 - x0
                        height = bottom - top
                        tracos_encontrados.append({
                            "pagina": page_num + 1,
                            "texto": text,
                            "x0": x0,
                            "top": top,
                            "x1": x1,
                            "bottom": bottom,
                            "width": width,
                            "height": height
                        })
    return tracos_encontrados


# Executar a função
try:
    coordenadas = extrair_coordenadas_tracos(input_pdf)

    if len(coordenadas) == 0:
        print("⚠️ Nenhum traço foi encontrado no PDF.")
    else:
        print(f"✅ Foram encontrados {len(coordenadas)} traços no PDF:\n")
        for idx, t in enumerate(coordenadas):
            print(f"Campo {idx + 1}:")
            print(f"  Página: {t['pagina']}")
            print(f"  Texto identificado: '{t['texto']}'")
            print(f"  Coordenadas: x0={t['x0']}, top={t['top']}, x1={t['x1']}, bottom={t['bottom']}")
            print(f"  Tamanho: {t['width']}x{t['height']}\n")

except Exception as e:
    print(f"❌ Erro ao processar o PDF: {e}")
