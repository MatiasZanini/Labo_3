# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 20:15:29 2025

@author: Mati
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Datos del cuarteto de Anscombe
data = {
    'I': {
        'x': np.array([10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]),
        'y': np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])
    },
    'II': {
        'x': np.array([10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]),
        'y': np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])
    },
    'III': {
        'x': np.array([10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]),
        'y': np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73])
    },
    'IV': {
        'x': np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0, 8.0, 8.0, 8.0]),
        'y': np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])
    }
}

# Crear figura principal y el grid externo 2x2
fig = plt.figure(figsize=(12, 10))
outer_grid = gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.3)

# Para cada conjunto del cuarteto de Anscombe
for i, key in enumerate(sorted(data.keys())):
    d = data[key]
    x = d['x']
    y = d['y']
    
    # Ajuste lineal: y = m*x + b
    m, b = np.polyfit(x, y, 1)
    y_fit = m * x + b
    resid = y - y_fit  # residuos
    
    # Crear un grid interno para cada celda: 2 filas (superior: gráfico, inferior: residuos)
    inner_grid = gridspec.GridSpecFromSubplotSpec(
        2, 1, subplot_spec=outer_grid[i], height_ratios=[3, 1], hspace=0.1)
    
    # Axes para el gráfico principal (scatter + línea de ajuste)
    ax_main = fig.add_subplot(inner_grid[0])
    ax_main.scatter(x, y, label='Datos')
    ax_main.plot(x, y_fit, color='orange', label='Ajuste lineal')
    ax_main.set_title(f'Anscombe {key}', fontsize=16)
    ax_main.legend(fontsize=8)
    # Remover etiquetas x en este subplot (se compartirán en el de residuos)
    ax_main.set_xticklabels([])
    
    # Axes para el gráfico de residuos
    ax_resid = fig.add_subplot(inner_grid[1], sharex=ax_main)
    ax_resid.scatter(x, resid, color='#d62728', s=20)
    ax_resid.axhline(0, color='gray', linestyle='--')
    ax_resid.set_ylabel('Residuos', fontsize=14)
    ax_resid.set_xlabel('x',fontsize=14)
    
    # Opcional: ajustar límites o estilos
    ax_resid.tick_params(axis='both', which='major', labelsize=12)
    ax_main.tick_params(axis='both', which='major', labelsize=12)

# plt.suptitle('Cuarteto de Anscombe: Datos, Ajuste Lineal y Residuos', fontsize=16)
plt.show()
