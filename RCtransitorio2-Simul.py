# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 18:49:57 2020

@author: User
"""

#%%
#Loading modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from IPython import get_ipython



#selecciono el grafico en Terminal (inline) o en ventana emergente (qt5)
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')

#%%

#Elijo el directorio donde se encuentran los archivos que voy a analiza
os.chdir (r'C:\Users\Cesar\Dropbox\Cursos\Lab3\Simulaciones\LTSpice\2021_C1\Transitorios')
#print("nombre del archivo completo con terminación .txt incluida")
#file = input()
file = 'Transitorio_RC_4.txt'
print("Valor de la R (ohm)")
Resist = float(input())

#Importo los datos del archivo
#data = np.loadtxt(file,dtype=float,delimiter = ',',skiprows= 1)
data = np.loadtxt(file,dtype=float,delimiter = '\t',skiprows= 1)



x1i = data[:,0] #columna de tiempo en segundos
y1i = data[:,2] #caida de tensión sobre el capacitor
y2i= (data[:,1]-data[:,2])/Resist   #corriente del circuito


#%% Gráfico de la tensión y corriente

plt.ion()
plt.close("all")
fig, ax1 = plt.subplots()
ax1.plot(x1i, y1i,'.-g');
ax1.set_ylabel('Tensión (V)', color='g', fontsize = 14);
ax1.set_xlabel('Tiempo (s)', fontsize = 14);
plt.grid('on')
ax2=ax1.twinx()
ax2.plot(x1i, y2i,'.-r')
ax2.set_ylabel('Corriente (A)', color='r', fontsize = 14)


#%% Ajuste de los resultados de la simulacion

# Tension sobre el capacitor
def tension1(time, c, d):
    #z= c*np.exp(-time*d)+Vfinal
    z = c*(1 - np.exp(-time*d))
    return z

xx1i = x1i[1:len(x1i)] # Tiempo
yy1i = y1i[1:len(y1i)] # Vc

plt.ion()
plt.figure(2)
plt.plot(xx1i, yy1i , 'g')
plt.grid('on')
plt.xlabel('Tiempo (s)', fontsize = 14)
plt.ylabel('Tensión (V)', color='g', fontsize = 14);

popt1, pcov1 = curve_fit(tension1, xx1i, yy1i)

perr1 = np.sqrt(np.diag(pcov1))



#%%

# Corriente en la malla
def corriente1(time, a, b):
    y = a*np.exp(-time*b)
    return y

xx1i = x1i[1:len(x1i)] # Tiempo
yy2i = y2i[1:len(y2i)] # Corriente

plt.ion()
plt.figure(3)
plt.plot(xx1i, yy2i , 'r')
plt.grid('on')
plt.xlabel('Tiempo (s)', fontsize = 14)
plt.ylabel('Corriente (A)', color='r', fontsize = 14);



popt2, pcov2 = curve_fit(corriente1, xx1i, yy2i)

perr2 = np.sqrt(np.diag(pcov2))

#%% Calculo de tau

tauVC=1/popt1[1]
taui=1/popt2[1]
deltatauVC=perr1[1]/popt1[1]*tauVC
deltataui=perr2[1]/popt2[1]*taui
print('Tiempo característico extraído de la tensión del condensador')
print('tau = (', round(tauVC,5), '+/-',  round(deltatauVC,5), ')s')
print('Tiempo característico extraído de la corriente')
print('tau = (', round(taui,5), '+/-',  round(deltataui,5), ') s')

#%%

#guardo los datos en un archiva de salida
fsalida=open('SalidaRCtransitorio.txt','a')
fsalida.write('%10.9f' %(tauVC)+',')
fsalida.write('%10.9f' % (deltatauVC)+',')
fsalida.write('%8.2f' % (Resist)+'\n')
#fsalida.write('%8.2f' % (0.01*Resist)+'\n')
fsalida.close()

