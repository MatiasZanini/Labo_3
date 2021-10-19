# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:51:54 2019

@author: Matías Zanini
"""

from osciloscopio_tek import osciloscopio_tek as tek
import time
from glob import glob
import numpy as np

#%%

#reload(osciloscopio_tek)


#%%-----------------------------Inicializar osciloscopio------------------------------------------ 

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado (installar NI VISA y 
#TEK VISA).
resource_name = 'USB::0x0699::0x0365::C020269::INSTR'


#inicializamos la comunicacion

osci = tek(resource_name)

osci.adquirir()

print('Datos del osciloscopio:', osci.identificar())

modo, prom, est, fren = osci.modo_adq()

print('Modo:', modo, ', Promediado:', prom, ', Estado:', est, ', Frenar:', fren)

# Modo de transmision: Binario
osci.set_binario()


#%% ---------------------------- Funciones -------------------------------------------------------

def medir_all():
    
    '''
    Mide todos los canales activos y devuelve un Dataframe de Pandas con los parametros y datos de cada uno. 
    '''
    
    data = []
    
    estado_canales = osci.estado_ch()
    
    canales_activos = [int(canal+1) for canal in range(len(estado_canales)) if estado_canales[canal] =='1'] 
    
    osci.pausar()
    
    for ch in canales_activos:
        
        print('midiendo canal {}'.format(ch))
        
        medir = osci.definir_medir(int(ch))
        
        tiempo, voltaje = medir()
        
        time.sleep(.1)
        
        data.append(tiempo)
        
        data.append(voltaje)
    
    print('Todos los canales adquiridos correctamente')
    
    t1 = np.asarray(data[0])
    
    V1 = np.asarray(data[1])
    
    t2 = np.asarray(data[2])
    
    V2 = np.asarray(data[3])
    
    data_array = np.array([t1, V1, t2, V2])
    
    osci.adquirir()
    
    return data_array.T




#%% ---------------------------------Mediciones---------------------------------------

#medicion en multiples canales

#direccion de la carpeta donde se guardaran los datos
path = 'C:/Users/Matias/Documents/GitHub/Doctorado/Mediciones/20210408/'

nombre = 'CO_alta' # Nombre raíz del archivo donde se guardaran los datos.

cant_med = 20 # Cantidad de veces que quieren medir.

iniciar_desde = 1 # Desde donde comienza la numeración de los archivos.

espera = 1 # Tiempo de espera entre mediciones en segundos.        

for k in range(cant_med):
    
    print('Medicion ' + str(int(k+1)))
    
    num_str = int(k + iniciar_desde)
    
    data = medir_all()
    
    files = [file.replace('\\','/') for file in glob(path + nombre + 
                                        ' {}.txt'.format(num_str) + '*') ]
        
    
    
    if len(files)>0:
        
        filename = files[len(files)-1]
        
        np.savetxt(filename + ' (nuevo)', data, delimiter=',', header='t1, V1, t2, V2')
        
    else:
        
        filename = path + nombre +' {}.txt'.format(num_str)
        
        np.savetxt(filename, data, delimiter=',', header='t1, V1, t2, V2')
        
        data.to_csv(filename)
    
        
    time.sleep(espera)

print('Fin de las mediciones. Cerrando comunicacion con el osciloscopio...')

osci.cerrar()

print('Comunicacion con el osciloscpio terminada.')








