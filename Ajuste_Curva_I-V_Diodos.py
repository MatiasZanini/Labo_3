"""
Ajuste de la curva I-V de un diodo
Creado por Adriana Márquez
Editado por Matías Zanini


Para ajustar  más de un archivo, simplemente replicar las partes de carga 
de datos y análisis.
"""
# cargamos las librerias de python que necesistmos:
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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


#%% ---------------------- Carga de datos -----------------------------------------------------------


# Colocar la ruta de la carpeta con los archivos entre r' ':
os.chdir (r'C:\Users\User\Desktop\Adriana\Laboratorio 3\Analisis phyton\Analisis señales DC')


# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:

file_name = 'prueba1.txt'

'''
Con np.loadtxt(ruta) podemos cargar los datos de una matriz guardada en un
archivo de texto como un array de numpy. Cada renglón es una fila.
Las columnas están separadas por una coma. Eso lo indicamos en el "delimiter".
También, podrían estar separadas por tabs '\t' o punto y coma ';'
Con skiprows=1 le pedimos que se saltee la primer fila, que tiene los títulos.
'''

Datosorig = np.loadtxt(file_name, delimiter = ',', skiprows = 1)

'''
Ordeno los datos según la primer columna.
La función np.argsort(array) ordena de menor a mayor un array de python y
me devuelve los índices del vector ya ordenado.

Luego, evalúo la matriz en dichos índices y ya me quedan las filas ordenadas
de menor a mayor.
'''
Datos = Datosorig[np.argsort(Datosorig[:, 0])]


#%% ----------------------------- Gráfico de los datos crudos -----------------------

# De la tabla extraigo sólo la 2da y 3ra columna (Vdiodo y Corriente):
    
Vd = Datos[:,1]

I = Datos[:,2]

n = len(Vd) # La función len() calcula el largo del vector o lista de python.

'''
Dado que la incertidumbre para las mediciones de Vd es siempre 5/1023
creamos un vector del largo de las mediciones cuyos elementos sean todos
dicho valor. Esto se hace con la función de numpy full(largo,valor), donde
largo indica el tamaño del vector y valor el número que querramos que 
aparezca en cada elemento.
'''
errorVd = np.full((n),0.005) 

errorI = np.full((n),0.010/220)+I/220*0.68 # la incertidumbre de la corriente depende de la R usada para medirla

# Grafico la curva I-V con todos los datos:
    
plt.close('all') # Cierro todos los gráficos

plt.figure(1) # Creo una nueva figura

'''
La función plt.errorbar(x,y, xerr=error_en_x, yerr=error_en_y, fmt=formato)
crea el gráfico. Se le da un array con los errores en xerr e yerr y los coloca
en los puntos como barras de error.

En fmt se le pone el color y el formato de linea. En este caso, '.b' indica que
se quiere que los datos se marquen en el gráfico con un punto (.) rojo (r).
'''
plt.errorbar(Vd, I, xerr=errorVd, yerr=errorI, fmt='r.')

plt.grid('on') # Pone la grilla en el gráfico

# Ponemos las etiquetas a los ejes x e y:
plt.xlabel('Tensión en el diodo (V)', fontsize = 14)
plt.ylabel('Corriente en el diodo (A)', fontsize = 14)

plt.title('Curva I-V de un diodo', fontsize = 16) # Creamos un título para el gráfico
plt.show() # Muestra el gráfico

#%%

'''
La curva parece ser exponencial, como indica un modelo teórico aproximado.
Querríamos verificarlo graficando I vs V en escala logarítmica
'''

plt.figure(2) # Crea una nueva figura (no es necesario cerrar la anterior)

plt.semilogy(Vd, I, 'r.') # Grafica en escala logarítmica con puntos (.) rojos (r).

plt.grid('on') # Grilla del gráfico

# Ponemos las etiquetas a los ejes x e y, más el título:
plt.xlabel('Caída de tensión en el diodo (V)', fontsize = 14)
plt.ylabel('Corriente en el diodo (A)', fontsize = 14)
plt.title('Curva I-V de un diodo común', fontsize = 16)
plt.show() # Mostramos el gráfico.


#%%

'''
El modelo aproximado es I = Io (exp(V/VT) - 1) donde Io y VT son constantes.

Quiero ajustar tal modelo a los datos xnew, ynew.

Para eso, creamos la función "modelo(V, I0, VT)" de 3 variables. Las primeras
dos, corresponden al voltaje y la corriente sobre el diodo, mientras que 
VT será el parámetro a ajustar.
'''

def modelo(V, Io,VT):
    
    return Io * (np.exp(V/VT) - 1)
  

'''
La función de scipy, curve_fit(f,xdata,ydata, p0=None), permite realizar 
ajustes mediante una función personalizada cualquiera (lineal o no). Para
ello, pide que se le entregue la función f, los datos de la variable 
independiente xdata y la variable dependiente ydata. 

En las funciones de python, encontrarán a veces variables que tienen un igual
cuando se las llama. En este caso, p0. Estas variables son opcionales y,
en caso de no ingresar ninguna, tomarán el valor que tienen al lado del igual
en su definición.
En este ejemplo, p0=None la variable p0 tendrá el valor None, que para
python es una especie de variable neutra, no hace nada.

Para algunos ajustes, será necesario poner una lista p0. Esta lista ingresada
por el usuario, entrega a curve_fit un "guess inicial". Esto es, una lista
con valores cercanos a los que se espera obtener en el ajuste. Esto le
simplifica la tarea a curve_fit de hallar los parámetros óptimos. 
En nuestro caso, como solo tenemos un parámetro (VT), podríamos poner p0=vguess
donde vguess es un valor cercano a lo que esperarían obtener para VT.
Si hubieran más parámetros que ajustar, se deberían poner como una lista
p0=[guess1,guess2, ...].
'''

popt, pcov = curve_fit(modelo, Vd, I) # popt son los parámetros que entrega el ajuste y pcov la covarianza

# ESTIMO LOS ERRORES ( 1 sigma ):
perr = np.sqrt(np.diag(pcov)) # np.diag(pcov) calcula la diagonal de la matriz de covarianza

plt.figure(3)

plt.errorbar(Vd, I, xerr=errorVd, yerr=errorI, fmt='r.',  label='Datos')

'''
Podemos modificar el grosor de la línea del gráfico con el parámetro 
"linewidth" y agregar una leyenda que se mostrará etiquetada en el gráfico con
"label"
'''

plt.plot(Vd, modelo(Vd, *popt),'b-', linewidth = 3, label='Ajuste')
plt.grid('on')
plt.xlabel('Caída de tensión en el diodo (V)', fontsize = 14)
plt.ylabel('Corriente en el diodo (A)', fontsize = 14)
plt.title('Curva I-V de un diodo común', fontsize = 16)

plt.legend() # Muestra el cuadrito con las etiquetas que pusimos en "label"

plt.show()

# Mostramos en la consola los parámetros obtenidos:
print('Modelo: I = Io (exp(V/VT) - 1)')
print('I0 = (', 1.e12 * round(popt[0],12), '+/-', 1.e12 * round(perr[0],13), ') 1e-12 A')
print('VT = (', 1000 * round(popt[1],5), '+/-', 1000 * round(perr[1],5), ') mV')

