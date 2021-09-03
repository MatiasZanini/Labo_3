# -*- coding: utf-8 -*-
"""
Editor de Spyder

Creado por Adriana Márquez
Editado por Matías Zanini
Análisis de mediciones de V0, V1 e I para estudiar el comportamiento VvsI de una resistencia
y por ley de OHM obtener el valor de R
"""
# cargamos las librerias de python que necesistmos:
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from IPython import get_ipython

#%% ------------------------ Elegir modo de salida de los gráficos -----------------------------------
'''
Descomentar la línea que corresponda. 
Si quieren que las figuras aparezcan en la terminal: inline 
Si quieren que las figuras aparezcan en una ventana emergente: qt5
'''
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')


#%% ---------------------- Carga de datos ---------------------------------------


# Colocar la ruta de la carpeta con los archivos entre r' ':
os.chdir (r'C:\Users\Mati\Desktop\labo3')

# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:

file1 = 'prueba1.txt'

'''
Con np.loadtxt(ruta) podemos cargar los datos de una matriz guardada en un
archivo de texto como un array de numpy. Cada renglón es una fila.
Las columnas están separadas por una coma. Eso lo indicamos en el "delimiter".
Con skiprows=1 le pedimos que se saltee la primer fila, que tiene los títulos.
'''

Misdatos = np.loadtxt(file1, delimiter=',', skiprows=1) 

'''
Ordeno los datos con la tensión de entrada.
La función np.argsort(array) ordena de menor a mayor un array de python y
me devuelve los índices del vector ya ordenado.

Luego, evaluo la matriz en dichos índices y ya me quedan las filas ordenadas
de menor a mayor, en este caso, según el voltaje.
'''
Misdatos_ordenados = Misdatos[np.argsort(Misdatos[:, 0])]

'''
Armamos arrays(vectores) con las columnas de mi archivo:
'''

Vfuente= Misdatos_ordenados[:,0] # Voltaje de la fuente

Vres = Misdatos_ordenados[:,1] # Voltaje que cae en la resistencia

Corriente = Misdatos_ordenados[:,2]/1000 # Corriente y pasaje a Ampere

n_res = len(Vres) # Guardamos el largo del vector en esta variable

'''
La función np.full(largo, numero) me genera un array de tamaño dado por "largo"
cuyos elementos son todos el numerito dado por "numero". 
'''
errory = np.full((n_res),0.005) # La incertidumbre para las mediciones de V es 5/1023
errorx=(Corriente*0.01+0.02)/1000 # La incertidumbre depende de la escala del multímetro

#%% ----------------------------- Gráfico de los datos crudos -----------------------

'''
Graficamos los datos tal cual salieron del Arduino, ordenados según el voltaje,
para observar si su comportamiento es lineal o no en una primera instancia.
'''

plt.ion() # Activa el modo interactivo del gráfico.

plt.close('all') # Cierro los gráficos abiertos por si había alguno.

plt.figure(1) # Genera una nueva figura donde vamos a graficar.

'''
La función plt.errorbar(x,y, xerr=error_en_x, yerr=error_en_y, fmt=formato)
crea el gráfico. Se le da un array con los errores en xerr e yerr y los coloca
en los puntos como barras de error.

En fmt se le pone el color y el formato de linea. En este caso, '.b' indica que
se quiere que los datos se marquen en el gráfico con un punto (.) azul (b).
'''

plt.errorbar(Corriente, Vres, xerr=errorx,yerr=errory, fmt=".b")

plt.grid() # Esto activa la grilla en el gráfico. Pueden comentarlo si no lo quieren.

# Ponemos etiquetas a los ejes x e y:
plt.xlabel('Corriente (A)', fontsize=16);
plt.ylabel('Tensión (V)', fontsize=16);

plt.show() # Muestra la figura


#%% ----------------Ajuste por caudrados mínimos pesado con incetidumbres en y ---------------


'''
Definimos el peso en el ajuste como 1/error ya que queremos que, a errores
más grandes, se le dé menos peso en el ajuste:
'''
w = 1/errory

'''

'''

X = sm.add_constant(Corriente)

wls_model = sm.WLS(Vres,X, weights = w) # Realiza el ajuste con el peso w

results = wls_model.fit() # Genera los parametros del ajuste

o, R = results.params # Entrega los parámetros del ajuste en dos variables: ordenada al origen y pendiente


oint, Rint = results.conf_int(alpha=0.05) #intervalo de confianza para ordenada al origen y pendiente

deltaR = (Rint[1]-Rint[0])/2 # Error de R

deltao = (oint[1]-oint[0])/2 # Error de o

print("R=(", R,"+/-",deltaR,") ohm")
print("ordenada al origen=(", o,"+/-",deltao,") V")

#calculo las bandas de confianza y predicción
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.sandbox.regression.predstd import wls_prediction_std

st, data, ss2 = summary_table(results, alpha=0.05)

fittedvalues = data[:, 2] # resultado de los valores ajustados

predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T # bandas de confianza
prstd, iv_l, iv_u = wls_prediction_std(results,alpha=0.05) # bandas de predicción con P>0.95

#%% --------------------- Graficamos el Ajuste obtenido ------------------------

plt.figure(2)

plt.errorbar(Corriente,Vres,xerr=errorx,yerr=errory,fmt=".b") #grafico valores medidos
plt.grid()
#plt.axis([0,2,0,3.5]) #permite seleccionar la escala
plt.xlabel('Corriente (A)');
plt.ylabel('Tensión (V)');
plt.plot(Corriente, fittedvalues, '-', lw=1) #grafico de la recta de ajuste
plt.plot(Corriente, iv_l, 'r--', lw=2) #banda de predicción inferior
plt.plot(Corriente, iv_u, 'r--', lw=2) #banda de predicción superior
plt.plot(Corriente, predict_mean_ci_low, 'g--', lw=1) #banda de confianza inferior
plt.plot(Corriente, predict_mean_ci_upp, 'g--', lw=1) #banda de confianza superior
titulo=('ley de ohm - R = ('+ str(round(R,2))+"+/-"+ str(round(deltaR,2))+") ohm")
plt.title(titulo)


#%%
#obtención de la resistencia del amperímetro
Vamp = Vfuente - Vres #caida de tensión en el amperímetro
errorVamp = 2*errory

#Ajuste por caudrados minimos pesado con incetidumbres en y
wa=1/errorVamp

X = sm.add_constant(Corriente)

wls_model = sm.WLS(Vamp,X, weights=wa)

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
plt.errorbar(Corriente,Vamp,xerr=errorx,yerr=errorVamp,fmt=".b")
plt.plot(Corriente, dataa[:,2], '-', lw=1)
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xlabel('Corriente (A)');
plt.ylabel('Tensión (V)');
tituloa=('Resistencia amperimetro= ('+ str(round(Ra,2))+"+/-"+ str(round(deltaRa,2))+") ohm")
plt.title(tituloa)


