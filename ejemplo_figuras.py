# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 18:00:34 2025

@author: Mati
"""

import matplotlib.pyplot as plt
import numpy as np
from IPython import get_ipython

#%% ------------------------ Elegir modo de salida de los gráficos -----------------------------------
'''
Descomentar la línea que corresponda. 
Si quieren que las figuras aparezcan en la terminal: inline 
Si quieren que las figuras aparezcan en una ventana emergente: qt5
'''
# get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')



#%%  Figura sencilla

# nos armamos unos datos de ejemplo

t = np.linspace(0, 2*np.pi, 100)
data1 = np.sin(t)
data2 = np.cos(t)


# Gráfico simple
plt.figure(figsize=(9, 8)) # ancho, alto
plt.plot(t, data1,'.-', label='Seno')
plt.plot(t, data2, 'o', label='Coseno')

# Etiquetas, grilla, leyenda, configuramos los ticks del grafico, etc.
plt.xlabel('tiempo [s]',fontsize=18)
plt.ylabel('data',fontsize=18)
plt.legend(fontsize=16)
plt.grid(axis='y', linestyle='--')
plt.tick_params(axis='both', which='both', length=4, width=2, labelsize=16)
# plt.tight_layout() # Ajusta la figura dentro del tamaño de la ventana para que no se corten las etiquetas de los ejes.
plt.show()

#%% Más ejemplos de configuraciones posibles

plt.figure(figsize=(9, 8))
plt.plot(t, data1, color='blue', linestyle='--', marker='o', label='Seno')
plt.plot(t, data2, color='red', linestyle='-', marker='x', label='Coseno')

plt.title('Gráfico de ejemplo') # En informes no se usa
plt.xlabel('tiempo [s]', fontsize=18)
plt.ylabel('data', fontsize=18)
plt.legend(loc='upper right', fontsize=16) # podemos fijar la posición donde aparece
plt.grid(True, which='both', linestyle=':', linewidth=0.7)
plt.tick_params(axis='both', which='both', length=4, width=2, labelsize=16)

plt.xlim(0, 2*np.pi)
plt.ylim(-1.5, 1.5)
plt.show()

#%% Comparar varios gráficos en una misma figura.

'''
Todas las configuraciones anteriores valen para cada gráfico por separado.
Pueden ponerlas debajo de cada plt.plot
'''

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(t, data1, color='blue')
plt.title('Seno')

plt.subplot(1, 2, 2)
plt.plot(t, data2, color='red')
plt.title('Coseno')

plt.suptitle('Método sencillo para comparar figuras')
plt.show()

#%% Método más flexible para armar subplots

'''
En este método, nos crearemos un objeto de python que contiene los gráficos
que vamos a crear, llamado axs. 
A ese objeto le podemos agregar los datos agraficar, las propiedades 
que pusimos anteriormente, etc.
'''


fig, axs = plt.subplots(1, 2, figsize=(16, 6))

axs[0].plot(t, data1, color='blue')
axs[0].set_title('Seno')
axs[0].set_xlabel('tiempo [s]',fontsize=18)
axs[0].set_ylabel('data',fontsize=18)
axs[0].tick_params(axis='both', which='both', length=4, width=2, labelsize=15)

axs[1].plot(t, data2, color='red')
axs[1].set_title('Coseno')
axs[1].set_xlabel('tiempo [s]',fontsize=18)
axs[1].set_ylabel('data',fontsize=18)
axs[1].tick_params(axis='both', which='both', length=4, width=2, labelsize=15)

fig.suptitle('comparación usando subplots',fontsize=20)
plt.show() # Muestra la figura


#%% Una utilidad para subplots: un solo grafico con dos ejes y distintos

data3 = np.cos(t) * 100  # se nos iría de escala en un mismo gráfico

fig, ax1 = plt.subplots(figsize=(9, 8))

# Primer eje Y
ax1.plot(t, data1, color='blue', label='Seno')
ax1.set_xlabel('tiempo [s]',fontsize=18)
ax1.set_ylabel('Seno', color='blue',fontsize=18)
ax1.tick_params(axis='y', labelcolor='blue', length=4, width=2, labelsize=15)
ax1.tick_params(axis='x', length=4, width=2, labelsize=15)

# Segundo eje Y compartido
ax2 = ax1.twinx() # esto me genera un nuevo par de ejes, que comparten eje X.
ax2.plot(t, data3, color='red', label='Coseno $\times$ 100') # pueden usar latex en los ejes!
ax2.set_ylabel('Coseno x 100', color='red',fontsize=18)
ax2.tick_params(axis='y', labelcolor='red', length=4, width=2, labelsize=15)

plt.title('Gráfico con dos ejes Y diferentes que comparten el eje X', fontsize=20)
plt.show()

#%% Automatización del guardado de figuras


fig, ax = plt.subplots()
ax.plot(t, data1)
ax.set_title('Ejemplo Guardado')
ax.set_xlabel('tiempo [s]')
ax.set_ylabel('Seno')

# Guardar la figura
fig.savefig('figura_ejemplo.png', dpi=300) # Si no aclaran la ruta, lo guarda en el directorio de trabajo
plt.show()
