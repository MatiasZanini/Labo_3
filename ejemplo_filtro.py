

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#%% simulo un filtro butterworth

#defino variables del filtro
orden = 1
frec_corte = 1000

#armo el filtro en particular y obtengo sus parámetros
b, a = signal.butter(orden, frec_corte, 'low', analog=True)
# hago un análisis en frecuencias para el filtro con params a y b
w, h = signal.freqs(b, a)

#Ploteo
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Respuesta en frecuencia del filtro Butterworth')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.grid(which='both', axis='both')
plt.axvline(frec_corte, color='green',linestyle = '--') 
plt.show()


#%% cargo una señal medida (en el formato de numpy)

#cargo los datos
datos = np.load('espectro.npz')
#tengo que asignar una a una las variables que hay adentro
tiempo   = datos['tiempo']
medicion = datos['medicion']

#%% Implementación del filtro

fs = 1/np.mean(np.diff(tiempo)) # frecuencia de sampleo media 
cutoff = 20  # Hz
tipo = 'low'
orden_s1 = 20

orden_s2 = 1


#acá implemento el filtro y genero la señal filtrada
sos = signal.butter(orden_s1, cutoff, tipo, fs = fs, output='sos')
filtered = signal.sosfilt(sos, medicion)

sos = signal.butter(orden_s2, cutoff, 'low', fs = fs, output='sos')
filtered1 = signal.sosfilt(sos, medicion)

plt.close('all')
plt.figure(5)
plt.subplot(2,1,1)
plt.plot(tiempo , medicion, label = 'Señal original')
plt.plot(tiempo , filtered1, label = 'Señal filtrada (orden {})'.format(orden_s2))
plt.plot(tiempo , filtered, label = 'Señal filtrada (orden {})'.format(orden_s1))
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.grid(b=True)
plt.ylim(0.18,0.7)
plt.legend() #esto le pone leyenda al gráfico, mira lo que yo definí como "label" en cada curva


sos_high = signal.butter(1, cutoff, 'high', fs = fs, output='sos')
filtered_high = signal.sosfilt(sos_high, medicion)

#otra manera de implementarlo
#B, A           = signal.butter(4, 40 / (fs / 2), btype='high') 
#medicion_hig1  = signal.lfilter(B, A, medicion      , axis=0)
plt.subplot(2,1,2)
plt.plot(tiempo , filtered_high, label='Filtro pasa-altos')
plt.grid(b=True)
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.legend()
#plt.ylim(-0.05,0.05)

plt.tight_layout()


#%% Filtro una señal ruidosa creada por mi

#Señal ruidosa
x = np.linspace(0,5, num = 10000)
frec1 = 2
frec2 = 15
senhal = 10*np.cos(2*np.pi*frec1*x) + 10*np.cos(2*np.pi*frec2*x) 
noise = 2*np.random.normal(0,1,10000)

#plot de la señal con ruido
plt.plot(x,senhal + noise,'.-')
plt.grid(b=True)

#filtro
fs = 1/np.mean(np.diff(x)) # frecuencia de sampleo media 
cutoff = 30 # Hz
tipo = 'high'  # 'high' para pasa-altos y 'low' para pasa-bajos

sos = signal.butter(5, cutoff, tipo, fs = fs, output='sos')
filtered = signal.sosfilt(sos, senhal + noise)

#plot de la señal sin filtrar y filtrada
plt.plot(x,senhal + noise,'.-')
plt.plot(x, filtered,'.-')
plt.grid(b=True)





#%% Jugamos a romper una onda cuadrada

t = np.linspace(0,1,10000)

frec = 5 # Hz

señal = signal.square(2 * np.pi * frec * t)

fs = 1/np.mean(np.diff(t)) # frecuencia de sampleo media 

cutoff = 25  # Hz (podemos probar que pasa a frec, 3*frec, 5*frec)

tipo = 'low'

orden_s1 = 5

orden_s2 = 1


#acá implemento el filtro y genero la señal filtrada
sos = signal.butter(orden_s1, cutoff, tipo, fs = fs, output='sos')
filtered = signal.sosfilt(sos, señal)

sos = signal.butter(orden_s2, cutoff, 'low', fs = fs, output='sos')
filtered1 = signal.sosfilt(sos, señal)

plt.close('all')
plt.figure(5)
plt.subplot(2,1,1)
plt.plot(t , señal, label = 'Señal original')
plt.plot(t , filtered1, label = 'Señal filtrada (orden {})'.format(orden_s2))
plt.plot(t , filtered, label = 'Señal filtrada (orden {})'.format(orden_s1))
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.grid(b=True)

plt.legend() 











