"""
Lab3 - DF - FCEyN - UBA
2021 (pandemic)
editado por Matías Zanini 

"""

#%%

# cargamos las librerias de python que necesistmos:
import numpy as np
import matplotlib.pyplot as plt
import os
from IPython import get_ipython
from scipy.optimize import curve_fit
from scipy.optimize import least_squares


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

# Nombre del archivo obtenido de Analisis 2 señales osciloscopio.py ' ' con la terminación .txt incluida:

file_name = 'Salidatransferencia.txt'

Misdatos = np.loadtxt(file_name, delimiter=",",skiprows=0) 

# Ordeno los datos con la frecuencia:
Misdatos1 = Misdatos[np.argsort(Misdatos[:, 4])]


# Desempaquetamos los datos:
    
T= Misdatos1[:,0] # Transferencia
errorT = Misdatos1[:,1] # incertidumbre de T
fase= Misdatos1[:,2] # valores de dif fase en radianes
errorfase=Misdatos1[:,3] # valores de incertidumbre de la fase
fase_grad= 180*(Misdatos1[:,2])/(np.pi) # lee y convierte valores de dif fase en grados
errorfase_grad=180*(Misdatos1[:,3])/(np.pi) # lee y convierte valores de incertidumbre de la fase
frec=Misdatos1[:,4] # v alores de la frecuencia (Hz)
errorfrec=Misdatos[:,5] # incertidumbre de la frecuencia
T_db=20*np.log10(T) # Atenuación en dB
errorT_db=20*(Misdatos1[:,1])/(Misdatos1[:,0])


plt.ion()

plt.close("all")
#Grafico los datos del archivo
plt.figure(1)
plt.errorbar(frec,T,xerr=errorfrec,yerr=errorT,fmt=".b", linestyle='dotted')
plt.axhline(1, color='black', linestyle='dashed', linewidth=0.5)
plt.axhline(0, color='black', linestyle='dashed', linewidth=0.5)
plt.axhline(1/np.sqrt(2), color='green', linestyle='dashed', linewidth=1.5)
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xscale('log')
plt.xlabel('Frecuencia (Hz)', size=15)
plt.ylabel('Transferencia', size=15)
#plt.legend(loc=3,prop={'size':12}, ncol=1, shadow=True, fancybox=True, title = "$\omega$ (rad/s)") #coloca las etiquetas en la mejor posición posible
plt.show()

plt.figure(2)
plt.errorbar(frec,T_db,xerr=errorfrec,yerr=errorT_db,fmt=".b", linestyle='dotted')
plt.axhline(-3, color='green', linestyle='dashed', linewidth=1.5)
plt.axhline(0, color='black', linestyle='dashed', linewidth=0.5)
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
#plt.xscale('log')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Atenuación (dB)')
plt.show()

plt.figure(3)
plt.errorbar(frec,fase_grad,xerr=errorfrec,yerr=errorfase_grad,fmt=".b")
plt.axhline(45, color='green', linestyle='dashed', linewidth=1.5)
plt.axhline(0, color='black', linestyle='dashed', linewidth=0.5)
plt.axhline(90, color='black', linestyle='dashed', linewidth=0.5)
plt.axhline(-45, color='green', linestyle='dashed', linewidth=1.5)
plt.axhline(-90, color='black', linestyle='dashed', linewidth=0.5)
#plt.grid('on');
#plt.axis([0,2,0,3.5]) #elijo el rango para el eje x del gráfico
plt.xscale('log')
plt.ylim(-360, 360)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$\Delta$ Fase (°)')
plt.show()



#%%

pasabajos = False # Poner True si es pasabajos o False si es pasaaltos.


#
# Definimos aquí la función que vamos a usar para el ajuste (Yteo)
# por ej: 

def Yteo0(xx0, a):
    
    pb = pasabajos
    
    if pb:    
    
        y= 1/(np.sqrt(1+np.square(xx0/np.abs(a)))) #pasabajos
    
    else:
    
        y= 1/(np.sqrt(1+np.square(np.abs(a)/xx0))) #pasaaltos
    return y

# Los datos de la fase y la atenuación no se ajustan con curve_fit y requieren de least_squares

def Yteo1(xx1, b):
    
    pb = pasabajos
    
    if pb:
    
        y= -180/(np.pi)*(np.arctan(xx1/np.abs(b))) #pasabajos
    
    else:
    
        y= 180/(np.pi)*(np.arctan(np.abs(b)/xx1))   #pasaaltos
    
    return y

def get_residuals1(frec, Fase, b):
  Yteos11 = Yteo1(frec, b)
  residuals1 = np.abs(Yteos11 - Fase)
  return residuals1


def Yteo2(xx2, c):
    
    pb = pasabajos
    
    if pb:
        
        y= -10*np.log10(1+np.square(xx2/np.abs(c))) #pasabajos
    
    else:
        
        y= -10*np.log10(1+np.square(np.abs(c)/xx2))  #pasabaltos
    
    return y

def get_residuals2(frec, Atenua, c):
  Yteos22 = Yteo2(frec, c)
  residuals2 = np.abs(Yteos22 - Atenua)
  return residuals2


popt0, pcov0 = curve_fit(Yteo0, frec,T)
perr0 = np.sqrt(np.diag(pcov0)) # errores de 1 sigma
Yteos0=Yteo0(frec,*popt0) # Calculamos los puntos teóricos usando la función Yteo y los parámetros obtenidos del ajuste 

popt2, pcov2 = curve_fit(Yteo2, frec,T_db)
perr2 = np.sqrt(np.diag(pcov2)) # errores de 1 sigma
Yteos2=Yteo2(frec,*popt2) # Calculamos los puntos teóricos usando la función Yteo y los parámetros obtenidos del ajuste 

#Guess parameters para los otros ajustes // Usamos least_squares cuando el ajuste mediante curve_fit no es bueno
guess_frec0 = popt0



#Performing the fit
res_lsq1 = least_squares(get_residuals1, guess_frec0, args=(fase,frec), method='trf')
#res_lsq2 = least_squares(get_residuals2, guess_frec0, args=(T_db,frec), method='trf')

#Fit results
best_parameters1 = res_lsq1['x']
Yteos1 = Yteo1(frec, best_parameters1)

#best_parameters2 = res_lsq2['x']
#Yteos2 = Yteo2(frec, best_parameters2)


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

pcov1 = calcular_cov(res_lsq1,fase)
pstd1 =np.sqrt(np.diag(pcov1))

#pcov2 = calcular_cov(res_lsq2,T_db)
#pstd2 =np.sqrt(np.diag(pcov2))

print()
print('F0 derivado de los datos de la Transferencia:')
print('('+ str(round(popt0[0],1)) + ' ±' + str(round(perr0[0],1)) +') Hz')
print()
print('F0 derivado de los datos de la Atenuación:')
#print('('+ str(round(best_parameters2[0],1)),'  ± ',str(round(pstd2[0],1)) +') Hz')
print('('+ str(round(popt2[0],1)),'  ± ',str(round(perr2[0],1)) +') Hz')
print()
print('F0 derivado de los datos de la fase:')
print('('+ str(round(best_parameters1[0],1)),'  ± ', str(round(pstd1[0],1)) +') Hz')




plt.figure(4)
plt.errorbar(frec,T,xerr=errorfrec,yerr=errorT,fmt=".b", label='exp') #grafico valores medidos
plt.plot(frec, Yteos0, linestyle='solid', color = 'red', linewidth = 2.0, label='Ajuste') # Ajuste
plt.xscale('log')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Transferencia')
plt.legend()
plt.title('F$_0$ = ('+ str(round(popt0[0],1)) + ' ±' + str(round(perr0[0],1)) +') Hz')
plt.show()


plt.figure(5)
plt.errorbar(frec,T_db,xerr=errorfrec,yerr=errorT_db,fmt=".b", label='exp') #grafico valores medidos
plt.plot(frec, Yteos2, linestyle='solid', color = 'red', linewidth = 2.0, label='fit') # Ajuste
#plt.xscale('log')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Atenuación (dB)')
plt.legend()
#plt.title('Atenuación: F$_0$ = (' + str(round(best_parameters2[0],1)) + '  ± ' + str(round(pstd2[0],1)) +') Hz')
plt.title('F$_0$ = (' + str(round(popt2[0],1)) + '  ± ' + str(round(perr2[0],1)) +') Hz')
plt.show()


plt.figure(6)
plt.errorbar(frec,fase_grad,xerr=errorfrec,yerr=errorfase_grad,fmt=".b", label='exp') #grafico valores medidos
plt.plot(frec, Yteos1, linestyle='solid', color = 'red', linewidth = 2.0, label='Ajuste') # Ajuste
plt.xscale('log')
plt.ylim(-5,95)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$\Delta$ Fase (°)')
plt.legend()
plt.title('F$_0$ = (' + str(round(best_parameters1[0],1)) + '  ± ' + str(round(pstd1[0],1)) +') Hz')
plt.show()







