# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:35:42 2021

@author: Mati
"""

ready = True

if ready:
    
    print('Hola Mundo!')
    
    
#%% ------------------------------- Definimos variables -----------------------------


a = 'hola' # Esta variable guarda un string (cadena de caracteres)

b = 2 # Esta variable guarda un entenero

c = 10.58 # Esta variable guarda un número de punto flotante

d = False # Esta variable guarda un booleano

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
    
    j = j + 1 # La variable se actualizará en cada iteración.
    
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


























