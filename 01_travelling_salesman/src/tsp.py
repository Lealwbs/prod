from mip import Model, xsum,  minimize, CBC, OptimizationStatus, BINARY
from itertools import product
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

# numero de clientes,no de identificacao da planta
# n = 34 # Instância 1
# n = 21 # Instância 2
n = 13 # Instância 3
planta = 0

# listas com os indices dos clientes e dos arcos
N = range(n)
A = [(i,j) for (i,j) in product(N,N) if i != j]

# posicao geografica dos nos

# Instância 1
# posx = np.array([37, 25, 27, 3, 17, 33, 32, 26, 20, 31, 23, 38, 14, 45, 9, 19, 36, 7, 46, 30, 18, 40, 43, 42, 5, 10, 4, 47, 22, 11, 16, 41, 24, 12])
# posy = np.array([36, 28, 21, 40, 41, 14, 36, 31, 29, 34, 17, 4, 44, 1, 6, 26, 37, 32, 22, 8, 24, 11, 23, 3, 7, 19, 43, 30, 5, 18, 15, 27, 25, 42])

# Instância 2
# posx = np.array([40, 25, 27, 3, 17, 33, 32, 26, 20, 31, 23, 38, 14, 45, 9, 19, 36, 7, 46, 30, 18])
# posy = np.array([5, 46, 39, 10, 20, 7, 5, 22, 31, 36, 45, 23, 28, 21, 14, 42, 29, 17, 4, 26, 30])

# Instância 3
posx = np.array([9, 25, 27, 3, 17, 33, 32, 26, 20, 31, 23, 38, 14])
posy = np.array([26, 33, 9, 19, 48, 7, 40, 17, 35, 39, 10, 20, 45])

# distancia Euclidiana entre os nos
c = [ [ sqrt( (posx[i] - posx[j])**2 + (posy[i] - posy[j])**2 ) for j in N ] for i in N]

# declaracao do modelo
model = Model('Problema do caixeiro viajante',solver_name=CBC) 

# x_ij igual a 1 se no j e visitado imediatamente apos no i; 0, caso contrario
x = {(i,j) : model.add_var(var_type=BINARY) for (i,j) in A}

# f_ij qtde de produto ficticio transportada pelo caixeiro viajante no arco (i,j) 
f = {(i,j) : model.add_var(lb=0.0) for (i,j) in A}

# funcao objetvio: minimizacao do comprimento/distancia da rota
model.objective = minimize(xsum(c[i][j] * x[i,j] for (i,j) in A)) 

# restricoes do grau de cada no: em t0do no, so chega um arco e so sai um arco dele
for i in N:
    model += xsum(x[ii,j] for (ii,j) in A if i == ii) == 1
for j in N:
    model += xsum(x[i,jj] for (i,jj) in A if j == jj) == 1

# restricoes para eliminacao de subciclos ou subrotas
# o caixeiro sai da planta com n-1 unidades de produto ficticio
# para deixar uma unidade em cada no a ser visitado
#restricoes de ativacao: um cliente i so pode ser atendido por j se j estiver instalado 
model += xsum(f[i,j] for (i,j) in A if i == planta) == n - 1

# restricao de balanco de fluxo: o caixeiro chega em um no com uma determinada
# quantidade de produto ficticio, deixa uma unidade deste produto, e sai
# deste no carregando uma unidade a menos.
for j in N:
    if j != planta:
        model += xsum(f[i,jj] for (i,jj) in A if j == jj) == 1 + xsum(f[jj,i] for (jj,i) in A if j == jj)

# restricao de ativacao do arco: o caixeiro so pode usar o arco (i,j) 
# para carregar produto ficticio se o arco for contabilizado na funcao objetivo
for (i,j) in A:
    model += f[i,j] <= (n-1) * x[i,j]
    
# otimiza o modelo chamando o resolvedor 
status = model.optimize()
if status == OptimizationStatus.OPTIMAL:
    print("Custo da rota: {:12.2f}".format(sum([c[i][j] * x[i,j].x for (i,j) in A])))
    cur_no = planta
    print("Rota: ") 
    while True:
          print("{:3d} ".format(cur_no+1),end='') 
          cur_no = [j for (i,j) in A if i == cur_no and x[i,j].x > 0.9][0]
          if cur_no == planta:
              break;
    print(), print()

    fig, ax = plt.subplots()
    plt.scatter(posx[:],posy[:],marker="o",color='black',s=10,label="nós")
    for i in N:
        plt.text(posx[i],posy[i], "{:d}".format(i + 1))

    for (i, j) in [(i, j) for (i, j) in A if x[i, j].x >= .9]:
        plt.plot((posx[i], posx[j]), (posy[i], posy[j]), linestyle="--", color="black")

    plt.scatter(posx[0],posy[0],marker="^",color='black',s=100,label="planta")
    plt.text(posx[0]+.5,posy[0], "{:s}".format("planta"))
    plt.legend()
    plt.plot()
    plt.savefig("exemplo_solucao.pdf")
    plt.show()