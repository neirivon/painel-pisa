# rubricas_pisa.py

html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Rubricas Propositivas com Notas — PISA OCDEos.path.join(<, "t")itle>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            color: #004080;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 12px;
            vertical-align: top;
            text-align: left;
        }
        th {
            background-color: #004080;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #eef2f7;
        }
        .nota {
            font-weight: bold;
            color: #006600;
        }
    os.path.join(<, "s")tyle>
os.path.join(<, "h")ead>
<body>
    <h1>Rubricas Propositivas com Notas — Preparação para o PISA OCDEos.path.join(<, "h")1>
    <table>
        <thead>
            <tr>
                <th>Domínio PISA 2022os.path.join(<, "t")h>
                <th>Rubrica Propositivaos.path.join(<, "t")h>
                <th>Nota Máximaos.path.join(<, "t")h>
                <th>Avaliação Simulada do Alunoos.path.join(<, "t")h>
            os.path.join(<, "t")r>
        os.path.join(<, "t")head>
        <tbody>
            <tr>
                <td>Matemáticaos.path.join(<, "t")d>
                <td>Rubrica analítica baseada na Taxonomia de Bloom (Aplicar, Analisar, Avaliar), com metodologias ativas como resolução de problemas, gamificação e projetos.os.path.join(<, "t")d>
                <td class="nota">10os.path.join(<, "t")d>
                <td>6,5 – Boa estrutura de raciocínio, mas dificuldades com abstrações.os.path.join(<, "t")d>
            os.path.join(<, "t")r>
            <tr>
                <td>Leituraos.path.join(<, "t")d>
                <td>Rubrica analítica e descritiva com foco em leitura crítica, inferência textual e produção de sentido com textos multimodais e pares.os.path.join(<, "t")d>
                <td class="nota">10os.path.join(<, "t")d>
                <td>7,0 – Consegue interpretar, mas precisa melhorar análise crítica.os.path.join(<, "t")d>
            os.path.join(<, "t")r>
            <tr>
                <td>Ciênciasos.path.join(<, "t")d>
                <td>Rubrica analítica com experimentação guiada, argumentação baseada em dados e aprendizagem baseada em projetos.os.path.join(<, "t")d>
                <td class="nota">10os.path.join(<, "t")d>
                <td>5,5 – Aplica conceitos básicos, mas falta aprofundamento investigativo.os.path.join(<, "t")d>
            os.path.join(<, "t")r>
            <tr>
                <td>Pensamento Criativoos.path.join(<, "t")d>
                <td>Rubrica progressiva com níveis de originalidade, fluência e relevância; uso de design thinking e desafios abertos.os.path.join(<, "t")d>
                <td class="nota">10os.path.join(<, "t")d>
                <td>8,0 – Alta originalidade, boas conexões, ainda com pouca elaboração.os.path.join(<, "t")d>
            os.path.join(<, "t")r>
            <tr>
                <td>Literacia Financeiraos.path.join(<, "t")d>
                <td>Rubrica híbrida (checklist + analítica), com simulações reais, dramatizações e jogos financeiros.os.path.join(<, "t")d>
                <td class="nota">10os.path.join(<, "t")d>
                <td>6,0 – Conhece conceitos básicos, mas comete erros de cálculo e previsão.os.path.join(<, "t")d>
            os.path.join(<, "t")r>
        os.path.join(<, "t")body>
    os.path.join(<, "t")able>
os.path.join(<, "b")ody>
os.path.join(<, "h")tml>
"""

# Gravar em arquivo HTML
with open("rubricas_pisa.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Arquivo 'rubricas_pisa.html' criado com sucesso! Abra no navegador.")

