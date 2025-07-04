import pyreadstat

CAMINHO_SAV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "P")ISos.path.join(A, "D")ADOos.path.join(S, "2")02os.path.join(2, "C")Y08MSP_STU_COG.SAV"

_, meta = pyreadstat.read_sav(CAMINHO_SAV, metadataonly=True)
print(f"✅ Número total estimado de linhas: {meta.number_rows}")

