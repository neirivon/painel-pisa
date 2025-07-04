import re
from bs4 import BeautifulSoup

def validar_html_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        conteudo = file.read()

    soup = BeautifulSoup(conteudo, 'html.parser')
    linhas = conteudo.splitlines()

    erros = []

    # 1. Verificar se as tags principais existem
    for tag in ['html', 'head', 'body']:
        if not soup.find(tag):
            erros.append(f"❌ Tag <{tag}> ausente. ➤ Verifique se a estrutura básica HTML está completa.")

    # 2. Verificar duplicação de funções JS
    funcoes = re.findall(r'function\s+(\w+)\s*\(', conteudo)
    duplicadas = set([f for f in funcoes if funcoes.count(f) > 1])
    if duplicadas:
        for nome in duplicadas:
            linhas_ocorrencia = [i + 1 for i, l in enumerate(linhas) if f"function {nome}(" in l]
            erros.append(f"❌ Função duplicada: '{nome}' nas linhas {linhas_ocorrencia}. ➤ Sugestão: consolidar em uma única função.")

    # 3. Verificar elementos HTML inexistentes usados por JS
    ids_usados = re.findall(r'document\.getElementById\(\"(.*?)\"\)', conteudo)
    ids_existentes = [tag.get('id') for tag in soup.find_all(attrs={'id': True})]
    for id_ in ids_usados:
        if id_ not in ids_existentes:
            erros.append(f"⚠️ Elemento com id '{id_}' usado em JS mas não existe no HTML. ➤ Verifique se o elemento foi removido ou renomeado.")

    # 4. Verificar presença de bibliotecas esperadas (jsPDF, html2canvas)
    if 'jspdf' not in conteudo.lower():
        erros.append("⚠️ Biblioteca jsPDF não parece estar carregada. ➤ Adicione o script: https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js")
    if 'html2canvas' not in conteudo.lower():
        erros.append("⚠️ Biblioteca html2canvas não parece estar carregada. ➤ Adicione o script: https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js")

    # 5. Verificar onclick sem função correspondente
    onclicks = re.findall(r'onclick=\"(\w+)\(\)\"', conteudo)
    for func in onclicks:
        if func not in funcoes:
            erros.append(f"⚠️ Botão chama função '{func}()' que não foi definida. ➤ Revise o nome da função ou inclua a definição.")

    # Salvar log em arquivo
    with open('log_validador.txt', 'w', encoding='utf-8') as log_file:
        if not erros:
            log_file.write("✅ Nenhum problema detectado. HTML e JavaScript parecem corretos.\n")
            print("✅ Nenhum problema detectado.")
        else:
            for erro in erros:
                log_file.write(erro + '\n')
            print("⚠️ Problemas encontrados. Verifique o arquivo 'log_validador.txt'.")

# Exemplo de uso:
validar_html_js('/home/neirivon/Downloads/avaliacao_juiz_dirceu_duarte_de_progressao_cognitiva_emocional_FINAL_CORRIGIDO_com_PDF_funcional.html')

