# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:17:12 2021

@author: Mati
"""

import numpy as np
import matplotlib.pyplot as plt

# Creamos algunos datos para graficar:
    
'''
np.arange(xi, xf, paso) crea un array de numpy que empieza en xi, termina en
xf yendo de a pasos de tamaño "paso".
'''    
    
t = np.arange(0.01, 10.0, 0.01) 

data1 = np.exp(t) # Exponencial de t

data2 = np.sin(2 * np.pi * t) # seno de 2pi t

fig, ax1 = plt.subplots() # Creamos una figura y un conjunto de ejes x e y.

color = 'tab:red' # Definimos una variable con el color rojo.

ax1.set_xlabel('time (s)') # Le ponemos nombre al eje x

ax1.set_ylabel('exp', color=color) # Le ponemos nombre al eje y con color rojo.

ax1.plot(t, data1, color=color) # Pedimos que  grafique el primer par de ejes.

ax1.tick_params(axis='y', labelcolor=color) # Le ponemos color al eje y.

'''
Ahora creamos el segundo par de ejes. Para poder plotearlos en el mismo 
gráfico y comparar, vamos a querer que compartan el mismo eje x.
Esto lo hacemos con la propiedad .twinx() :
'''

ax2 = ax1.twinx()

color = 'tab:blue' # Definimos una variable con el color azul

ax2.set_ylabel('sin', color=color) # Le ponemos nombre al nuevo eje y.

'''
Ahora, como todavía no pedimos que nos muestre la figura, podemos pedirle
a python que grafique el segundo par de ejes x e y en la misma figura.
Hacemos esto con ax2.plot():
'''

ax2.plot(t, data2, color=color)

ax2.tick_params(axis='y', labelcolor=color) # Le ponemos color a la etiqueta.

fig.tight_layout()  # Ajustamos la figura para que no se nos corte el eje y.

plt.show() # Mostramos el gráfico.









