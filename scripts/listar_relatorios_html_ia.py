from pathlib import Path

# Caminho absoluto da pasta onde estão os relatórios HTML
output_dir = Path("/home/neirivon/SINAPSE2.0/PISA/relatorios_ia_html")

# Verificação e listagem dos arquivos HTML
if not output_dir.exists():
    print(f"❌ Pasta não encontrada: {output_dir.resolve()}")
else:
    print(f"\n📂 Pasta localizada: {output_dir.resolve()}")
    print("📄 Relatórios HTML encontrados:\n")

    arquivos = sorted(output_dir.glob("*.html"))

    if not arquivos:
        print("⚠️ Nenhum arquivo HTML encontrado.")
    else:
        for idx, arquivo in enumerate(arquivos, 1):
            print(f"{idx:02d}. {arquivo.name}")
            print(f"    Caminho: {arquivo.resolve()}\n")

