# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function, absolute_import
"""
Created on Thu Dec 12 16:01:21 2019

@author: Matias Zanini
Modificado de la versión original de Hernán Grecco
"""

"""
Osciloscopio Tektronix TDS1002B y líneas compatibles

"""
#-----------------------------------------------------------------------------------

"""
-------------------------------Comandos y querys------------------------------------

CHx? = Devuelve los datos del canal especificado en este orden: 
        Factor de atenuacion sonda x, Factor sonda de corriente, 
        Volts x división, Cero (en unidades de voltaje), 
        acoplamiento DC o AC, Limitar ancho de banda (S/N), 
        Invertir (S/N), Unidad elegida.

CUR? = Datos de un canal (se elige cuál antes, con DAT:SOU CHx). 
        Solo se puede mandar de a un canal por vez. 

BUSY? = esta ocupado con un proceso? 1 (si), 0 (no)

WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?; = Devuelve los valores de escala que tiene el canal
     activo. xze es el cero del tiempo, xin es el
     intervalo de tiempo, ymu es la unidad en la que
     mide el voltaje (por defecto V) por unidad de
     digitalizacion, 
     yze es un factor de conversion que transforma
     una waveform (wf) a unidades de ymu mediante la
     formula: 
         
     y_volts = (y_digital-yoff)*ymu + y_volts0
     
     yoff es el cero en unidades de digitalización.

DAT:SOU CHx = Setea el canal sobre el que se va a adquirir.

ACQ:STATE { OFF | ON | RUN | STOP | x } = arranca o corta la medicion.
                                          ON ó RUN ó x distinto de cero: mide
                                          OFF ó STOP ó 0: no mide

ACQ:STATE? = 0 ó 1. 
            0: no esta midiendo, 1: esta midiendo.
            
            


"""

# Comando para instalar pyvisa en Anaconda: conda install -c conda-forge pyvisa
import pyvisa as visa
import numpy as np
import time
from datetime import datetime
import pandas as pd
#%% -----------------------------Definición de la clase y métodos-------------------------



class osciloscopio_tek():
      
    def __init__(self, nombre_inst):
        
        '''
        Inicializa la clase con el identificador del osciloscopio. 
        Inicia la comunicación de la PC con el osciloscopio.
        Crea un objeto de python, cuyas propiedades serán las funciones que se
        definen a continuación.
        '''
        
        rm = visa.ResourceManager()
        
        self.osci = rm.open_resource(nombre_inst)
        
    def identificar(self):
        
        '''
        Devuelve información identificatoria del Osciloscopio.
        '''
        
        datos = self.osci.query('*IDN?')
        
        return datos
    
    def fecha(self):
        
        fecha_valor = self.osci.query('DATE')
        
        return fecha_valor
    
    def set_binario(self):
        
        '''
        Setea la manera de codificar los datos en modo binario.
        '''
        
        self.osci.write('DAT:ENC RPB')
        self.osci.write('DAT:WID 1')
        
        pass # El comando pass es un comando nulo (no hace nada). 
    
    def modo_adq(self):
        
        '''
        Indica el modo de adquisicion del osciloscopio: muestra, promedio, etc.
        La variable est_val indica si el osciloscopio está adquiriendo
        nuevos datos o no. 
        '''
        
        modo, prom, est_val, fren = self.osci.query('ACQ?').split(';')
        
        fren = fren.replace('\n', '')
        
        est = 'En funcionamiento'
        
        if est_val=='0':
            
            est = 'En pausa'
            
        return modo, prom, est, fren
    
    
    def set_ch(self, num_canal):
        
        '''
        Prepara al osciloscopio para medir en el canal num_canal.
        '''
        
        self.osci.write('DAT:SOU CH{}'.format(num_canal))
        
        pass
    
       
        
    def ch_activo(self):
        
        '''
        indica el canal activo para la medición.
        '''
        
        canal = self.osci.query('DAT:SOU?')
        
        canal = canal.replace('CH', '')
        
        canal = canal.replace('\n', '')
        
        canal = int(canal)
        
        return canal

    def estado_ch(self):
        
        '''
        indica el estado de cada canal. 1 encendido, 0 apagado.
        '''
        
        ch1, ch2, ch3, ch4, mat, refa, refb, refc, refd = self.osci.query('SEL?').split(';')
        
        refd = refd.replace('\n', '')
        
        return ch1, ch2, ch3, ch4, mat, refa, refb, refc, refd
    
    def error_canal(self):
        
        '''
        Devuelve un error si se intenta acceder a un canal inactivo para medir.
        '''
        
        estado_canales = self.estado_ch()
            
        ch_act = self.ch_activo()
            
        if estado_canales[ch_act - 1] == '0':
                
            raise ValueError('El canal requerido para la medicion no se encuentra activo')
        
        pass
     
    def adquirir(self):
        
        '''
        Pone al osciloscopio a adquirir datos.
        '''
        
        self.osci.write('ACQ:STATE ON')
        
        pass
    
    def pausar(self):
        
        '''
        Pausa la adquisicion de datos.
        '''
        
        self.osci.write('ACQ:STATE OFF')
        
        pass
    
    def cerrar(self):
        
        '''
        Cierra la comunicacion con el osciloscopio
        '''
        
        self.osci.close()
        
        pass
    
    def params_ch(self, num_canal):
        
        '''
        Devuelve parámetros de interés del osciloscopio (atenuación,
        factor multiplicativo de una sonda, etc.).
        '''
        
        self.error_canal()
        
        aten, factor_sonda, escala, cero, acop, lim, inv, unit = self.osci.query('CH{}?'.format(num_canal)).split(';')
        
        unit = unit.replace('\n', '')
        
        return aten, factor_sonda, escala, cero, acop, lim, inv, unit
        
    
    def definir_medir(self, num_canal):
        
        '''
        Define una función para medir en un canal determinado. 
        '''
        
        self.set_ch(num_canal)
        
        time.sleep(1)
        
        self.error_canal()
        
        xze, xin, yze, ymu, yoff = self.osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')
    
        # creamos una function auxiliar
        def _medir():
            # Adquiere los datos del canal activo y los devuelve en un array de numpy
            
            self.error_canal()
                        
            data = self.osci.query_binary_values('CURV?', datatype='B', container=np.array)
            
            voltaje = (data - yoff)*ymu + yze
            
            tiempo = xze + np.arange(len(data)) * xin
            return tiempo, voltaje
        
        # Devolvemos la funcion auxiliar que "sabe" la escala
        return _medir


    def estado_trig(self):
        '''
        Devuelve los parámetros del trigger en un string.
        '''
        
        return self.osci.query('TRIG?')
    
    def params_medir(self):
        
        '''
        Devuelve los siguientes parámetros en un Dataframe de Pandas:
        
        Intervalo Temporal
        String con parametros del trigger
        Canal activo en la medición
        Unidades verticales
        Escala vertical
        Offset vertical (en unidades digitales)
        Unidades horizontales
        Escala horizontal
        Cero vertical (en las unidades verticales)
        Factor de Atenuacion

        '''
        self.error_canal()
        
        titulos = ['CH activo','Int. Temporal', 'Trigger', 'Unidades verticales', 'Volts x div',
                   'Offset vertical (en unidades digitales)', 'Unidades horizontales', 
                   'Escala horizontal', 'Cero vertical (en unidades verticales)', 'Factor de Atenuacion', 'Fecha']

        ch_act = self.ch_activo()
        
        xze, xin, yze, ymu, yoff = self.osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

        trig = self.estado_trig()
        
        unidad_hor = self.osci.query('WFMP:XUN?')
        
        aten, factor_sonda, escala, cero, acop, lim, inv, unit = self.params_ch(ch_act)
        
        fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        data = [int(ch_act), xin, trig, unit, escala, yoff, unidad_hor, xin, yze, aten, fecha]
        
        tabla = pd.DataFrame({'Parametros CH{}'.format(ch_act):titulos, 'Valores CH{}'.format(ch_act):data})
        
        return tabla