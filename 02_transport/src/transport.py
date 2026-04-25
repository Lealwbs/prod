from mip import Model, minimize, xsum

# Dados do problema
custos = [
    [10, 2, 20, 11],  # CD 1
    [12, 7, 9, 20],   # CD 2
    [4, 14, 16, 18]   # CD 3
]
oferta = [15, 25, 10]
demanda = [5, 15, 15, 15]

# Armazena o tamanho original que sera utilizado na impressao
num_cds_reais = len(oferta)
num_mercados_reais = len(demanda)

total_oferta = sum(oferta)
total_demanda = sum(demanda)

if total_demanda > total_oferta:
    deficit = total_demanda - total_oferta
    oferta.append(deficit) # Adiciona a oferta fictícia
    custos.append([0] * len(demanda)) # Adiciona uma linha de custos 0
    print(f"Demanda > Oferta.")
    print(f"CD Fictício criado para absorver a falta de {deficit} unidades.\n")
    
elif total_oferta > total_demanda:
    excesso = total_oferta - total_demanda
    demanda.append(excesso) # Adiciona a demanda fictícia
    for linha in custos:
        linha.append(0) # Adiciona uma coluna de custo 0 em cada CD
    print(f"Oferta > Demanda.")
    print(f"Mercado Fictício criado para reter o excesso de {excesso} unidades.\n")
    
else:
    print("Problema perfeitamente balanceado. Nenhum ajuste necessário.\n")

m = range(len(oferta))
n = range(len(demanda))

model = Model("Problema_de_Transporte")

# Variáveis
x = [[model.add_var(name=f"x_{i}_{j}", lb=0) for j in n] for i in m]

# Função Objetivo
model.objective = minimize(xsum(custos[i][j] * x[i][j] for i in m for j in n))

# Restrições de Oferta
for i in m:
    model += xsum(x[i][j] for j in n) <= oferta[i]

# Restrições de Demanda
for j in n:
    model += xsum(x[i][j] for i in m) >= demanda[j]

status = model.optimize()

if model.num_solutions:
    print(f"Custo Total Mínimo: {model.objective_value}")
    for i in m:
        for j in n:
            if x[i][j].x > 0:
                quantidade = x[i][j].x
                
                # Identifica se a origem é real ou fictícia
                nome_origem = f"CD {i+1}" if i < num_cds_reais else "CD Fictício (Falta de Produto)"
                
                # Identifica se o destino é real ou fictício
                nome_destino = f"Mercado {j+1}" if j < num_mercados_reais else "Mercado Fictício (Estoque Retido)"
                
                print(f"Enviar {quantidade:5.1f} unidades do {nome_origem} para o {nome_destino}")
else:
    print("Nenhuma solução encontrada.")