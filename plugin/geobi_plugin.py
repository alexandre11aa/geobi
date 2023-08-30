import os
import sys
import inspect
import warnings
import subprocess

from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

from qgis.core import QgsProcessingAlgorithm, QgsApplication

# Ignorando aviso de mais de um executável simultâneo
warnings.filterwarnings("ignore", category=ResourceWarning)

# Obtendo o caminho do diretório do script atual
sys.path.append(os.path.split(inspect.getfile(inspect.currentframe()))[0])

import resources

class GeoBi:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):

        # Configurando ícone
        icon = os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], 'icone_de_mdb.png')

        # Configurando botão de ação
        self.action = QAction(QIcon(icon), 'Ferramente GeoBi', self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        # Configurando locais onde o botão de ação estará
        self.iface.addPluginToMenu('&GeoBi Tools', self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):

        # Removendo botões de ação ao retirar seleção de plugin
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu('&MFerramenta GeoBi', self.action)
        del self.action

    def run(self):

        # Abrindo executável do GeoBi no QGis
        executable_path = os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], 'GeoBi.exe')
        subprocess.Popen([executable_path])
