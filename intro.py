# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:35:42 2021

@author: Mati
"""

ready = True

if ready:
    
    print('Hola Mundo!')
    
    
#%% ------------------------------- Definimos variables -----------------------------

'''
NOTA: Las celdas en Spyder se definen con: #%%
Al escribir esto, se genera una división del script que permite ejecutar fácilmente una partecita del mismo
sin necesidad de ejecutar el script completo.
'''


a = 'hola' # Esta variable guarda un string (cadena de caracteres)

b = 2 # Esta variable guarda un entenero

c = 10.58 # Esta variable guarda un número de punto flotante

d = False # Esta variable guarda un booleano (tipo de variable lógica que puede tener solo dos valores: True o False)

#%%

'''
Podemos hacer cosas con las variables luego de definirlas
'''

print(b+c) # Suma los números y los devuelve en la consola.

print(a) # Muestra el valor de a en la consola. En este caso, un string.

'''
También podemos asignar los resultados de las operaciones en una nueva 
variable:
'''

e = b+c # Ahora, definimos una nueva variable que tendrá guardado el valor 12.58 en punto flotante.


#%% Listas:
    
'''
Las listas son un arreglo indexado de objetos de python. Pueden guardar casi cualquier cosa.
El índice de las listas comienza desde el cero.
'''
    
lista = [a, b, c, d, e]

# Podemos llamar a un elemento de la lista con []:
    
print(lista[0]) # Esto mostrará en la consola el primer elemento de la lista, "a". Por lo tanto, en la consola aparecerá "hola".

#%%

# Podemos "sumar" listas. Para Python, esto es CONCATENARLAS.

otra_lista = [1,2,3] # Lista de números enteros.

lista_suma = lista + otra_lista # Concatenamos las dos listas.

print(lista_suma)


#%%  -------------------------------- IF, FOR y WHILE --------------------------------


if 2+2 == 4:
    
    print('Este bloque de código se ejecutará.')
    
    
    
if 2+2 == 1:
    
    print('Este bloque de código no se ejecutará.')
    

if False:
    
    print('Este bloque no se ejecutará.')
    
    
#%%

if 2+2==3:
    
    print('primer condición')
    
else:
        
    print('Como no se cumplió la primer condición, se ejecuta este bloque.')
    
#%%

if 2+2==1:
    
    print('primer condicion')
    
elif 2+2==3:
        
    print('segunda condicion')

elif 2+2==4:
    
    print('tercera condicion. Esta si se ejecutará.')


#%%


for elemento in lista:
    
    print(elemento) # En cada iteración, la variable "elemento" cambiará y se convertira en cada elemento de la lista.
    
    
 #%%   
'''
También podemos definir la variable de la iteración durante la declaración del for:
'''

for i in range(5):
    
    print(i) # Aquí la variable "i" irá desde 0 hasta 4, de forma que se iterará 5 veces.


#%%

j = 0


while j<10:
    
    j = j + 1 # La variable se actualizará en cada iteración. El comando: j += 1 es una abreviatura para j = j + 1 que pueden usar
    
    print('El valor de j es:', j) # Este código se ejecutará hasta que j sea mayor o igual a 10


#%%

while True:
    
    print('Este código se ejecutará por siempre, hasta que alguien detenga el programa de manera externa.')


#%%


'''
Podemos combinar estos comandos de diferentes maneras. 
Siempre recordando que una nueva orden implica un nuevo bloque.
'''

if 2+2==4:
    
    print('Este es el primer bloque de identación. Lo armamos presionando "Tab" ')

    for elemento in ['Agua','Aire','Fuego','Tierra']:
        
        # Este es el segundo bloque de identación.
        
        print(elemento) # Se mostrará en la consola cada elemento de la lista en cada iteración.
        
    print('Volvimos al primer bloque. Se ejecutará cuando termine el segundo bloque.')





#%% ------------------------ FUNCIONES ------------------------------------------------

'''
Las funciones son objetos de Python que permiten guardar bajo un nombre un conjunto de instrucciones. 
Esas instrucciones pueden depender de variables que el usuario puede ingresar al llamar a la función
con el objetivo de ejecutar sus instrucciones.

'''


# Ejemplo 1. Función numérica:
    
def suma(x,y):
    
    return x+y

# Ejemplo 2. Función sin variables:
    
def cartelito():
    
    '''
    NOTA: en este caso no hizo falta utilizar el comando "return", ya que el bloque de código 
    interno de la función, siempre se ejecuta. Así, el cartel se muestra en la consola. El 
    comando "return" sirve para explicitar lo que se quiere que la función devuelva al ejecutarse
    y pueda ser guardado en una variable.
    '''
    
    string = 'Este cartel se mostrará al llamar a la función "cartelito"' # Variable interna. Solo se define dentro de la funcion.
    
    
    print(string)


# Ejemplo 3. Función con un if:
    
def menor_a_10(numero):
    
    if numero < 10:
        
        return True
    
    else:
        
        return False



#%% --------------------------- IMPORTAR LIBRERÍAS -----------------------------------------------

'''
NOTA: esto se hace siempre al inicio del script. En este en particular, lo hacemos recién ahora porque estamos aprendiendo
a utilizar las funciones de python.
'''

import numpy as np # Nos permite trabajar con objetos que funcionan como matrices y vectores

import scipy as sp # Provee una gran variedad de funciones matemáticas, herramientas de ajuste, etc.

from scipy.constants import constants as ctes # Provee una gran variedad de constantes físicas y matemáticas

import pandas as pd # Permite crear tablas de datos y guardarlas fácilmente en la computadora.

from matplotlib import pyplot as plt # Permite graficar los resultados obtenidos. Vermos como usarla bien más adelante.


#%%

'''
Los arreglos de numpy funcionan como vectores en el sentido de que solo admiten números como sus elementos y permiten que se
realicen ciertas operaciones entre ellos. Entre estas se encuentra, la suma, resta, multiplicación por escalar, producto interno,
producto matricial, entre otros.
'''

v1 = np.array([1,2,3,4,5,6])

v2 = np.array([2,2,2,2,2,2])


# Prueben los siguientes resultados en la consola:
    
v1+v2

v1*v2

np.dot(v1,v2)



#%%

m1 = np.array([[1,1], [1,2]])

m2 = np.array([[2,2], [3,3]])


# Prueben los siguientes resultados en la consola:

m1+m2

m1*m2

np.dot(m1,m2)


#%% Guardado de datos


# Esto guardará los archivos en el directorio de trabajo que tengan seleccionado.

np.savetxt('vector1.txt', v1)

np.savetxt('matriz1.txt', m1)

# Si quieren especificar otro directorio deben explicitarlo con un string:
    
path = 'C:/Users/Mati/Documents/GitHub/Labo_3/' # Recuerden utilizar la barra normal "/" y no la invertida "\"

filename = 'vector2.txt'

np.savetxt(path+filename, v2)


#%% Carga de datos


v1_cargado = np.loadtxt('vector1.txt') # Hay que definir una variable donde se guardarán los datos cargados.

# Nuevamente, puede cargarse el archivo desde un directorio específico:

path = 'C:/Users/Mati/Documents/GitHub/Labo_3/' # Recuerden utilizar la barra normal "/" y no la invertida "\"

filename = 'vector2.txt'    

v2_cargado = np.loadtxt(path+filename)



#%% 
'''
Numpy tiene funciones útiles.
Scipy tiene muchas constantes físicas y matemáticas.
Las herramientas de ajuste de datos de scipy las veremos otra clase.
'''

q_electron = ctes.e # Carga del electrón en Coulombs

np.sin(ctes.pi) # Numpy tiene cargadas las funciones trigonométricas.

'''
NOTA: El seno de pi puede no dar exactamente 0. Esto es por la aproximación de punto flotante que hace la máquina
uno no puede poner el valor de pi (infinitos decimales) con precisión perfecta, debido a la limitación de memoria.
'''

np.exp(1) # La funcion exponencial. Evaluada en 1, debería dar el número e



#%% 

# Funciones útiles

'''
Para ver que hace cada función, tocar click sobre la misma (dejando el cursor para escribir sobre ella) y presionar
"ctrl + i"
'''

equiespaciado = np.linspace(1,10,10) # Vector del 1 al 10 con 10 elementos.

ordenado = np.arange(0, 40, 10) # Vector del 0 al 40 (no incluído) con pasos de 10 en 10.

a = [1,2,3]

vector_from_list = np.asarray(a) # Convierte una lista u objeto similar en un array de numpy.

len(equiespaciado) # Devuelve el tamaño del arreglo.

sum(equiespaciado) # Devuelve la suma de los elementos del arreglo.

np.mean(equiespaciado) # Devuelve el promedio del vector.


#%%

'''
La librería pandas es muy útil para generar tablas de datos. Las tablas se llaman DataFrame y
poseen un nombre para cada columna, mientras que las filas quedan asociadas a un índice.
'''

tiempo = [1,2,3,4,5,6,7,8]

señal = [4,5.4,5.3, 3, 4.3, 2.2, 2.4, 8]

N = len(tiempo)

tabla = pd.DataFrame(index = range(N), columns= ['Tiempo', 'Voltaje']) # Definimos N filas y 2 columnas. 

tabla['Tiempo'] = tiempo # Agregamos los datos del tiempo a la columna 'Tiempo'

tabla['Voltaje'] = señal # Agregamos los datos de la señal a la columna 'Voltaje'


print(tabla)



#%% 

# Otra forma es creando un diccionario:
    
diccionario = {'Tiempo': tiempo, 'Voltaje': señal}

tabla2 = pd.DataFrame(diccionario)

print(tabla2)


#%%

# Guardar la tabla como CSV:

path = 'C:/Users/Mati/Documents/GitHub/Labo_3/' # Recuerden utilizar la barra normal "/" y no la invertida "\"

filename = 'Datos.csv'

    
tabla.to_csv(path+filename, index=False) # El ignore_index=True le pide que no guarde los numeros de los indices en la tabla

#%%

# Cargar el CSV como tabla:
    
tabla_cargada = pd.read_csv(path+filename)


tiempo_array = np.asarray(tabla_cargada['Tiempo']) # Con esto nos armamos un array de numpy con los datos de la tabla























