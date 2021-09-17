# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:31:07 2020

@author: Lab 3 - DF - FCEyN - UBA
editado por Matías Zanini 
Análisis de tres señales senoidales ajuste de amplitud, valor de offset, frecuencia y fase inicial.
Los parámetros de ajuste de las tres señales se obtienen en un archivo de salida txt
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
os.chdir (r'D:/nuestras carpetas/Mati/Ayudante/UBA/Labo 3 - 2C 2021/prácticas/Mediciones AC/')


# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:

file_name = 'prueba_5.txt'

#Extraigo los datos del archivo

data = np.loadtxt(file_name,dtype=float,delimiter = ',',skiprows= 1)

#Obtenemos los datos del archivo para señal 1 y señal 2

x1i = data[:,0] # Tiempo de la señal V1  
y1i = data[:,1] # V1

x2i  =data[:,0] # Tiempo de la señal V2   
y2i = data[:,2] # V2

'''
Si la señal es menor a 1 LSB OJO CON ARDUINO! Están saturando por debajo
y podrían estar mandando una señal negativa a la entrada analógica de 
Arduino. 
Con el siguiente if, saldrá una advertencia para que chequeen su circuito.
'''

if min(y1i) < 1.1/1023 or min(y2i) < 1.1/1023:
    
    print('OJO CON ARDUINO!!!! Posible saturación por debajo de 0V.')


#%% ------ Acondicionamiento de la señal y Gráfico de los datos crudos------------------------------

'''
Dado que arduino mide por tandas y luego espera 5 segundos es altamente 
probable que, entre medición y medición, observen saltos abruptos o 
"discontinuidades" en la señal. 

Esto es esperable, ya que habría que tener
muchísima suerte para hacer coincidir cada inicio de medición, con el mismo 
valor en que terminó la medición anterior.

El siguiente bloque de código, nos permitirá encontrar automáticamente
el inicio de nuestra tanda de medición y restringirá los datos para quedarnos 
únicamente con ella, sin ver la anterior con su respectivo salto.
'''

j=1 # Inicializo la variable j que nos servirá como contador de cada punto de la señal

# Inicializo otras variables que utilizaremos:
datoinicial1 = 0
datofinal1 = 0
dif = 0
N = len(x1i) # Esta variable guarda el largo del vector tiempo.  


'''
En el próximo while, haremos lo siguiente. Recorreremos toda la señal x1i 
que contiene el tiempo de la medición (lo vemos como una rampa en el serial 
plot) punto por punto y calcularemos la diferencia entre un punto y el 
siguiente.

Luego, si encontramos que dos puntos consecutivos de la señal están separados
en más de 0.001 s, sabremos que la misma pegó un salto (pues comenzamos a
medir nuevamente y el tiempo vuelve a 0).

Cuando esto ocurra, saldremos del while y la variable j tendrá guardado el 
índice del punto donde ocurrió este salto.
 
Ese valor de j será el que tomemos como nuestro dato inicial para la medición.
'''

while dif<0.001 and j< N-1:   
    
    j=j+1 # Le suma uno a la variable j y la sobreescribe. 
    
    dif = abs(x1i[j-1])-abs(x1i[j]) 
    
    '''
    NOTA: en python, la línea 
    
    j=j+1
    
    puede también escribirse como
    
    j+=1
    
    ambas hacen lo mismo: incrementar el valor de la variable j en 1.
    '''
        

else:
    if (j == N-1):
      datoinicial1=0 # Si j llegó al final del archivo sin ver saltos, nos quedamos con todo.
    else:
      datoinicial1=j # Sino, nos quedamos con ese j.


# Si el primer tiempo es menor a 0.0001, tomaremos ese como inicial.
if (x1i[0]<0.0001): 
    
    datoinicial1=0
    
    j=0
   
'''
Hasta esta parte del código, en la variable datoinicial1 debería estar 
guardado el índice del inicio de nuestra tanda de medición.

Veamos ahora el final de la tanda:
'''

dif = 0 # Reiniciamos la variable dif
j=j+1 # Vamos al siguiente j luego del inicio de la tanda.

'''
Ahora hacemos lo mismo que antes pero partiendo del siguiente j al inicial.
'''
  
while dif<0.001 and j<N-1 and x1i[j]>=0:
    j=j+1
    dif=(x1i[j-1])-(x1i[j])
else:
    datofinal1=j-1


# Ahora si, restringimos nuestra medición al intervalo de una sola tanda:
x1 = x1i[datoinicial1:datofinal1]  
y1 = y1i[datoinicial1:datofinal1]

x2 = x2i[datoinicial1:datofinal1]  
y2 = y2i[datoinicial1:datofinal1]


# Grafico los datos seleccionados para analizar
plt.ion()
plt.close("all")
plt.figure(1)
plt.plot(x1, y1,'.-g', label='1');
plt.plot(x2, y2,'.-b', label='2');
#plt.plot(x3, y3,'.-r', label='3');
#plt.grid('on');
plt.xlabel('tiempo (s)');
plt.ylabel('Voltaje (V)');
plt.legend()

# Tomamos los parámetros de la señal estimados por Arduino:
frec1=data[datofinal1-60,5]
w1=2*np.pi*frec1
Amplitud1=data[datofinal1-20,3]
Tauest=1/frec1
w2=2*np.pi*frec1
Amplitud2=data[datofinal1-20,4]


j=0
while x1[j]<=x1[0]+Tauest:
    j=j+1
else:
    datofinalper=j

# Armamos vectores con las señales restringidas a un solo período (según el período dado por Arduino):    
x1perest=x1[0:datofinalper]
y1perest=y1[0:datofinalper]
y2perest=y2[0:datofinalper]

valormedio1 = np.mean(y1perest)
valormedio2 = np.mean(y2perest)

# Buscamos el índice para el cual las señales son máximas:
jmax1 = np.where(y1perest==np.max(y1perest))[0][0]
jmax2 = np.where(y2perest==np.max(y2perest))[0][0]

# Definimos la fase, considerando la señal como un coseno:
    
T11 = x1perest[jmax1] # Tiempo donde la señal es máxima. Indica cuan desplazado está el coseno.
T21 = x1perest[jmax2] # Tiempo donde la señal es máxima. Indica cuan desplazado está el coseno.

fase1=-w1*T11 # Cuánto hay que correr a un coseno para obtener la señal que tenemos.
fase2=-w1*T21 

print()

print("frecuencia1 (Hz)=",frec1,"fase1 (rad)=",fase1,",Amplitud1 (V)=",round(Amplitud1,2),",valormedio (V)=",round(valormedio1,2))

print()

print("frecuencia2 (Hz)=",frec1,"fase2 (rad)=",fase2,",Amplitud2 (V)=",round(Amplitud2,2),",valormedio (V)=",round(valormedio2,2))

print()


#%% --------------------------- Ajuste por cosenos ---------------------------------------------

'''
Muchas veces, el éxito de un ajuste a los datos mediante una función dada, 
depende fuertemente de que le demos al algoritmo una "ayudita". 
Esto es, proveerle al algoritmo de ajuste, un conjunto de suposiciones (guess)
de los parámetros que esperamos encontrar. 

Así, el algoritmo no comienza a iterar "a ciegas" desde valores arbitrarios
para los parámetros, sino que comienza la búsqueda mucho más cerca del 
resultado óptimo.

En este caso, el programa de Arduino, provee dichos guess que podemos darle
al algoritmo. Sin embargo, podría pasar que durante su obtención, Arduino
se equivoque y el ajuste no funcione.

Si este fuera el caso, pueden probar descomentar el bloque de código titulado
"obtención alternativa de guess para el ajuste". Dicho bloque, intentará 
obtener los guess para el ajuste directamente de la señal que midieron.  
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

#Guess parameters
guess_amplitude1 = Amplitud1
guess_omega1 = w1 
guess_offset1 = valormedio1
guess_phi1 = fase1
guess_parameters1 = [guess_amplitude1, guess_omega1, guess_offset1, guess_phi1]

'''
Si el ajuste dio mal, probar descomentar el siguiente bloque y otro que se
encuentra más abajo.
Luego, ejecutar nuevamente código desde el bloque siguiente:
'''  
# #%% --------------- Obtención alternativa de guess para el ajuste ------------------------

# def periodo(t_señal, señal, percent_tol = 5, separacion_max = 5):
    
#     '''
#     Esta función calcula el período y la cantidad de puntos en un período de
#     una señal sinusoidal. Para ello, explora un rango alrededor de los máximos
#     dado por una tolerancia porcentual de la amplitud. Luego establece los
#     picos de la señal y calcula el período como la diferencia entre dos 
#     consecutivos.
#     '''
    
#     inds_max = [i for i in range(len(señal)) 
#                 if max(señal)*(1-percent_tol/100)<=señal[i]<=max(señal)*(1+percent_tol/100)]

#     ind_periodos = [i+1 for i in range(len(inds_max)-1) 
#                     if (inds_max[i+1]-inds_max[i])>separacion_max ]
    
#     periodos = [round(np.mean(inds_max[:ind_periodos[0]]))]
    
#     if len(ind_periodos)>1:
    
#         tuplas_per = [(ind_periodos[i],ind_periodos[i+1]) for i in range(len(ind_periodos)-1)]
        
#         for tupla in tuplas_per:
            
#             periodos.append(round(np.mean(inds_max[tupla[0]:tupla[1]])))
        
#         periodos.append(round(np.mean(inds_max[tuplas_per[-1][1]:])))
    
#     else:
        
#         periodos.append(round(np.mean(inds_max[ind_periodos[0]:])))
    
    
#     tper = np.mean([(t_señal[periodos[i+1]]-t_señal[periodos[i]]) for i in range(len(periodos)-1)])

#     iper = round(np.mean([(periodos[i+1]-periodos[i]) for i in range(len(periodos)-1)]))
    
#     return tper, iper

# tper, iper = periodo(x1,y1)

# guess_amplitude1 = (max(y1)-min(y1))/2
# guess_omega1 = 2*np.pi/tper
# guess_offset1 = valormedio1
# guess_phi1 = fase1
# guess_parameters1 = [guess_amplitude1, guess_omega1, guess_offset1, guess_phi1]



# Ajuste para la señal V1:
res_lsq1 = least_squares(get_residuals, guess_parameters1, args=(y1,x1),method='trf')

#Fit results
best_parameters1 = res_lsq1['x']

# Creamos un dominio con muchos puntos para la función fiteada:
x1_fit = np.linspace(x1[0],x1[-1],1000)

fitted_function1 = cos_fit_fun(best_parameters1, x1_fit)

pcov1 = calcular_cov(res_lsq1,y1)


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
plt.scatter(x1, y1,label='data1')
plt.plot(x1_fit, fitted_function1, color = 'red', linewidth = 2.0, label='fit')
N=len(x1)
plt.xlim(x1[0],x1[N-1])
plt.xlabel("tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title('~'+str(round(best_parameters1[1]/(2*np.pi),0))+' Hz')

#Guess parameters2
guess_amplitude2 = Amplitud2 #taken from plot above
guess_omega2 = w2 
guess_offset2 = valormedio2
guess_phi2 = fase2
guess_parameters2 = [guess_amplitude2, guess_omega2, guess_offset2, guess_phi2]


# Descomentar lo siguiente si se corre la obtención alternativa de guess:

# tper2, iper2 = periodo(x2,y2)
# guess_amplitude2 = (max(y2)-min(y2))/2
# guess_omega2 = 2*np.pi/tper2
# guess_offset2 = valormedio2
# guess_phi2 = fase2
# guess_parameters2 = [guess_amplitude2, guess_omega2, guess_offset2, guess_phi2]





# Ajuste para la señal V2:
res_lsq2 = least_squares(get_residuals, guess_parameters2, args=(y2,x2))

pcov2 = calcular_cov(res_lsq2,y2)
pstd2 =np.sqrt(np.diag(pcov2))

#Fit results
best_parameters2 = res_lsq2['x']

# Creamos un dominio con muchos puntos para la función fiteada:
x2_fit = np.linspace(x2[0],x2[-1],1000)

fitted_function2 = cos_fit_fun(best_parameters2, x2_fit)
print("PARAMETROS DEL AJUSTE DEL CANAL 2")
print('Best Amplitude2: ' ,round(best_parameters2[0],3),'  ± ',round( pstd2[0],3))
print('Best frec2: ' ,round(best_parameters2[1]/(2*np.pi),3),'  ± ',round( pstd2[1]/(2*np.pi),3))
print('Best offset2: ',round(best_parameters2[2],3),'  ± ',round( pstd2[2],3))
print('Best Phi2: ' ,round(best_parameters2[3],3),'  ± ',round( pstd2[3],3))
print()
plt.scatter(x2, y2,label='data2')
plt.plot(x2_fit, fitted_function2, color = 'blue', linewidth = 2.0, label='fit')

difPhi=round(best_parameters2[3]-best_parameters1[3],2) 
print("Diferencia de fase entre 1 y 2 en radianes=",difPhi," (",round(difPhi*180/np.pi,2),"grados )" )


#graficamos la figura de Lissajous, tomamos más puntos para graficar las señales
N=len(x1)
x1f=np.arange(x1[0],x1[N-1],step=(x1[N-1]-x1[0])/500)
V1fit = cos_fit_fun(best_parameters1, x1f)
V2fit = cos_fit_fun(best_parameters2, x1f)

plt.figure(3)
plt.plot(V1fit, V2fit, color = 'red', linewidth = 1.0)
plt.xlabel("Voltaje 1 (V)")
plt.ylabel("Voltaje 2 (V)")
plt.title('Figura de Lissajous'+'  '+ str(round(best_parameters1[1]/(2*np.pi),0))+' Hz'+'  '+str(round(difPhi*180/np.pi,0))+' grados')
