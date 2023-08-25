from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys 

class SimpleGUI(QMainWindow):
    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Método das Bissetrizes")
        self.setGeometry(100, 100, 400, 300)

        # Arquivo de entrada

        self.fonte_texto = QLabel("Fonte", self)
        self.fonte_texto.setStyleSheet("font-weight: bold;")
        self.fonte_texto.move(15, 1)

        self.fundo_nome_do_arquivo_texto = QLabel('', self)
        self.fundo_nome_do_arquivo_texto.setStyleSheet('''background-color: #ededed; 
                                                          border: 1px solid #d8d8d8; 
                                                          padding: 10px;''')
        self.fundo_nome_do_arquivo_texto.setGeometry(100, 100, 370, 52)
        self.fundo_nome_do_arquivo_texto.move(15, 25)

        self.nome_do_arquivo_texto = QLabel("Nome do Arquivo", self)
        self.nome_do_arquivo_texto.move(30, 35)

        self.nome_do_arquivo_entrada = QLineEdit(self)
        self.nome_do_arquivo_entrada.setGeometry(100, 170, 227, 22)
        self.nome_do_arquivo_entrada.move(115, 40)

        self.buscar_1 = QPushButton("...", self)
        self.buscar_1.clicked.connect(self.show_message)
        self.buscar_1.setGeometry(100, 200, 25, 22)        
        self.buscar_1.move(346, 40)

        # Opções

        self.opcoes_texto = QLabel("Opções", self)
        self.opcoes_texto.setStyleSheet("font-weight: bold;")
        self.opcoes_texto.move(15, 75)

        self.fundo_opcoes_texto = QLabel('', self)
        self.fundo_opcoes_texto.setStyleSheet('''background-color: #ededed; 
                                                          border: 1px solid #d8d8d8; 
                                                          padding: 10px;''')
        self.fundo_opcoes_texto.setGeometry(100, 100, 370, 52)
        self.fundo_opcoes_texto.move(15, 100)

        ## Polígonos

        self.nome_do_arquivo_texto = QLabel("Polígonos", self)
        self.nome_do_arquivo_texto.move(30, 110)

        self.lista_de_lados_do_poligono = QComboBox(self)
        self.lista_de_lados_do_poligono.setGeometry(100, 170, 255, 22)
        self.lista_de_lados_do_poligono.move(115, 115)
        self.lista_de_lados_do_poligono.addItems(["Iguais à três vértices", 
                                                  "Iguais à quatro vértices", 
                                                  "Menores ou iguais à quatro vértices", 
                                                  "Maiores que quatro vértices (*)",
                                                  "Maiores ou iguais à quatro vértices (*)",
                                                  "Maiores ou iguais à três vétcies (*)"])

        # Gerar

        self.gerar_linhas = QPushButton("Gerar", self)
        self.gerar_linhas.clicked.connect(self.show_message)
        self.gerar_linhas.setGeometry(100, 200, 70, 25)

    def show_message(self):
        print('oi')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())
