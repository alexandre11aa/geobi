# GeoBi

Ferramenta para cálculo áreas de contribuição de sistemas de drenagem urbana através do método das bissetrizes.

Na pasta SCRIPT estão presentes os códigos em Python da ferramenta executável GeoBi que funciona de forma independente. Já na pasta PLUGIN estão presentes os arquivos que vão dentro do ZIP usados para instalar o GeoBi diretamente no QGIS. O único arquivo que não está presente é o *GeoBi.exe* devido ao limite de memória para arquivos no repositório. De qualquer forma, o executável funciona de maneira indepentente do QGIS, e o plugin dentro do programa é usado apenas para aciona-lo. Essa abordagem foi escolhida no lugar de compilar os códigos diretamente no plugin, devido à ferramente GeoBi fazer modificações diretamente nos arquivos de extensão SHP, que é usada em multiplas plataformas além do QGIS.

# Anexos

Para baixar a extensão no formato ZIP para instalar no QGIS acesse: 

https://drive.google.com/file/d/1g5TBm9Ge2fF093MvP3_IXKj-NfwNBPmV/view

Para baixar o executável que funciona de forma independente acesse: 

https://drive.google.com/file/d/1u27JoaQfPNegLFrA835CD1J1uIiTV3E4/view

Para ler o artigo científico desenvolvido para a ferramenta acesse:

https://coopex.unifip.edu.br/index.php/coopex/article/view/551

# Requirements (.exe)

attrs           23.2.0  
certifi         2023.11.17  
click           8.1.7  
click-plugins   1.1.1  
cligj           0.7.2  
colorama        0.4.6  
fiona           1.9.5  
geopandas       0.14.2  
mpmath          1.3.0  
numpy           1.26.3  
packaging       23.2  
pandas          2.2.0  
pip             23.2.1  
pyproj          3.6.1  
PyQt5           5.15.10  
PyQt5-Qt5       5.15.2  
PyQt5-sip       12.13.0  
python-dateutil 2.8.2  
pytz            2023.3.post1  
scipy           1.12.0  
setuptools      69.0.3  
shapely         2.0.2  
six             1.16.0  
sympy           1.12  
tzdata          2023.4  
