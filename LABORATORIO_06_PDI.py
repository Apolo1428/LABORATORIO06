# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:54:13 2021

@author: GRUPO
"""

import pathlib
import sys
import numpy as np
import math
import cmath
import os
import cv2
import random
from GUIPDI import*
from Matrix_Kernel import get_kernel 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import Filtros

def matrix_format(mat):

    a = mat.round(5)
    
    string = np.array2string(a)
    l = string[1:-1].split("\n")
    len_ = len(l[1][l[1].index('['):][1:-1])
    up = "┌" + len_*" " + "┐\n"
    down = "└" + len_*" " + "┘"
    
    # print(up+a+down)
    rows = a.shape[0]
    string = up
    for k in range(rows):
        string += "│" + l[k][l[k].index('['):][1:-1] +"│\n"
    string += down
    return string

# matrix_format('[1,2.12345,3;1,4,3.123456;3,3,3;1,2,3]')
# input()
class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        ###################################################################
        self.ui.abutton.clicked.connect(self.abrir_img1)
        self.ui.abutton_2.clicked.connect(self.abrir_img2)
        self.ui.abutton_3.clicked.connect(self.abrir_img3)

        
        self.ui.rbutton.clicked.connect(self.reset1)
        self.ui.rbutton_2.clicked.connect(self.reset2)
        self.ui.rbutton_3.clicked.connect(self.reset3)

        self.ui.update_p.clicked.connect(self.update_pk)
        self.ui.update_d.clicked.connect(self.update_dk)
        self.ui.update_f.clicked.connect(self.update_f)
        self.ui.update_t1.clicked.connect(self.update_t1)        
        
        self.ui.sbutton.clicked.connect(self.save_img1)
        self.ui.sbutton_2.clicked.connect(self.save_img2)
        self.ui.sbutton_3.clicked.connect(self.save_img3)
        
        
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def abrir_img1(self):
        archivo = QtWidgets.QFileDialog.getOpenFileName(self,'Abrir imagen','C:\\','Todos los pixmap (*.bmp *.cur *.gif *.icns *.ico *.jpeg *.jpg *.pbm *.pgm *.png *.ppm *.svg *.svgz *.tga *.tif *.tiff *.wbmp *.webp *.xbm *.xpm)')[0]
        self.image_work1 = archivo
        self.image_work1cv = cv2.imread(archivo)
        self.ui.imgdef.setPixmap(QtGui.QPixmap(archivo))
    def abrir_img2(self):
        archivo = QtWidgets.QFileDialog.getOpenFileName(self,'Abrir imagen','C:\\','Todos los pixmap (*.bmp *.cur *.gif *.icns *.ico *.jpeg *.jpg *.pbm *.pgm *.png *.ppm *.svg *.svgz *.tga *.tif *.tiff *.wbmp *.webp *.xbm *.xpm)')[0]
        self.image_work2 = archivo
        self.image_work2cv = cv2.imread(archivo)
        self.ui.imgdef_2.setPixmap(QtGui.QPixmap(archivo))    
    def abrir_img3(self):
        archivo = QtWidgets.QFileDialog.getOpenFileName(self,'Abrir imagen','C:\\','Todos los pixmap (*.bmp *.cur *.gif *.icns *.ico *.jpeg *.jpg *.pbm *.pgm *.png *.ppm *.svg *.svgz *.tga *.tif *.tiff *.wbmp *.webp *.xbm *.xpm)')[0]
        self.image_work3 = archivo
        self.image_work3cv = cv2.imread(archivo,0)
        self.ui.imgdef_3.setPixmap(QtGui.QPixmap(archivo))
    
    def reset1(self):
        self.ui.imgfilt.clear()
    def reset2(self):
        self.ui.imgfilt_2.clear()
    def reset3(self):
        self.ui.imgfilt_3.clear()
    
    def save_img1(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        archivo, _ = QtWidgets.QFileDialog.getSaveFileName(self,'Guardar archivo...', 'C:\\','Imagen (*.bmp *.jpg *.png)')
        self.qImg1.save(archivo)
    def save_img2(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        archivo, _ = QtWidgets.QFileDialog.getSaveFileName(self,'Guardar archivo...', 'C:\\','Imagen (*.bmp)')
        self.qImg2.save(archivo)
    def save_img3(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        archivo, _ = QtWidgets.QFileDialog.getSaveFileName(self,'Guardar archivo...', 'C:\\','Imagen (*.bmp)')
        self.qImg3.save(archivo)
    
    
    def update_pk(self):
        try:
            self.kernel1 = np.matrix(self.ui.lineedit.text()[1:-1])
            self.ui.matrizLabel.setText(matrix_format(self.kernel1))
            self.image_1_proc = cv2.filter2D(self.image_work1cv, -1, self.kernel1)

            size = self.image_1_proc.shape
            step = self.image_1_proc.size / size[0]
            qformat = QtGui.QImage.Format_Indexed8
        
            if len(size) == 3:
                if size[2] == 4:
                    qformat = QtGui.QImage.Format_RGBA8888
                else:
                    qformat = QtGui.QImage.Format_RGB888
            img = QtGui.QImage(self.image_1_proc, size[1], size[0], step, qformat)
            img = img.rgbSwapped()
            self.qImg1 = img
            self.ui.imgfilt.setPixmap(QtGui.QPixmap.fromImage(img))
        except:
            self.ui.lineedit.setText("Error de Formato o Imagen")
    def update_dk(self):
        try:
            aumento = float(self.ui.slider.value())
            aumento = round(aumento/10+1)
            dict_kernel = get_kernel(aumento)
            self.kernel1 = np.matrix(dict_kernel[self.ui.combo.currentIndex()])
            
            self.ui.matrizLabel.setText(matrix_format(self.kernel1))
            self.image_1_proc = cv2.filter2D(self.image_work1cv, -1, self.kernel1)
            size = self.image_1_proc.shape
            step = self.image_1_proc.size / size[0]
            qformat = QtGui.QImage.Format_Indexed8
        
            if len(size) == 3:
                if size[2] == 4:
                    qformat = QtGui.QImage.Format_RGBA8888
                else:
                    qformat = QtGui.QImage.Format_RGB888
            img = QtGui.QImage(self.image_1_proc, size[1], size[0], step, qformat)
            img = img.rgbSwapped()
            self.qImg1 = img
            self.ui.imgfilt.setPixmap(QtGui.QPixmap.fromImage(img))
            
        except:
            self.ui.lineedit.setText("Error de Formato o Imagen")
    def update_f(self):
        try:
            gray = cv2.cvtColor(self.image_work2cv, cv2.COLOR_BGR2GRAY)
            self.image_2_proc = Filtros.dict_filtros[self.ui.combo_2.currentIndex()](gray)
            cv2.imwrite('IMAGEN_AUX.jpg', self.image_2_proc)
            img = cv2.imread('IMAGEN_AUX.jpg')
            
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.qImg2 = qImg
            self.ui.imgfilt_2.setPixmap(QtGui.QPixmap.fromImage(qImg))
            os.remove('IMAGEN_AUX.jpg')
        except:
            print("error en el programa")

    def update_t1(self):
        try:
            img = self.image_work3cv 
            dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            
            # Calcular el módulo de la Transformada de Fourier
            magnitude_spectrum = 20 * \
                np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
            cv2.imwrite('IMAGEN_AUX.jpg',magnitude_spectrum)     
            
            self.ui.imgfilt_3.setPixmap(QtGui.QPixmap('IMAGEN_AUX.jpg'))
            os.remove('IMAGEN_AUX.jpg')
        except:
            print("error en el programa")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())