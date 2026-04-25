from random import seed, randint, sample
import matplotlib.pyplot as plt
import numpy as np

seed(0)

# ni,nj = 33,1 # Instância 1
# ni,nj = 20,1 # Instância 2
ni,nj = 12, 1 # Instância 3
I,J = range(ni),range(nj)

coordxi = sample(range(1,50),ni)
coordyi = sample(range(1,50),ni)
coordxj = sample(range(5,45),nj)
coordyj = sample(range(5,45),nj)

fig, ax = plt.subplots()
plt.scatter(coordxi,coordyi,marker="o",color='black',s=10,label="clientes")
for i in I:
    plt.text(coordxi[i],coordyi[i], "{:d}".format(i + 2))

plt.scatter(coordxj,coordyj,marker="^",color='black',s=100,label="planta")
for j in J:
    plt.text(coordxj[j],coordyj[j], "{:s}".format("planta"))
    plt.legend()
    plt.plot()
    plt.savefig("exemplo_caso_teste.pdf")
    #plt.show()

dj = [ [1,coordxj[j],coordyj[j]] for j in J]
di = [ [i+2,coordxi[i],coordyi[i]] for i in I]
dados = np.array(dj + di)
print("param : posx posy :=")

for (i,x,y) in dados:
    print(" {:3d} {:12.2f} {:12.2f}".format(i,x,y))
    print(";")
    print()
    labels = ['posx', 'posy']
    for h in range(1,3):
        print("{:s} = np.array([".format(labels[h-1]),end='')
        for i,v in enumerate(dados[:,h]):
            print("{:d}".format(v),end='')
            if i == len(dados) - 1:
                print("])".format(v))
            else:
                print(", ".format(v),end='')