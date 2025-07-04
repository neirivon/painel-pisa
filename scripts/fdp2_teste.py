from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=14)
pdf.cell(0, 10, txt="✅ Teste bem-sucedido com emojis e UTF-8: π, √, Ω, 🎓, 📚, ✨", ln=True)

pdf.output("/home/neirivon/SINAPSE2.0/PISA/painel_pisa/pdfs_correcoes/teste_fpdf2_unicode.pdf")
print("✅ PDF gerado com sucesso!")
