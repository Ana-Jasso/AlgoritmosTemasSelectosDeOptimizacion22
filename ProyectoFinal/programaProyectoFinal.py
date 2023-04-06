import pandas as pd
from operator import itemgetter

dn = pd.read_csv('Nodos.csv') #IMPORTACION DE LOS NODOS.
n = len(dn['N']) #GUARDAR EL NUMERO DE NODOS EN UNA VARIABLE.
print(f'Num de nodos: {n}\n') #IMPRIMIR NUMERO DE NODOS
df = pd.read_csv('Arcos.csv') #IMPORTACION DEL DATA FRAME.
print(df) #IMPRIMIR DATA FRAME
dN = pd.read_csv('Nombres.csv', encoding = "ISO-8859-1")
print(dN)

paises = [i for i in range(n)] #ARREGLO / LISTA DE PAÍSES
print(paises)
arcos = [ (i,j) for i in paises for j in paises if i!=j] #LISTA CON LOS ARCOS QUE GENERAN ESTOS PAÍSES
print(arcos)

#GUARDAMOS LOS NOMBRES DE CADA PAÍS
nombres_paises = dN['Nombres']
k=0
nombres = {}
for i in paises:
    nombres[i]=nombres_paises[k]
    k+=1
print(nombres)


a_distancia = df['Distancias'] #GUARDAMOS LAS DISTANCIAS DE CADA ARCO
k=0 #DECLARAMOS UNA VARIABLE PARA ITERAR LAS DISTANCIAS DE CADA ARCO
distancia = {} #DECLARAMOS UN DICCIONARIO PARA GUARDAR LAS DISTANCIAS ENTRE CADA ARCO
for i,j in arcos: #ITERAMOS EL DICCIONARIO
    distancia[i,j] = a_distancia[k] #ALMACENAMOS LAS DISTANCIAS EN EL DICCIONARIO
    k+=1 #VARIABLE PARA ITERAR EL LISTADO DE DISTANCIAS

print('\nListado de distancias entre cada nodo:\n')
print(distancia)

#PASO 1: ACOMODAMOS DE MENOR A MAYOR EL DICCIONARIO.
distancia_asc = sorted(distancia.items(), key=itemgetter(1))
print('\nLos valores acomodados de menor a mayor son:\n')
print(distancia_asc)

#PASO 2: CREAMOS UN DICCIONARIO CON LOS 5 ARCOS QUE CONTENGAN LAS MENORES DISTANCIAS ENTRE SÍ
candidatos=[]
print('\nLos 5 arcos con menor distancia entre ellos son:\n')
for i in range(0,10):
    candidatos.insert(i, distancia_asc[i])
candidatos = dict(candidatos)
print(candidatos)

#PASO 3: CREAR ARCOS ANTRE ESOS 5 ARCOS CANDIDATOS
#CREACIÓN DEL TOUR TSP
print('\nCreando arcos con las 5 distancias más cortas:')
TSP= [-1] #LISTA DONDE SE ESTARÁ AGREGANDO EL TOUR TSP
contador= 0
while(contador<5):
    for i, j in candidatos:
        if TSP[0] == -1:
            TSP[0] = i
            TSP.append(j)
            print(f'\nPodemos unir {i},{j} al TSP')
        elif TSP[0]==j and i not in TSP:
            print(f'Podemos unir {i},{j} al TSP')
            TSP.insert(0,i)
        elif TSP[-1] == i and j not in TSP:
            print(f'Podemos unir {i},{j} al TSP')
            TSP.insert(-1,j)
    contador+=1

print('\nResultado del Tour TSP hasta el momento:')
print(TSP)
#OBTENEMOS EL COSTO ACTUAL DE LA RUTA
i=0
l=1
costo=0
for i in range(0,len(TSP)-1):
    k= TSP[i]
    j= TSP[l]
    print(f'({k},{j}): {float(distancia[k,j])} + ')
    costo = costo + float(distancia[k,j])
    i+=1
    l+=1
print(f'El costo actual del tour: {costo}')

#PASO 4: UTILIZAMOS EL MÉTODO DE SOLUCIÓN DEL VECINO MÁS CERCANO PARA COMPLETAR EL TOUR TSP
print('\n\nInicializando el vecino más cercano:')
while len(TSP)<n:
    k=TSP[-1] #EL ULTIMO NODO DONDE ME ENCUENTRO ACTUALMENTE
    cercania={(k,j): distancia[(k,j)] for j in paises if k!= j and j not in TSP} #LA DISTANCIA DEL ULTIMO NODO EN EL QUE ESTOY CON TODOS LOS DEMAS QUE NO FORMAN PARTE DEL TOUR POR AHORA.
    new = min(cercania.items(), key=lambda x:x[1]) #SE DEVUELVE EL VALOR DEL NODO QUE QUEDA MÁS CERCA
    TSP.append(new[0][1]) #SE AGREGA EL NUEVO VALOR A LA LISTA
    print(f'\nEl país más cercano al nodo {k} es {new[0][1]}')
    print(TSP)
    costo = distancia[k,new[0][1]] + costo
    print(f'Costo: {costo}')
TSP.append(TSP[0]) #VOLVEMOS AL NODO INICIAL
costo = distancia[TSP[-2],TSP[0]]+costo #SUMAMOS COSTO
print('\n\nTour TSP completado:')
print(TSP)
print(f'El costo del tour: {costo}\n')

#PASO 5: INICIAMOS UN RECORRIDO DE BÚSQUEDA LOCAL CON EL MÉTODO SWAMP
print('\nSe inicia búsqueda local.')
hayMejoresSoluciones = True
while hayMejoresSoluciones == True:
    diferencia = {}
    costosnuevos = {}
    for i in range(1,n):
        TSPMejorado = TSP.copy()
        if i == n-1:
            j=1
            variableDeControl = TSP[i]
            print(f'\nLa primera posición es {TSPMejorado[i]} y la segunda {TSPMejorado[j]}')
            TSPMejorado[i] = TSP[j]
            TSPMejorado[j] = variableDeControl
        else:
            j=i+1
            variableDeControl = TSP[i]
            print(f'\nLa primera posición es {TSPMejorado[i]} y la segunda {TSPMejorado[j]}')
            TSPMejorado[i] = TSP[j]
            TSPMejorado[j] = variableDeControl
        print(f'El TSP cambiado resulta: {TSPMejorado}')
        p=0
        l=1
        nuevoCosto = 0
        for p in range(0,n):
            k= TSPMejorado[p]
            o= TSPMejorado[l]
            nuevoCosto = nuevoCosto + float(distancia[k,o])
            p+=1
            l+=1
        costosnuevos[TSPMejorado[j],TSPMejorado[i]] = nuevoCosto
        print(f'El costo es de: {costosnuevos[TSPMejorado[j],TSPMejorado[i]]}')
        diferencia[TSPMejorado[j],TSPMejorado[i]] = nuevoCosto - costo
        print(f'Diferencia con el tour TSP: {diferencia[TSPMejorado[j],TSPMejorado[i]]}')
    print('\nDiferencias:')
    print(diferencia)
    mejorDiferencia = min(diferencia.keys(), key=lambda m: diferencia[m])
    if diferencia[mejorDiferencia] > 0:
        hayMejoresSoluciones = False
        print('\nYa no hay una mejor solución')
    else:
        print(f'\nLa mejor diferencia es de {diferencia[mejorDiferencia]}')
        print(f'\n\nTSP anterior: {TSP}')
        print(f'Con un costo de {costo}')
        pA= TSP.index(mejorDiferencia[0])
        pB= TSP.index(mejorDiferencia[1])
        variableDeControl = TSP[pA]
        print(f'\nSe reemplazan {mejorDiferencia[0]} y {mejorDiferencia[1]}')
        TSP[pA] = TSP[pB]
        TSP[pB] = variableDeControl
        print(f'\nTSP actualizado: {TSP}')
        print(f'Con un costo de: {costosnuevos[mejorDiferencia[0],mejorDiferencia[1]]}\n')
        costo = costosnuevos[mejorDiferencia[0],mejorDiferencia[1]]

print('\n\nTour TSP final:')
print(TSP)
TSP_Nombres = []
for i in TSP:
    TSP_Nombres.append(nombres[i])
print(TSP_Nombres)
print(f'Con un costo de: {costo}\n')
