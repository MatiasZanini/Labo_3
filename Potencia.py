# -*- coding: utf-8 -*-
"""
Editor de Spyder

Creado por Adriana Márquez
Análisis de mediciones sobre la resistencia de carga Rc del circuito para equivalente Thevenin
Estudio de la potencia disipada en Rc
"""
#cargamos las librerias de python que necesistmaos
import numpy as np
import matplotlib.pyplot as plt
import os
from IPython import get_ipython

#selecciono si las figuras aparecen en la terminal (inline) o en ventana emergente (qt5)
get_ipython().run_line_magic('matplotlib', 'inline')
#get_ipython().run_line_magic('matplotlib', 'qt5')

#Elijo el directorio donde se encuentran los archivos que voy a analizar
os.chdir (r'C:\Users\User\Desktop\Adriana\Laboratorio 3\Analisis phyton\Analisis señales DC')

#Leo el archivo txt tiene que estar en la misma carpeta que el programa
print("nombre del archivo completo con terminación .txt incluida")
file1 = input()
#en el archivo que leo las columnas están separadas por coma, la primera fila tiene el título entonces la salteo
Misdatos1=[]
Misdatos = np.loadtxt(file1, delimiter=",",skiprows=1)

#Ordeno los datos con la tensión de la resistencia
Misdatos1=Misdatos[np.argsort(Misdatos[:, 0])]



"""
#leer los datos desde una archivo csv delimitado por tabs
print("nombre del archivo completo con terminación .csv incluida")
file = input()
Misdatos1=np.genfromtxt(file,delimiter='\t',skip_header=1)
"""

#Datos ordenados col0: Vresistencia, Col1: Corriente en mA
y0= Misdatos1[:,0]
x1 = Misdatos1[:,1]/1000 #paso la corrient a Ampere
Rc=y0/x1
Potencia=y0*x1
n=len(y0)
errory=np.full((n),0.005) #la incertidumbre para las mediciones de V es 5/1023
errorx=(x1*0.01+0.02)/1000 # la incertidumbre depende de la escala del multimetro
errorRc=(errory/y0+errorx/x1)*Rc #incertidumbre de Rc 
errorPot=(errory/y0+errorx/x1)*Potencia #incertidumbre de Potencia
plt.ion()
#cierro los gráficos abiertos
plt.close("all")
#Grafico los datos del archivo
plt.figure(1)
plt.errorbar(Rc,Potencia,xerr=errorRc,yerr=errorPot,fmt=".b")
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xlabel('Resistencia (ohm)');
plt.ylabel('Potencia(W)');
plt.show()


