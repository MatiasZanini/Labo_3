# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:30:35 2023

@author: Matias
"""
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

#%%

# Definimos una función que nos deje cargar los archivos del openchoice:

def datos_choice(path):
    
    df = pd.read_csv(path, index_col=False, names= list(range(17)))

    columna_canales = []

    for canal in [1,2]:
        
        columna_canal = [columna for columna in list(df.columns) if 
            'CH{}'.format(canal) in list(df[columna])]
        
        if len(columna_canal) < 1:
            
            raise ValueError('Canal no encontrado')
            
        columna_canales.append(columna_canal[0])
        
    t1, v1 = [np.asarray(df[columna_canales[0]+2]), 
                    np.asarray(df[columna_canales[0]+3])]

    t2, v2 = [np.asarray(df[columna_canales[1]+2]), 
                    np.asarray(df[columna_canales[1]+3])]
        
    return t1,v1,t2,v2
    
    
    
#%% Ahora vamos a cargar los datos:
    
path = 'C:/Users/Matias/Documents/GitHub/Labo_3/archivos/Copia de 0.5.csv'

t1, v1, t2, v2 = datos_choice(path)

# Ahora graficamos:
    
plt.plot(t1, v1, '.-', label='Canal 1')
plt.plot(t2, v2, '.-', label='Canal 2')
plt.legend()















