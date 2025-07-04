#!/bin/bash

cd ~/SINAPSE2.0/PISA/painel_pisa || exit 1

# Diretórios para microdados do PISA OCDE
mkdir -p dados_pisa_ocde/2000
mkdir -p dados_pisa_ocde/2003
mkdir -p dados_pisa_ocde/2006
mkdir -p dados_pisa_ocde/2009
mkdir -p dados_pisa_ocde/2012
mkdir -p dados_pisa_ocde/2015
mkdir -p dados_pisa_ocde/2018
mkdir -p dados_pisa_ocde/2022

# Diretórios para relatórios do PISA OCDE
mkdir -p relatorios_pisa_ocde/2000
mkdir -p relatorios_pisa_ocde/2003
mkdir -p relatorios_pisa_ocde/2006
mkdir -p relatorios_pisa_ocde/2009
mkdir -p relatorios_pisa_ocde/2012
mkdir -p relatorios_pisa_ocde/2015
mkdir -p relatorios_pisa_ocde/2018
mkdir -p relatorios_pisa_ocde/2022

# Diretórios para relatórios do INEP (somente relatórios)
mkdir -p relatorios_inep/2000
mkdir -p relatorios_inep/2003
mkdir -p relatorios_inep/2006
mkdir -p relatorios_inep/2009
mkdir -p relatorios_inep/2012
mkdir -p relatorios_inep/2015
mkdir -p relatorios_inep/2018
mkdir -p relatorios_inep/2022

# Diretórios para microdados do SAEB (por ciclos)
mkdir -p dados_saeb/1999_2001
mkdir -p dados_saeb/2003
mkdir -p dados_saeb/2005_2007
mkdir -p dados_saeb/2009
mkdir -p dados_saeb/2011_2013
mkdir -p dados_saeb/2015
mkdir -p dados_saeb/2017_2019
mkdir -p dados_saeb/2021_2023

# Diretórios para relatórios do SAEB (também por ciclos)
mkdir -p relatorios_saeb/1999_2001
mkdir -p relatorios_saeb/2003
mkdir -p relatorios_saeb/2005_2007
mkdir -p relatorios_saeb/2009
mkdir -p relatorios_saeb/2011_2013
mkdir -p relatorios_saeb/2015
mkdir -p relatorios_saeb/2017_2019
mkdir -p relatorios_saeb/2021_2023

echo "✅ Estrutura de diretórios criada com sucesso!"

