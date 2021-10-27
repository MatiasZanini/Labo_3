# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:31:07 2020

@author: Lab 3 - DF - FCEyN - UBA
editado por Matías Zanini 
Análisis de dos señales senoidales ajuste de amplitud, valor de offset, frecuencia y fase inicial.


-------------- IMPORTANTE!! ------------------------------------------------

Los parámetros de ajuste de las señales se guardan en un ÚNICO archivo txt. 
Cada vez que corran el programa, los parámetros obtenidos mediante el ajuste se agregarán
al mismo archivo de texto. Al finalizar, quedará un archivo con todos los resultados de
transferencia, frecuencia y fase con sus respectivos errores, todos en forma de columnas. 

"""
#%%
# cargamos las librerias de python que necesistmos:
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
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
os.chdir (r'D:\nuestras carpetas\Mati\Ayudante\UBA\Labo 3 - 2C 2021\datos\datos pasaaltos')


# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:

file_name = '500.txt'

#Extraigo los datos del archivo

data = np.loadtxt(file_name,dtype=float,delimiter = ',',skiprows= 1)

#Obtenemos los datos del archivo para señal 1 y señal 2

t1 = data[:,0] # Tiempo de la señal V1  
V1 = data[:,1] # V1

t2  =data[:,0] # Tiempo de la señal V2   
V2 = data[:,2] # V2



#%% -------------------------- Gráfico de los datos crudos------------------------------


# Grafico los datos seleccionados para analizar
plt.ion()
plt.close("all")
plt.figure(1)
plt.plot(t1, V1,'.-g', label='1');
plt.plot(t2, V2,'.-b', label='2');
#plt.plot(x3, y3,'.-r', label='3');
#plt.grid('on');
plt.xlabel('tiempo (s)');
plt.ylabel('Voltaje (V)');
plt.legend()




#%% --------------------------- Ajuste por cosenos ---------------------------------------------

'''
Muchas veces, el éxito de un ajuste a los datos mediante una función dada, 
depende fuertemente de que le demos al algoritmo una "ayudita". 
Esto es, proveerle al algoritmo de ajuste, un conjunto de suposiciones (guess)
de los parámetros que esperamos encontrar. 

Así, el algoritmo no comienza a iterar "a ciegas" desde valores arbitrarios
para los parámetros, sino que comienza la búsqueda mucho más cerca del 
resultado óptimo.

'''

# Definimos las funciones para el ajuste y errores:

print()
def cos_fit_fun(parameters, time):
  a = parameters[0]
  omega = parameters[1]
  offset = parameters[2]
  phi = parameters[3]
  y = a * np.cos(omega * time + phi) + offset
  return y

def get_residuals(parameters, position_data, time_data):
  theoretical_function = cos_fit_fun(parameters, time_data)
  residuals = np.abs(theoretical_function - position_data)
  return residuals

# Calculamos la matriz de covarianza "pcov"
def calcular_cov(res,y_datos):
    U, S, V = np.linalg.svd(res.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(res.jac.shape) * S[0]
    S = S[S > threshold]
    V = V[:S.size]
    pcov = np.dot(V.T / S**2, V)

    s_sq = 2 * res.cost / (y_datos.size - res.x.size)
    pcov = pcov * s_sq
    return pcov


#%% --------------- Obtención alternativa de guess para el ajuste ------------------------

def periodo(t_señal, señal, percent_tol = 20, separacion_max = 100):
    
    '''
    Esta función calcula el período y la cantidad de puntos en un período de
    una señal sinusoidal. Para ello, explora un rango alrededor de los máximos
    dado por una tolerancia porcentual de la amplitud. Luego establece los
    picos de la señal y calcula el período como la diferencia entre dos 
    consecutivos.
    '''
    
    inds_max = [i for i in range(len(señal)) 
                if max(señal)*(1-percent_tol/100)<=señal[i]<=max(señal)*(1+percent_tol/100)]

    ind_periodos = [i+1 for i in range(len(inds_max)-1) 
                    if (inds_max[i+1]-inds_max[i])>separacion_max ]
    
    periodos = [round(np.mean(inds_max[:ind_periodos[0]]))]
    
    if len(ind_periodos)>1:
    
        tuplas_per = [(ind_periodos[i],ind_periodos[i+1]) for i in range(len(ind_periodos)-1)]
        
        for tupla in tuplas_per:
            
            periodos.append(round(np.mean(inds_max[tupla[0]:tupla[1]])))
        
        periodos.append(round(np.mean(inds_max[tuplas_per[-1][1]:])))
    
    else:
        
        periodos.append(round(np.mean(inds_max[ind_periodos[0]:])))
    
    
    tper = np.mean([(t_señal[periodos[i+1]]-t_señal[periodos[i]]) for i in range(len(periodos)-1)])

    iper = round(np.mean([(periodos[i+1]-periodos[i]) for i in range(len(periodos)-1)]))
    
    return tper, iper, periodos


# tper = periodo, iper = cant de puntos en un periodo, maxs = indices de los máximos:
tper, iper, maxs = periodo(t1,V1) 

guess_amplitude1 = (max(t1)-min(V1))/2
guess_omega1 = 2*np.pi/tper
guess_offset1 = np.mean(V1[maxs[0]:maxs[1]])
guess_phi1 = -2*np.pi/tper*t1[maxs[0]]
guess_parameters1 = [guess_amplitude1, guess_omega1, guess_offset1, guess_phi1]

# --------

# Ajuste para la señal V1:
res_lsq1 = least_squares(get_residuals, guess_parameters1, args=(V1,t1),method='trf')

#Fit results
best_parameters1 = res_lsq1['x']

# Creamos un dominio con muchos puntos para la función fiteada:
t1_fit = np.linspace(t1[0],t1[-1],1000)

fitted_function1 = cos_fit_fun(best_parameters1, t1_fit)

pcov1 = calcular_cov(res_lsq1,V1)


# De la matriz de covarianza podemos obtener los valores de desviación estándar
# de los parametros hallados
pstd1 =np.sqrt(np.diag(pcov1))

print("PARAMETROS DEL AJUSTE DEL CANAL 1")
print('Best Amplitude1: ' ,round(best_parameters1[0],3),'  ± ',round( pstd1[0],3))
print('Best frec1: ' ,round(best_parameters1[1]/(2*np.pi),3),'  ± ',round( pstd1[1]/(2*np.pi),3))
print('Best offset1: ',round(best_parameters1[2],3),'  ± ',round( pstd1[2],3))
print('Best Phi1: ' ,round(best_parameters1[3],3),'  ± ',round( pstd1[3],3))
print()




plt.figure(2)
plt.scatter(t1, V1,label='data1')
plt.plot(t1_fit, fitted_function1, color = 'red', linewidth = 2.0, label='fit')
N=len(t1)
plt.xlim(t1[0],t1[N-1])
plt.xlabel("tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title('~'+str(round(best_parameters1[1]/(2*np.pi),0))+' Hz')


tper2, iper2, maxs2 = periodo(t2,V2)
guess_amplitude2 = (max(V2)-min(V2))/2
guess_omega2 = 2*np.pi/tper2
guess_offset2 = np.mean(V2[maxs[0]:maxs[1]])
guess_phi2 = -2*np.pi/tper2*t2[maxs[0]]
guess_parameters2 = [guess_amplitude2, guess_omega2, guess_offset2, guess_phi2]



# Ajuste para la señal V2:
res_lsq2 = least_squares(get_residuals, guess_parameters2, args=(V2,t2))

pcov2 = calcular_cov(res_lsq2,V2)
pstd2 =np.sqrt(np.diag(pcov2))

#Fit results
best_parameters2 = res_lsq2['x']

# Creamos un dominio con muchos puntos para la función fiteada:
t2_fit = np.linspace(t2[0],t2[-1],1000)

fitted_function2 = cos_fit_fun(best_parameters2, t2_fit)
print("PARAMETROS DEL AJUSTE DEL CANAL 2")
print('Best Amplitude2: ' ,round(best_parameters2[0],3),'  ± ',round( pstd2[0],3))
print('Best frec2: ' ,round(best_parameters2[1]/(2*np.pi),3),'  ± ',round( pstd2[1]/(2*np.pi),3))
print('Best offset2: ',round(best_parameters2[2],3),'  ± ',round( pstd2[2],3))
print('Best Phi2: ' ,round(best_parameters2[3],3),'  ± ',round( pstd2[3],3))
print()
plt.scatter(t2, V2,label='data2')
plt.plot(t2_fit, fitted_function2, color = 'blue', linewidth = 2.0, label='fit')

difPhi=round(best_parameters2[3]-best_parameters1[3],2) 
print("Diferencia de fase entre 1 y 2 en radianes=",difPhi," (",round(difPhi*180/np.pi,2),"grados )" )


#graficamos la figura de Lissajous, tomamos más puntos para graficar las señales
N=len(t1)
t1f=np.arange(t1[0],t1[N-1],step=(t1[N-1]-t1[0])/500)
V1fit = cos_fit_fun(best_parameters1, t1f)
V2fit = cos_fit_fun(best_parameters2, t1f)

plt.figure(3)
plt.plot(V1fit, V2fit, color = 'red', linewidth = 1.0)
plt.xlabel("Voltaje 1 (V)")
plt.ylabel("Voltaje 2 (V)")
plt.title('Figura de Lissajous'+'  '+ str(round(best_parameters1[1]/(2*np.pi),0))+' Hz'+'  '+str(round(difPhi*180/np.pi,0))+' grados')


#%% guardamos los datos ajustados en un archivo txt

Trans= np.abs(best_parameters2[0]/best_parameters1[0])
errorTrans=(pstd2[0]/best_parameters2[0]+pstd1[0]/best_parameters1[0])*Trans
frec= best_parameters2[1]/(2*np.pi)
errorfrec=pstd2[1]/(2*np.pi)
diffase=best_parameters2[3]-best_parameters1[3]
errordiffase=pstd2[3]+pstd1[3]

fsalida=open('Salidatransferencia.txt','a')
fsalida.write('%10.3f' %(Trans)+',')
fsalida.write('%10.9f' % (errorTrans)+',')
fsalida.write('%8.2f' % (diffase)+',')
fsalida.write('%8.2f' % (errordiffase)+',')
fsalida.write('%8.2f' % (frec)+',')
fsalida.write('%8.2f' % (errorfrec)+'\n')
fsalida.close()
