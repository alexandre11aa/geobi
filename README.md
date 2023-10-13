# GeoBi

Esta ferramenta foi desenvolvida para cálculo áreas de contribuição do sistema de microdrenagem através método das bissetrizes.

Na pasta SCRIPT estão presentes os códigos em Python da ferramenta executável GeoBi que funciona de forma independente. Já na pasta PLUGIN estão presentes os arquivos que vão dentro do ZIP usados para instalar o GeoBi diretamente no QGIS. O único arquivo que não está presente é o "GeoBi.exe" devido ao limite de memória de arquivos do repositório. De qualquer forma, o executável funciona de maneira indepentente do QGIS, e o plugin dentro do programa é usado apenas para aciona-lo. Essa abordagem foi escolhida no lugar de compilar os códigos diretamente no plugin, devido à ferramente GeoBi fazer modificações diretamente nos arquivos de extensão SHP, que é usada em multiplas plataformas além do QGIS.

Para baixar a extensão no formato ZIP para instalar no QGis acesse: 

https://drive.google.com/file/d/1g5TBm9Ge2fF093MvP3_IXKj-NfwNBPmV/view

Para baixar o executável que funciona de forma independente acesse: 

https://drive.google.com/file/d/1u27JoaQfPNegLFrA835CD1J1uIiTV3E4/view
