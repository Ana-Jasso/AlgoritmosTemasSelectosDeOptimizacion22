import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

df = pd.read_csv('101nodes.csv') #IMPORTACION DEL DATA FRAME.
n = len(df['NODO']) #GUARDAR EL NUMERO DE NODOS EN UNA VARIABLE.
print(f'Num de nodos: {n}\n') #IMPRIMIR NUMERO DE NODOS
print(df) #IMPRIMIR COORDENADAS

ciudades = [i for i in range(n)] #LISTA DE CIUDADES
arcos = [ (i,j) for i in ciudades for j in ciudades if i!=j] #LISTA CON LOS ARCOS QUE GENERAN ESTAS CIUDADES

#GUARDAR LOS DATOS DE COORDENADAS EN DOS ARRAYS
coordenadas_x = df['X']
coordenadas_y = df['Y']

distancia={ (i,j): np.hypot(coordenadas_x[i]-coordenadas_x[j], coordenadas_y[i]-coordenadas_y[j]) for i, j in arcos}
print('\nListado de distancias entre cada nodo:\n')
print(distancia)

#PARA DEFINIR EL NODO DE INICIO, SE USARÁ EL MÉTODO BURBUJA PARA ENCONTRAR LA MENOR DISTANCIA QUE EXISTE ENTRE UN NODO Y OTRO Y PARTIREMOS DESDE CUALQUIERA DE ESOS DOS NODOS.

menorDistancia = distancia[0,1]
for i, j in distancia:
    if (menorDistancia > distancia[i,j]):
        menorDistancia = distancia[i,j]
        nodoInicial = i
print(menorDistancia)
print(f'\nSe iniciará desde el nodo: {nodoInicial}\n') #IMPRIMIR NODO INICIAL

#CREACIÓN DE LA LISTA

TSP= [nodoInicial] #LISTA DONDE SE ESTARÁ AGREGANDO EL TOUR TSP
costo = 0
while len(TSP)<n:
    k=TSP[-1] #EL ULTIMO NODO DONDE ME ENCUENTRO ACTUALMENTE
    cercania={(k,j): distancia[(k,j)] for j in ciudades if k!= j and j not in TSP} #LA DISTANCIA DEL ULTIMO NODO EN EL QUE ESTOY CON TODOS LOS DEMAS QUE NO FORMAN PARTE DEL TOUR POR AHORA.
    new = min(cercania.items(), key=lambda x:x[1]) #SE DEVUELVE EL VALOR DEL NODO QUE QUEDA MÁS CERCA
    TSP.append(new[0][1]) #SE AGREGA EL NUEVO VALOR A LA LISTA
TSP.append(nodoInicial) #VOLVEMOS AL NODO INICIAL

print(f'El tour TSP es:\n{TSP}\n') #TSP SEGUN PYHTON

#OBTENER EL COSTO DE LA RUTA
print('Suma del costo total del tour TSP')
i=0
l=1
for i in range(0,n):
    k= TSP[i]
    j= TSP[l]
    print(f'({k},{j}): {float(distancia[k,j])} + ')
    costo = costo + float(distancia[k,j])
    i+=1
    l+=1

print(f'El costo del tour es de: {costo}')

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