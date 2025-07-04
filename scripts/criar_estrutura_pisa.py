import os

base_path = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISA"))
folders = [
    "ineos.path.join(p, "2")000", "ineos.path.join(p, "2")003", "ineos.path.join(p, "2")006", "ineos.path.join(p, "2")009",
    "ineos.path.join(p, "2")012", "ineos.path.join(p, "2")015", "ineos.path.join(p, "2")018", "ineos.path.join(p, "2")022",
    "ocdos.path.join(e, "j")son", "ocdos.path.join(e, "c")sv", "scripts"
]

for folder in folders:
    full_path = os.path.join(base_path, folder)
    os.makedirs(full_path, exist_ok=True)
    print(f"📁 Criado: {full_path}")

print("\n✅ Estrutura de diretórios PISA criada com sucesso!")

