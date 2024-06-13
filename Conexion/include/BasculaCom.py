
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time as tm
import mysql.connector
from include.Consultas import *
#Clase de lectura continua de PLC
class PlcThread(QtCore.QThread):
    result=pyqtSignal( bool)
    fini=pyqtSignal(bool)
    AcumuSurt=0
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        # self.main_window = MainWindow
        
    @QtCore.pyqtSlot(list)
    def run(self):     
        Res=0
        with open('conexion.txt', 'r') as archivo:
            contenido = archivo.read()
        try:
            conexion = mysql.connector.connect(
                    host = contenido,
                    user ="root",
                    password ="",  
                    database ="valmo",
                    port =3306
            )
                
            if conexion.is_connected():
                cursor = conexion.cursor()
                mysql_value = 1
                conexion = True
                evento()
            else:
                mysql_value = 0
                conexion = False 
        except Exception as e:
            mysql_value = 0

            conexion = False     
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EMISOR DE VARIABLES A LA OTRA CLASE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.result.emit(conexion)
        tm.sleep(3)
        self.fini.emit(Res)
    