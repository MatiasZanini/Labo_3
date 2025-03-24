# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 16:25:57 2025

@author: Publico
"""

import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt

#%%

# inicializo comunicacion con equipos
rm = visa.ResourceManager()
#lista de dispositivos conectados, para ver las id de los equipos
rm.list_resources()


#%% Generador de funciones AFG1022

#inicializo generador de funciones
fungen = rm.open_resource('USB0::0x0699::0x0353::1625695::INSTR')
#le pregunto su identidad
fungen.query('*IDN?')

#le pregunto la freq
fungen.query('SOUR1:FREQ?')
#le seteo la freq
fungen.write('SOUR1:FREQ 2000')

#le pregunto la amplitud
fungen.query('SOUR1:VOLT?')
#le seteo la amplitud
fungen.write('SOUR1:VOLT 2')
fungen.query('SOUR1:VOLT?')
#le pregunto si la salida esta habilitada
fungen.query('OUTPut1:STATe?')
#habilito la salida
fungen.write('OUTPut1:STATe 1')
fungen.query('OUTPut1:STATe?')
#le pregunto la impedancia de carga seteada
fungen.query('OUTPUT1:IMPEDANCE?')


#%% Osciloscopio TBS1000C

#inicializo el osciloscopio
osci = rm.open_resource('USB0::0x0699::0x03C4::C010503::INSTR')
#le pregunto su identidad
osci.query('*IDN?')
#le pregunto la conf del canal (1|2)
osci.query('CH1?')
#le pregunto la conf horizontal
osci.query('HOR?')
#le pregunto la punta de osciloscopio seteada
osci.query('CH2:PRObe?')



#Seteo de canal
channel=1
scale = 1
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.query("CH{0}:SCA?".format(channel))
"""escalas Voltaje (V) ojo estas listas no son completas
2e-3
5e-3
10e-3
20e-3
50e-3
100e-3
5e-2
10e-2
"""

zero = 0
osci.write("CH{0}:POS {1}".format(channel, zero))
osci.query("CH{0}:POS?".format(channel))

channel=2
scale = 2e-1
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.write("CH{0}:POS {1}".format(channel, zero))

#seteo escala horizontal
scale = 200e-6
osci.write("HOR:SCA {0}".format(scale))
osci.write("HOR:POS {0}".format(zero))	
osci.query("HOR?")
"""
escalas temporales (s)

10e-9
25e-9
50e-9
100e-9
250e-9
500e-9
1e-6
2e-6
5e-6
10e-6
25e-6
50e-6

"""

#Seteamos el canal del que queremos obtener la curva:
ch = 1

osci.write('DATA:SOUR CH{}'.format(ch))

#Comprobamos:
osci.query('DATA:SOUR?')


#le pido los valores de la pantalla (0:255)
data = osci.query_binary_values('CURV?', datatype='B',container=np.array)
plt.plot(data)

#le pido los parametros de la pantalla
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
xze
xin
voltaje = (data - yoff) * ymu + yze 
tiempo = xze + np.arange(len(data)) * xin

plt.plot(tiempo,voltaje)


#%% Medimos las dos curvas
    
#frenamos la adquisición para medir las dos curvas al mismo tiempo:
osci.write('ACQ:STATE OFF')

datos = []

for ch in [1,2]:
    
    osci.write('DATA:SOUR CH{}'.format(ch))
    
    data = osci.query_binary_values('CURV?', datatype='B',container=np.array)
    
    xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')
    
    voltaje = (data - yoff) * ymu + yze 
    tiempo = xze + np.arange(len(data)) * xin
    
    datos.append([tiempo,voltaje])
    time.sleep(0.1)
    
osci.write('ACQ:STATE ON')
    
t1 = datos[0][0]
v1 = datos[0][1]

t2 = datos[1][0]
v2 = datos[1][1]

plt.plot(t1,v1, label='Señal canal 1')
plt.plot(t2,v2, label='Señal canal 2')
plt.legend()


#%% Mediciones instantáneas

ch = 1

osci.write('MEASU:IMM:SOU CH{}'.format(ch))

osci.query('MEASU:IMM:SOU?') #chequeamos

osci.query('MEASU:IMM:TYP?') # qué está midiendo?

# que quiero medir?:
    
'''
{AMPlitude|AREa|BURst|CARea|CMEan|CRMs|DELay|FALL|FREQuency
|HIGH|LOW|MAXimum|MEAN|MINImum|NDUty|NEDGECount|NOVershoot |NPULSECount|NWIdth|
PEDGECount|PDUty |PERIod|PHAse|PK2Pk|POVershoot|PPULSECount|PWIdth|RISe|RMS}
'''

tipo = 'PHA'

osci.write('MEASU:IMM:TYP {}'.format(tipo))    
    
osci.query('MEASU:IMM:VAL?')    
    
#si lo quiero como número flotante:
    
medida = float(osci.query('MEASU:IMM:VAL?'))

#IMPORTANTE: Si tienen problemas para pasar el string a float usar el siguiente comando:
osci.write('HEAD OFF') #Esto le quita las letras iniciales a la respuesta, permitiendo pasarla a float


print(medida)

#%% Mediciones persistentes (aparecen en la pantalla del osciloscopio)

med = 1 #numero del slot donde colocamos un tipo de medicion (de 1 a 6)

osci.query('MEASU:MEAS{}?'.format(med)) # Preguntamos qué se está midiendo en ese slot

osci.query('MEASU:MEAS{}:STATE?'.format(med)) # Vemos si está prendida o apagada
osci.write('MEASU:MEAS{}:STATE ON'.format(med)) #La prendemos si hace falta


ch_fuente1 = 1 #Sobre qué canal se toma la medición
ch_fuente2 = 2 #Sobre qué canal se toma una medición relativa respecto de la 1 (por ejemplo, la fase)

osci.write('MEASU:MEAS{}:SOU1 CH{}'.format(med,ch_fuente1)) 
osci.write('MEASU:MEAS{}:SOU2 CH{}'.format(med,ch_fuente2))


osci.query('MEASU:MEAS{}:TYP?'.format(med)) # qué está midiendo?

# que quiero medir?:
    
'''
{AMPlitude | AREa | BURst | CARea | CMEan | CRMs | DELay
| FALL |FREQuency | HIGH | LOW | MAXimum | MEAN | MINImum | NDUty | NEDGECount
| NOVershoot | NPULSECount|NWIdth | PDUty | PEDGECount | PERIod | PHAse | PK2Pk |
POVershoot | PPULSECount | PWIdth | RISe | RMS}
'''

tipo = 'PHA'

osci.write('MEASU:MEAS{}:TYP {}'.format(med,tipo)) #seteamos qué queremos medir  
    
osci.query('MEASU:MEAS{}:VAL?'.format(med)) #Le pido que me diga cuanto vale la medicion    
    
#si lo quiero como número flotante:
    
medida = float(osci.query('MEASU:MEASU{}:VAL?'.format(med)))

#IMPORTANTE: Si tienen problemas para pasar el string a float usar el siguiente comando:
osci.write('HEAD OFF') #Esto le quita las letras iniciales a la respuesta, permitiendo pasarla a float

print(medida)






#%% Autoajustar el trigger y escala

osci.write('AUTOSET:ENABLE ON')


osci.write('AUTOSET EXEC')


#%% Apagar o prender un canal
ch=1
osci.write('SELECT:CH{} OFF'.format(ch)) #apaga el canal
osci.write('SELECT:CH{} ON'.format(ch)) #prende el canal



#%%
#IMPORTANTE: al finalizar la medición, hay que cerrar la comunicación

osci.close()
fungen.close()
    
'''
Link muy útil: https://github.com/fainsteinf/laboratorio3/tree/main

Repositorio del JTP del curso de verano de Labo 3 2025, Facundo Fainstein.
Contiene códigos útiles para el manejo de los instrumentos y tiene 
comandos para comunicarse con los generadores de funciones SIGLENT.

'''
    
    
    
    
    
    
    
    
    


