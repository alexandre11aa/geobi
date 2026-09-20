# GeoBi

Ferramenta para cálculo áreas de contribuição de sistemas de drenagem urbana através do método das bissetrizes.

Na pasta *script* estão presentes os códigos em Python da ferramenta executável GeoBi que funciona de forma independente. Já na pasta *plugin* estão presentes os arquivos que vão dentro do ZIP usados para instalar o GeoBi diretamente no QGIS (versões 3.28.10 a 3.44.14). O único arquivo que não está presente é o *GeoBi.exe* devido ao limite de memória para arquivos no repositório. De qualquer forma, o executável funciona de maneira indepentente do QGIS (versões 3.28.10 a 3.44.14), e o plug-in dentro do programa é usado apenas para aciona-lo. Essa abordagem foi escolhida no lugar de compilar os códigos diretamente no plug-in, devido à ferramente GeoBi fazer modificações diretamente nos arquivos de extensão SHP, que é usada em multiplas plataformas além do QGIS (versões 3.28.10 a 3.44.14).

# Anexos

Para baixar a extensão no formato ZIP para instalar no QGIS (versões 3.28.10 a 3.44.14) acesse: 

https://drive.google.com/file/d/1g5TBm9Ge2fF093MvP3_IXKj-NfwNBPmV/view

Para baixar o executável que funciona de forma independente acesse: 

https://drive.google.com/file/d/1u27JoaQfPNegLFrA835CD1J1uIiTV3E4/view

Para ler o artigo científico desenvolvido para a ferramenta acesse:

https://editora.unifip.edu.br/index.php/coopex/article/view/551

# Requirements (.exe)

Python 3.11.0

Instalação: `pip install -r requirements.txt`

altgraph                 0.17.5  
certifi                  2026.7.22  
geopandas                1.0.1  
mpmath                   1.3.0  
numpy                    2.1.3  
packaging                26.3  
pandas                   2.2.3  
pefile                   2024.8.26  
pillow                   12.3.0  
pyinstaller              6.22.3  
pyinstaller-hooks-contrib 2026.7  
pyogrio                  0.11.0  
pyproj                   3.7.1  
PyQt5                    5.15.11  
PyQt5-Qt5                5.15.2  
PyQt5_sip                12.19.0  
python-dateutil          2.9.0.post0  
pytz                     2026.3.post1  
pywin32-ctypes           0.2.3  
scipy                    1.15.3  
shapely                  2.1.0  
six                      1.17.0  
sympy                    1.14.0  
tzdata                   2026.4  

Sistema operacional: Windows

# Gerando o executável (.exe)

Na pasta *script*, com o ambiente virtual ativo:

```
pyinstaller --onefile --noconsole --clean --name GeoBi --icon ..\plugin\icone_de_mdb.png --distpath ..\plugin --collect-all pyogrio --collect-all pyproj --collect-all shapely --collect-all geopandas interface_grafica_mdb.pyw
```

O *GeoBi.exe* é gerado diretamente na pasta *plugin*.
