# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:52:43 2020

@author: User
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
import magpylib as magpy
import statsmodels.api as sm
import os


#%%

'''
Para hacer el modelo de una bobina, vamos a aprovechar la clase "Collection"
que posee Magpylib para juntar varias fuentes de corriente en una sola por
superposición.

Podemos modelar una bobina de dos maneras, una más simplificada y otra más
precisa, pero más costosa computacionalmente (y puede llegar a tener más 
errores numéricos si no se hace bien).

NOTA: Recordar que las unidades en Magpylib son:

Corriente en Ampere [A]
Posición en milímetros [mm]
Campo en militeslas [mT]
'''

# Modelo simplificado:

coil1 = magpy.Collection() # Definimos el objeto para la Bobina 1

for z in np.linspace(-8, 8, 16):
    
    winding = magpy.current.Loop(current=100, diameter=10, position=(0,0,z) ) # Definimos el devanado de la bobinas
    
    coil1.add(winding)

coil1.show()

# Modelo más preciso:
    
ts = np.linspace(-8, 8, 1000)

vertices = np.c_[5*np.cos(ts*2*np.pi), 5*np.sin(ts*2*np.pi), ts] # Parametrizamos una espiral

coil2 = magpy.current.Line(current=100, vertices=vertices) # Creamos una fuente de corriente lineal con la forma de espiral

coil2.show()

#%%

'''
Usamos Matplotlib para graficar la líneas de campo de las bobinas que creamos
anteriormente.
'''

fig, [ax1,ax2] = plt.subplots(1, 2, figsize=(13,5))

# creamos la grilla donde graficaremos:
ts = np.linspace(-20, 20, 20)
grid = np.array([[(x,0,z) for x in ts] for z in ts])

# Obtenemos el campo y lo ploteamos:
B = magpy.getB(coil1, grid)
Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax1.streamplot(
    grid[:,:,0], grid[:,:,2], B[:,:,0], B[:,:,2],
    density=2,
    color=Bamp,
    linewidth=np.sqrt(Bamp)*3,
    cmap='coolwarm',
)

# Obtenemos el campo y lo ploteamos para la segunda bobina:
B = magpy.getB(coil2, grid)
Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

cp = ax2.contourf(
    grid[:,:,0], grid[:,:,2], Bamp,
    levels=100,
    cmap='coolwarm',
)
ax2.streamplot(
    grid[:,:,0], grid[:,:,2], B[:,:,0], B[:,:,2],
    density=2,
    color='black',
)

# Seteamos el estilo de las líneas, títulos y leyendas:
ax1.set(
    title='Campo magnético de la Bobina 1',
    xlabel='x-position [mm]',
    ylabel='z-position [mm]',
    aspect=1,
)
ax2.set(
    title='Campo magnético de la Bobina 2',
    xlabel='x-position [mm]',
    ylabel='z-position [mm]',
    aspect=1,
)

plt.colorbar(sp.lines, ax=ax1, label='[mT]')
plt.colorbar(cp, ax=ax2, label='[mT]')

plt.tight_layout()
plt.show()






#%%

get_ipython().run_line_magic('matplotlib', 'qt5')

pm=magpy.magnet.Cylinder(magnetization=[0,0,1000], dimension = [15,5]) # dimension (diameter,height) in mm.
# no pos, angle, axis specified so default values are used
print('magnatización',pm.magnetization) # Output: [0. 0. 1000.]
print('dimensiones',pm.dimension) # Output: [15. 5.]
print('posición',pm.position) # Output: [0. 0. 0.]
print(pm.orientation.as_euler('xyz')) # Output: [0. 0. 0.]
#print(pm.angle) # Output: 0.0
#print('eje',pm.xis) # Output: [0. 0. 1.]
#s.move([1,2,3])
#s.setOrientation(angle,axis)
#create sensor positions
xs1 = np.linspace(-150,150,200)
zs1 = np.linspace(-150,150,250)
Bs1 = np.array([[pm.getB([x,0,z]) for x in xs1] for z in zs1])


plt.ion()
plt.close("all")
#Dibujamos las líneas de campo alrededor del imán
plt.figure(1)
X,Y = np.meshgrid(xs1,zs1)
U,V = Bs1[:,:,0], Bs1[:,:,2]
amp = np.sqrt(U**2+V**2)
plt.contourf( X, Y, amp,np.linspace(0,130,50),cmap=plt.cm.brg) 
plt.streamplot(X, Y, U, V, color='w', density=3,linewidth=0.8)
plt.title = 'Campo magnético del imán',
plt.xlabel ('x-position [mm]'),
plt.ylabel ('z-position [mm]'),
plt.xlim=[-150,150]
plt.ylim=[-150,150],
plt.aspect = 1



#%%

#Calculo del campo en el eje z

zi = 30 # Posición inicial en mm

zf = 300 # Posición final en mm


zs = np.linspace(zi,zf,100)
Bs = np.array([pm.getB([0,0,z]) for z in zs] )


Bzs=Bs[:,2] # Nos quedamos con la componente en z ya que el resto es nulo.
   
#Graficamos la dependencia del campo con la posición a los largo del eje del imán
plt.figure(2)
plt.plot(zs,Bzs,'bs')
plt.xlabel("z(mm)")
plt.ylabel("Bz(T)")

#%%

'''
Proponemos una función para el ajuste Bz=a/z**k, estudiamos relación 
logBz vs logz para encontrar k analizar rango de validez del modelo variando 
el límite de zs.
'''

logzs=np.log10(zs)
logBzs=np.log10(Bzs)

Xs = sm.add_constant(logzs)
ols_model = sm.OLS(logBzs,Xs)
results = ols_model.fit()
o,m=results.params

ajuste=m*logzs+o
print('pendiente=', m)
print('ordenada al origen=', o)
print('R^2=',results.rsquared)
Bajuste=10**ajuste
#realizamos gráfico y ajuste en escala log-log 
plt.figure(3)
plt.plot(zs,Bajuste, 'r', label='Ajuste')
plt.scatter(zs,Bzs, label = 'Simulación')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('z(mm)')
plt.ylabel('Bz(T)')
plt.legend()

#%%

'''
Cargamos el archivo con mediciones y hacemos el mismo proceso de ajuste
pero ahora tenemos en cuenta que tienen error.
'''
carpeta = '' # Poner ruta de la carpeta con los datos

os.chdir(carpeta)

path = 'nombre_arch.txt' # Nombre del archivo con los datos

datos = np.loadtxt(path)


z = datos[:,0]

Bz = datos[:,1]

err_z = 5*np.ones(len(z)) # Poner error en mm

err_Bz = datos[:, 2]


logz=np.log10(zs)
logBz=np.log10(Bzs)

X = sm.add_constant(logz)

ajuste = sm.WLS(logBz, X, weights=1.0 / (err_Bz ** 2))
resultados = ajuste.fit()
print(resultados.summary())


#realizamos gráfico y ajuste en escala log-log 
plt.figure(4)
plt.plot(zs,Bajuste, 'r', label='Ajuste')
plt.errorbar(z,Bz, yerr=err_Bz, xerr=err_z, label = 'Datos')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('z(mm)')
plt.ylabel('Bz(T)')
plt.legend()



#intervalo de confianza para ordenada al origen y pendiente
oint,mint=resultados.conf_int(alpha=0.05)
deltam=abs((mint[1]-mint[0])/2)
deltao= abs((oint[1]-oint[0])/2)