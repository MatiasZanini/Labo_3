# -*- coding: utf-8 -*-
"""
Editor de Spyder

Creado por Adriana Márquez
Editado por Matías Zanini
Análisis de mediciones sobre la resistencia de carga Rc del circuito para equivalente Thevenin
Estudio de la potencia disipada en Rc
"""
# cargamos las librerias de python que necesistmos:
import numpy as np
import matplotlib.pyplot as plt
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
os.chdir (r'C:\Users\User\Desktop\Adriana\Laboratorio 3\Analisis phyton\Analisis señales DC')

# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:

file1 = 'prueba1.txt'

'''
Con np.loadtxt(ruta) podemos cargar los datos de una matriz guardada en un
archivo de texto como un array de numpy. Cada renglón es una fila.
Las columnas están separadas por una coma. Eso lo indicamos en el "delimiter".
También, podrían estar separadas por tabs '\t' o punto y coma ';'
Con skiprows=1 le pedimos que se saltee la primer fila, que tiene los títulos.
'''

Misdatos = np.loadtxt(file1, delimiter = ',', skiprows=1)

'''
Ordeno los datos con la tensión de la resistencia.
La función np.argsort(array) ordena de menor a mayor un array de python y
me devuelve los índices del vector ya ordenado.

Luego, evalúo la matriz en dichos índices y ya me quedan las filas ordenadas
de menor a mayor, en este caso, según el voltaje sobre la resistencia.
'''
Misdatos_ordenados = Misdatos[np.argsort(Misdatos[:, 0])]



"""
#leer los datos desde una archivo csv delimitado por tabs
print("nombre del archivo completo con terminación .csv incluida")
file = input()
Misdatos_ordenados=np.genfromtxt(file,delimiter='\t',skip_header=1)
"""

#%% ---------------------------- Gráfico ----------------------------------------

Vres = Misdatos_ordenados[:,0]

corriente = Misdatos_ordenados[:,1]/1000 #paso la corriente a Ampere

Rc = Vres/corriente

Potencia = Vres*corriente

n = len(Vres) # La función len() calcula el largo del vector o lista de python.

'''
Dado que la incertidumbre para las mediciones de V es siempre 5/1023
creamos un vector del largo de las mediciones cuyos elementos sean todos
dicho valor. Esto se hace con la función de numpy full(largo,valor), donde
largo indica el tamaño del vector y valor el número que querramos que 
aparezca en cada elemento.
'''

errory = np.full((n),0.005) 

errorx = (corriente*0.01+0.02)/1000 # la incertidumbre depende de la escala del multimetro

errorRc = (errory/Vres + errorx/corriente)*Rc #incertidumbre de Rc 

errorPot = (errory/Vres + errorx/corriente)*Potencia #incertidumbre de Potencia

plt.ion()

plt.close("all") #cierro los gráficos abiertos

plt.figure(1) # Creo una nueva figura

'''
La función plt.errorbar(x,y, xerr=error_en_x, yerr=error_en_y, fmt=formato)
crea el gráfico. Se le da un array con los errores en xerr e yerr y los coloca
en los puntos como barras de error.

En fmt se le pone el color y el formato de linea. En este caso, '.b' indica que
se quiere que los datos se marquen en el gráfico con un punto (.) azul (b).
'''

plt.errorbar(Rc, Potencia, xerr=errorRc, yerr=errorPot, fmt='.b')
#plt.grid() # Descomentar esta línea si quiero que aparezca la grilla en el gráfico 
#plt.axis([0,2,0,3.5]) # Descomentar si quiero elegir el rango para el eje x del gráfico

# Ponemos etiquetas a los ejes x e y:
plt.xlabel('Resistencia (ohm)')
plt.ylabel('Potencia(W)') 

plt.show() # Muestra la figura


