print("\nPorque para mim o viver é Cristo, e o morrer é ganho. Filipenses 1:21\n")

import sys
import base64
import geopandas as gpd

from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from metodo_das_bissetrizes import mdb_poligonos_internos
from metodo_das_bissetrizes import mdb_poligonos_externos

from imagens_da_interface import imagens

class funcoes():

    # Caminho para arquivos
    def procurando_caminho(self, decisao):

        opcoes = QFileDialog.Options()
        opcoes |= QFileDialog.ReadOnly

        if decisao == 1:
            caminho, _ = QFileDialog.getOpenFileName(self, 'Abrir Arquivo Shapefile', '', 'Arquivos Shapefile (*.shp)', options=opcoes)

        elif decisao == 2:
            caminho, _ = QFileDialog.getSaveFileName(self, 'Salvar Arquivo', '', 'Arquivos Shapefile (*.shp)', options=opcoes)

        return caminho

    # Quantidade de vértices limite para cálculo dos polígonos
    def numero_de_poligonos(self):

        if self.lista_de_lados_do_poligono.currentText() == "Iguais a três vértices":
            self.nmr_de_vertices = 4
            
        elif self.lista_de_lados_do_poligono.currentText() == "Menores ou iguais a quatro vértices":
            self.nmr_de_vertices = 5

        elif self.lista_de_lados_do_poligono.currentText() == "Qualquer número de vértices (*)":
            self.nmr_de_vertices = 1000

    # Polígonos internos
    def calculo_dos_poligonos_internos(self):

        try:
            self.gdf_poligonos = gpd.read_file(self.caminho_do_arquivo_1)

            self.gdf_bissetrizes, self.gdf_areas_1 = mdb_poligonos_internos(self.gdf_poligonos, 
                                                                            self.nmr_de_vertices, 
                                                                            self.gdf_poligonos.crs)

            self.gdf_bissetrizes.to_file(self.caminho_do_arquivo_3)
            self.gdf_areas_1.to_file(self.caminho_do_arquivo_3.replace(".shp", "_areas.shp"))

            QMessageBox.information(self, "   A V I S O !", "Arquivos shapefiles gerados com sucesso!")

        except Exception as e:

            QMessageBox.critical(self, "   E R R O !", "Não foi possível gerar os arquivos shapefile esperados, certifique-se de inserir as informações corretamente!")

            print(e)

    # Polígonos externos
    def calculo_dos_poligonos_externos(self):

        try:

            self.gdf_poligonos = gpd.read_file(self.caminho_do_arquivo_1)

            self.gdf_pontos = gpd.read_file(self.caminho_do_arquivo_2)

            self.gdf_retas, self.gdf_areas_2 = mdb_poligonos_externos(self.gdf_poligonos, 
                                                                    self.gdf_pontos, 
                                                                    self.nmr_de_vertices, 
                                                                    self.gdf_pontos.crs)

            self.gdf_retas.to_file(self.caminho_do_arquivo_4)
            self.gdf_areas_2.to_file(self.caminho_do_arquivo_4.replace(".shp", "_areas.shp"))

            QMessageBox.information(self, "   A V I S O !", "Arquivos shapefiles gerados com sucesso!")

        except Exception as e:

            QMessageBox.critical(self, "   E R R O !", "Não foi possível gerar os arquivos shapefile esperados, certifique-se de inserir as informações corretamente!")

            print(e)

    # Procurando arquivo de polígonos de lote
    def procurar_1(self):

        self.caminho_do_arquivo_1 = self.procurando_caminho(1)

        self.nome_do_arquivo_entrada.setText(self.caminho_do_arquivo_1)

    # Procurando arquivo de pontos de rua
    def procurar_2(self):

        self.caminho_do_arquivo_2 = self.procurando_caminho(1)

        self.nome_do_arquivo_entrada_2.setText(self.caminho_do_arquivo_2)

    # Salvando arquivo de polígonos e áreas de lote
    def gerando_1(self):

        self.caminho_do_arquivo_3 = self.procurando_caminho(2)

        self.numero_de_poligonos()

        self.calculo_dos_poligonos_internos()

    # Salvando arquivo de polígonos e áreas de rua
    def gerando_2(self):

        self.caminho_do_arquivo_4 = self.procurando_caminho(2)

        self.numero_de_poligonos()

        self.calculo_dos_poligonos_externos()

    # Informações sobre polígonos e áreas de lote
    def ajuda_1(self):

        mensagem  = 'Para que o cálculo funcione corretamente, é preciso inserir um arquivo shapefile com polígonos regulares desenhados. '
        mensagem += 'O gerador de lotes irá calcular e gerar as linhas das bissetrizes para polígonos com qualquer quantidade de vertices, '
        mensagem += 'e calculará as áreas na unidade do SRC escolhido, dos polígonos iguais ou menores que quatro vertices gerando pontos em '
        mensagem += 'seus centros. Para visualizar os valores das áreas no QGIS é preciso habilitar as etiquetas, caso contrário, apenas '
        mensagem += 'pontos aparecerão.'

        QMessageBox.information(self, "   A J U D A !", mensagem)

    # Informações sobre polígonos e áreas de rua
    def ajuda_2(self):

        mensagem  = 'Para que o cálculo funcione corretamente, é preciso que o arquivo shapefile anterior com polígonos continue o mesmo, '
        mensagem += 'e seja inserido um novo arquivo shapefile de pontos que delimitem a distância dos vértices dos polígonos aos possíveis '
        mensagem += 'poços de visita ou cruzamentos. O gerador de ruas irá calcular e gerar as linhas e calculará as áreas na unidade do SRC '
        mensagem += 'escolhido, dos polígonos iguais ou menores que quatro vertices gerando pontos em seus centros. Para visualizar os '
        mensagem += 'valores das áreas no QGIS é preciso habilitar as etiquetas, caso contrário, apenas pontos aparecerão.'

        QMessageBox.information(self, "   A J U D A !", mensagem)

class interface(QMainWindow, funcoes):
    
    def __init__(self):

        super().__init__()

        self.tela()

    def tela(self):

        # 0.0 Configurações da janela
        
        self.setWindowTitle("Método das Bissetrizes")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setGeometry(100, 100, 400, 265)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(imagens('icone')))
        self.setWindowIcon(QIcon(pixmap))

        # 1.0 Configurações do fundo

        self.fonte_texto = QLabel("Lotes", self)
        self.fonte_texto.setStyleSheet("font-weight: bold;")
        self.fonte_texto.move(15, 1)

        self.fundo_nome_do_arquivo_texto = QLabel('', self)
        self.fundo_nome_do_arquivo_texto.setStyleSheet('''background-color: #ededed; 
                                                          border: 1px solid #d8d8d8; 
                                                          padding: 10px;''')
        self.fundo_nome_do_arquivo_texto.setGeometry(100, 100, 370, 85)
        self.fundo_nome_do_arquivo_texto.move(15, 25)

        # 1.1 Arquivo de entrada

        self.nome_do_arquivo_texto = QLabel("Nome do Arquivo", self)
        self.nome_do_arquivo_texto.move(30, 35)

        self.nome_do_arquivo_entrada = QLineEdit('', self)
        self.nome_do_arquivo_entrada.setGeometry(100, 170, 227, 22)
        self.nome_do_arquivo_entrada.move(115, 40)

        self.buscar_1 = QPushButton("...", self)
        self.buscar_1.clicked.connect(self.procurar_1)
        self.buscar_1.setGeometry(100, 200, 25, 22)        
        self.buscar_1.move(346, 40)

        # 1.2 Polígonos

        self.nome_do_arquivo_texto = QLabel("Polígonos", self)
        self.nome_do_arquivo_texto.move(30, 65)

        self.lista_de_lados_do_poligono = QComboBox(self)
        self.lista_de_lados_do_poligono.setGeometry(100, 170, 255, 22)
        self.lista_de_lados_do_poligono.move(115, 70)
        self.lista_de_lados_do_poligono.addItems(["Iguais a três vértices", 
                                                  "Menores ou iguais a quatro vértices", 
                                                  "Qualquer número de vértices (*)"])

        # 1.3 Gerar

        self.gerar_linhas_1 = QPushButton("Gerar", self)
        self.gerar_linhas_1.clicked.connect(self.gerando_1)
        self.gerar_linhas_1.setGeometry(100, 200, 70, 25)
        self.gerar_linhas_1.move(240, 115)

        # 1.4 Ajuda

        self.ajuda_lotes = QPushButton("Ajuda", self)
        self.ajuda_lotes.clicked.connect(self.ajuda_1)
        self.ajuda_lotes.setGeometry(100, 200, 70, 25)
        self.ajuda_lotes.move(315, 115)

        # 2.0 Configurações do fundo

        self.pontos_texto = QLabel("Ruas", self)
        self.pontos_texto.setStyleSheet("font-weight: bold;")
        self.pontos_texto.move(15, 140)

        self.fundo_nome_do_arquivo_texto_2 = QLabel('', self)
        self.fundo_nome_do_arquivo_texto_2.setStyleSheet('''background-color: #ededed; 
                                                            border: 1px solid #d8d8d8; 
                                                            padding: 10px;''')
        self.fundo_nome_do_arquivo_texto_2.setGeometry(100, 100, 370, 55)
        self.fundo_nome_do_arquivo_texto_2.move(15, 165)

        # 2.1 Arquivo de entrada

        self.nome_do_arquivo_texto_2 = QLabel("Nome do Arquivo", self)
        self.nome_do_arquivo_texto_2.move(30, 175)

        self.nome_do_arquivo_entrada_2 = QLineEdit('', self)
        self.nome_do_arquivo_entrada_2.setGeometry(100, 170, 227, 22)
        self.nome_do_arquivo_entrada_2.move(115, 180)

        self.buscar_2 = QPushButton("...", self)
        self.buscar_2.clicked.connect(self.procurar_2)
        self.buscar_2.setGeometry(100, 200, 25, 22)        
        self.buscar_2.move(346, 180)

        # 2.2 Gerar

        self.gerar_linhas_2 = QPushButton("Gerar", self)
        self.gerar_linhas_2.clicked.connect(self.gerando_2)
        self.gerar_linhas_2.setGeometry(100, 200, 70, 25)
        self.gerar_linhas_2.move(240, 225)

        # 2.3 Ajuda

        self.ajuda_cruzamentos = QPushButton("Ajuda", self)
        self.ajuda_cruzamentos.clicked.connect(self.ajuda_2)
        self.ajuda_cruzamentos.setGeometry(100, 200, 70, 25)
        self.ajuda_cruzamentos.move(315, 225)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = interface()
    window.setWindowState(Qt.WindowNoState)
    window.show()
    sys.exit(app.exec_())