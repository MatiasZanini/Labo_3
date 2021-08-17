# -*- coding: utf-8 -*-
"""
Editor de Spyder

Creado por Adriana Márquez
Análisis de mediciones de V0, V1 e I para estudiar el comportamiento VvsI de una resistencia
y por ley de OHM obtener el valor de R
"""
#%%
#cargamos las librerias de python que necesistmaos
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from IPython import get_ipython

#selecciono si las figuras aparecen en la terminal (inline) o en ventana emergente (qt5)
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')

#Elijo el directorio donde se encuentran los archivos que voy a analizar
os.chdir (r'C:\Users\User\Desktop\Adriana\Laboratorio 3\Analisis phyton\Analisis señales DC')

#Leo el archivo txt tiene que estar en la misma carpeta que el programa
print("nombre del archivo completo con terminación .txt incluida")
file1 = input()
#en el archivo que leo las columnas están separadas por coma, la primera fila tiene el título entonces la salteo
Misdatos1=[]
Misdatos = np.loadtxt(file1, delimiter=",",skiprows=1) 
#print(Misdatos1)
#Ordeno los datos con la tensión de entrada
Misdatos1=Misdatos[np.argsort(Misdatos[:, 0])]

"""
#leer los datos desde una archivo csv delimitado por tabs
print("nombre del archivo completo con terminación .csv incluida")
file = input()
Misdatos1=np.genfromtxt(file,delimiter='\t',skip_header=1)
"""

#Datos ordenados col0 : Vfuente, col1: Vresistencia, Col2. Corriente en mA
y0= Misdatos1[:,0]
y1 = Misdatos1[:,1]
x1 = Misdatos1[:,2]/1000 #paso la corrient a Ampere
n=len(y1)
errory=np.full((n),0.005) #la incertidumbre para las mediciones de V es 5/1023
errorx=(x1*0.01+0.02)/1000 # la incertidumbre depende de la escala del multimetro
plt.ion()
#cierro los gráficos abiertos
plt.close("all")
#Grafico los datos del archivo
plt.figure(1)
plt.errorbar(x1,y1,xerr=errorx,yerr=errory,fmt=".b")
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xlabel('Corriente (A)');
plt.ylabel('Tensión (V)');
plt.show()


print('Chequeamos que el comportamiento de V vs I sea lineal antes de realizar el ajuste')


#%%
#Ajuste por caudrados minimos pesado con incetidumbres en y
w=1/errory
X = sm.add_constant(x1)
wls_model = sm.WLS(y1,X, weights=w)
results = wls_model.fit()
o,R=results.params
#intervalo de confianza para ordenada al origen y pendiente
oint,Rint=results.conf_int(alpha=0.05)
deltaR=(Rint[1]-Rint[0])/2
deltao= (oint[1]-oint[0])/2

print("R=(", R,"+/-",deltaR,") ohm")
print("ordenada al origen=(", o,"+/-",deltao,") V")

#calculo las bandas de confianza y predicción
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.sandbox.regression.predstd import wls_prediction_std

st, data, ss2 = summary_table(results, alpha=0.05)

fittedvalues = data[:, 2] #resultado de los valores ajustados
predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T #bandas de confianza
prstd, iv_l, iv_u = wls_prediction_std(results,alpha=0.05) #bandas de predicción con P>0.95

plt.figure(2)
plt.errorbar(x1,y1,xerr=errorx,yerr=errory,fmt=".b") #grafico valores medidos
#plt.grid('on');#agrega una grilla al grafico
#plt.axis([0,2,0,3.5]) #permite seleccionar la escala
plt.xlabel('Corriente (A)');
plt.ylabel('Tensión (V)');
plt.plot(x1, fittedvalues, '-', lw=1) #grafico de la recta de ajuste
plt.plot(x1, iv_l, 'r--', lw=2) #banda de predicción inferior
plt.plot(x1, iv_u, 'r--', lw=2) #banda de predicción superior
plt.plot(x1, predict_mean_ci_low, 'g--', lw=1) #banda de confianza inferior
plt.plot(x1, predict_mean_ci_upp, 'g--', lw=1) #banda de confianza superior
titulo=('ley de ohm - R = ('+ str(round(R,2))+"+/-"+ str(round(deltaR,2))+") ohm")
plt.title(titulo)


#%%
#obtención de la resistencia del amperímetro
vamp=y0-y1 #caida de tensión en el amperímetro
errorvamp=2*errory
#Ajuste por caudrados minimos pesado con incetidumbres en y
wa=1/errorvamp
X = sm.add_constant(x1)
wls_model = sm.WLS(vamp,X, weights=wa)
resultsamp = wls_model.fit()
oa,Ra=resultsamp.params
#intervalo de confianza para ordenada al origen y pendiente
oaint,Raint=resultsamp.conf_int(alpha=0.05)
deltaRa=(Raint[1]-Raint[0])/2
deltaoa= (oaint[1]-oaint[0])/2

sta, dataa, ss2a = summary_table(resultsamp, alpha=0.05)
print()
print("Ramperimetro=(", Ra,"+/-",deltaRa,") ohm")
print("ordenada al origen=(", oa,"+/-",deltaoa,") V")

plt.figure(3)
plt.errorbar(x1,vamp,xerr=errorx,yerr=errorvamp,fmt=".b")
plt.plot(x1, dataa[:,2], '-', lw=1)
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xlabel('Corriente (A)');
plt.ylabel('Tensión (V)');
tituloa=('Resistencia amperimetro= ('+ str(round(Ra,2))+"+/-"+ str(round(deltaRa,2))+") ohm")
plt.title(tituloa)


