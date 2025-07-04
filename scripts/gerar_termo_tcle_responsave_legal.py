from pypdf import PdfReader, PdfWriter
from pypdf.generic import AnnotationBuilder
import os

# Caminho completo do arquivo PDF
input_pdf = os.path.expanduser("~/SINAPSE2.0/PISA/TCLE_IFTM_Autorizor_Menor_Idade_Representante_Legal.pdf")
output_pdf = os.path.expanduser("~/SINAPSE2.0/PISA/TCLE_IFTM_Editavel_Com_Campos.pdf")

# Verifica se o arquivo existe
if not os.path.exists(input_pdf):
    raise FileNotFoundError(f"Arquivo não encontrado: {input_pdf}")

# Ler o PDF original
reader = PdfReader(input_pdf)
writer = PdfWriter()

# Copiar todas as páginas para o writer
pages = reader.pages

# Supondo que o conteúdo esteja na última página
page = pages[-1]

# Definir coordenadas aproximadas para os campos (ajustar conforme necessário)
fields_info = [
    {"name": "nome_responsavel", "rect": [80, 700, 400, 715], "label": "Nome do Responsável"},
    {"name": "cpf_responsavel", "rect": [100, 680, 300, 695], "label": "CPF do Responsável"},
    {"name": "nome_aluno", "rect": [110, 640, 400, 655], "label": "Nome do Aluno/Dependente"},
    {"name": "local", "rect": [80, 590, 200, 605], "label": "Local"},
    {"name": "data", "rect": [300, 590, 380, 605], "label": "Data (dd/mm/aaaa)"},
]

# Criar campos de formulário
for field in fields_info:
    annotation = AnnotationBuilder.text_field(
        name=field["name"],
        value="",
        rect=field["rect"]
    )
    page.add_annotation(annotation)

# Substituir a última página pela modificada
pages[-1] = page

# Adicionar todas as páginas ao writer
for p in pages:
    writer.add_page(p)

# Salvar o novo PDF com campos editáveis
with open(output_pdf, "wb") as fp:
    writer.write(fp)

print(f"\n✅ PDF editável salvo com sucesso em:\n{output_pdf}")
print("\nCampos adicionados:")
for f in fields_info:
    print(f"- Campo '{f['name']}' na posição {f['rect']}")
