# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:19:27 2020

@author: User
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from IPython import get_ipython

#%%

#selecciono si las figuras aparecen en la terminal (inline) o en ventana emergente (qt5)
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')

#Elijo el directorio donde se encuentran los archivos que voy a analizar
os.chdir (r'C:\Users\Cesar\Dropbox\Cursos\Lab3\Simulaciones\LTSpice\2021_C1\Transitorios')

#Leo el archivo txt tiene que estar en la misma carpeta que el programa

file1 = 'SalidaRCtransitorio.txt'
#en el archivo que leo las columnas están separadas por coma, la primera fila tiene el título entonces la salteo
Misdatos1=[]
Misdatos = np.loadtxt(file1, delimiter=",",skiprows=1) 
#print(Misdatos1)
#Ordeno los datos con la resistencia utilizada
Misdatos1=Misdatos[np.argsort(Misdatos[:, 1])]

"""
#leer los datos desde una archivo csv delimitado por tabs
print("nombre del archivo completo con terminación .csv incluida")
file = input()
Misdatos1=np.genfromtxt(file,delimiter='\t',skip_header=1)
"""

#Datos ordenados col0 : Vfuente, col1: Vresistencia, Col2. Corriente en mA
y0= Misdatos1[:,0] #valores de tau
errory0 = Misdatos1[:,1] #incertidumbre de tau
x0= Misdatos1[:,2] #valores de R
#errorx0=Misdatos1[:,3]/1 #valores de incertidumbre de R

plt.ion()

plt.close("all")
#Grafico los datos del archivo
plt.figure(1)
plt.plot(x0,y0,'.b')
plt.xlabel('Resistencia (ohm)');
plt.ylabel('Tau (s)');
plt.show()


print('Chequeamos que el comportamiento de Tau vs R sea lineal antes de realizar el ajuste')


#%%
#Ajuste por cuadrados minimos ponderado con incertidumbres en y
w=1/errory0
X = sm.add_constant(x0)
wls_model = sm.WLS(y0,X, weights=w)
results = wls_model.fit()
o,C=results.params
#intervalo de confianza para ordenada al origen y pendiente
oint,Cint=results.conf_int(alpha=0.05)
deltaC=abs((Cint[1]-Cint[0])/2)
deltao= abs((oint[1]-oint[0])/2)

print("C = (", C," +/- ",deltaC,") F")
print("ordenada al origen = (", o," +/- ",deltao,") V")

#%%
plt.figure(2)
yajustado = o+C*x0
plt.plot(x0,y0,'.b');
plt.plot(x0,yajustado,'r')
plt.xlabel('Resistencia (ohm)', fontsize = 14)
plt.ylabel('Tau (s)', fontsize = 14)

