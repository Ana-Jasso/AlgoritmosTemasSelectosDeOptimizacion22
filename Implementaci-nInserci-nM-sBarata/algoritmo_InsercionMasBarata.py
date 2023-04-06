import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

df = pd.read_csv('101nodes.csv') #IMPORTACION DEL DATA FRAME (PUEDE SER EL DE 5, 48 O MÁS NODOS).
n = len(df['NODO']) #GUARDAR EL NUMERO DE NODOS EN UNA VARIABLE.
print(f'Num de nodos: {n}\n') #IMPRIMIR NUMERO DE NODOS
print(df) #IMPRIMIR COORDENADAS

nodos = [i for i in range(n)] #LISTA DE NODOS
arcos = [ (i,j) for i in nodos for j in nodos if i!=j] #LISTA CON LOS ARCOS QUE GENERAN ESTOS NODOS ENTRE SÍ

#GUARDAR LOS DATOS DE COORDENADAS EN DOS ARRAYS
coordenadas_x = df['X']
coordenadas_y = df['Y']

distancia={ (i,j): np.hypot(coordenadas_x[i]-coordenadas_x[j], coordenadas_y[i]-coordenadas_y[j]) for i, j in arcos}
print('\nListado de distancias entre cada nodo:\n')
print(distancia)

#PASO 1: PARA DEFINIR EL NODO DE INICIO, BUSCAMOS LA MENOR DISTANCIA QUE EXISTE ENTRE UN NODO Y OTRO Y PARTIREMOS DESDE ESOS DOS NODOS.

menorDistancia = min(distancia.keys(), key=lambda m: distancia[m])
nodoInicial = menorDistancia[0]
nodoSiguiente = menorDistancia[1]

print(f'\nSe iniciará desde el nodo: {nodoInicial}\n i={nodoInicial}') #IMPRIMIR NODO INICIAL

#PASO 2: FORMAR UN SUBTOUR CON EL NODO MÁS CERCANO AL NODO DE INICIO
print(f'\nEl nodo más cercano al nodo i es: {nodoSiguiente}\n T={nodoInicial}-{nodoSiguiente}-{nodoInicial}')
#CREACIÓN DE LA LISTA
TSP= [nodoInicial, nodoSiguiente, nodoInicial] #LISTA DONDE SE ESTARÁ AGREGANDO EL TOUR TSP
costo = distancia[nodoInicial,nodoSiguiente] * 2
print(TSP)
print(f'Costo inicial: {costo}')

#PASO 3: ENCONTRAR UN ARCO [i,j] Y UN NODO K QUE NO SE ENCUENTRE EN EL SUBTOUR
while len(TSP)<=n: #REPRESENTACIÓN DEL PASO 5
    diccionario_deltaf = {}
    print('¿TSP?\nNO\n')
    vueltas = len(TSP) -1

    #CALCULAR DELTA F Y FORMAR UN DICCIONARIO
    for i in range(vueltas):
        j= i+2
        variable = TSP[i:j]
        print(f'\nInterceptando dentro de: {variable}')
        k=0
        for k in nodos:
            if k not in TSP:
                print(f'Nodo no en T: {k}')
                diccionario_deltaf[variable[0],variable[1],k] = distancia[variable[0], k] + distancia[k, variable[1]] - distancia[variable[0], variable[1]]
                print(f'Delta F es la distancia de {variable[0]},{k} más la listancia de {k},{variable[1]} menos la distancia de {variable[0]},{variable[1]} que es igual a {diccionario_deltaf[variable[0],variable[1],k]}')
    #ENCONTRAR EL COSTO (DELTA F) MAS BARATO
    print(f'\n\n{diccionario_deltaf}')
    masBarato = min(diccionario_deltaf.keys(), key=lambda p: diccionario_deltaf[p])
    costo = diccionario_deltaf[masBarato] + costo
    print(f'\n\nSe interceptará el nodo {masBarato[2]} entre {masBarato[0]} y {masBarato[1]} sumando un costo de {costo}')
    #PASO 4: INSERTARLO EN EL TOUR TSP
    rango = int(len(TSP))
    for w in range(0, rango):
        if masBarato[0] == TSP[w] and masBarato[1] == TSP[w+1]:
            TSP.insert(w+1, masBarato[2])
    print(TSP)
print(f'TSP completado.')

#DEMOSTRACIÓN GRÁFICA DE LA RUTA
x= coordenadas_x
y= coordenadas_y

plt. figure(figsize=(12,6))
plt.scatter(x,y,color='black')

for n in range(len(TSP)-1):
    plt.plot([coordenadas_x[TSP[n]],coordenadas_x[TSP[n+1]]],
             [coordenadas_y[TSP[n]],coordenadas_y[TSP[n+1]]], color = 'red')

plt.xlabel('coordenadas_x')
plt.ylabel('coordenadas_y')
plt.title('TSP')
plt.show()