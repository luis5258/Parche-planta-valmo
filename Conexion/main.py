import sys,os
import time as tm
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
#from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtWidgets 
from PyQt5.QtWidgets import *
from PyQt5.uic  import loadUi
from PyQt5.QtCore import Qt
import imagen.recursos
import sys
from include.BasculaCom import *
from PyQt5.QtGui import QKeyEvent


class MainWindow(QMainWindow):
    ReqToWrite=pyqtSignal(list)
    ReqToDisAla=pyqtSignal(list)
    global DataToPlc
    DataToPlc = [1,]

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        path=os.getcwdb()
        uic=loadUi("templateCon/index.ui",self)
        self.show()
        self.setFocus()
                
        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------- HILO PLC --------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        
        self._thread=QThread()
        self._threaded=PlcThread()
        self._threaded.result.connect(self.MainFun)
        self.ReqToWrite.connect(self._threaded.run)
        self._threaded.moveToThread(self._thread)
        app.aboutToQuit.connect(self._thread.quit)
        self._thread.start()
        self.IniciaTransmision()
        self._threaded.fini.connect(self.IniciaTransmision)
        
        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------- FIN DEL HILO -------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------------------------------------
        
    @QtCore.pyqtSlot()
        
    

    def IniciaTransmision(self):
        self.ReqToWrite.emit(DataToPlc)
            
    def MainFun(self, conexion):            
        if conexion == True: 

            self.conexion_lbl.setStyleSheet("background-color:Transparent; color: rgb(0, 170, 0); font: 20pt;")          
            conexion_db="Conexión exitosa"
            self.conexion_lbl.setText(conexion_db)
        else:
            self.conexion_lbl.setStyleSheet("background-color:Transparent; color: rgb(255, 0, 0); font: 20pt;")          
            conexion_db="Sin conexión"
            self.conexion_lbl.setText(conexion_db)
        
app = QtWidgets.QApplication(sys.argv)
UI=MainWindow()
UI.show()
sys.exit(app.exec())