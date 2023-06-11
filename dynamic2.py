import random
import time
#stała ładowność, zmienna liczba kontenerów

def generate_containers(num, weights, values, b):
    for i in range(0,num):
        r1 = random.randint(1,b) 
        r2 =  random.randint(1,b)
        weights.append(r1)
        values.append(r2)
        #print("r1:",r1,"r2:",r2)
    return weights, values


def optimal_load_dynamic_1(b, weights, values):
    n = len(weights)
    D = [[0] * (b + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, b + 1):
            if weights[i - 1] > j:
                D[i][j] = D[i - 1][j]
            else:
                D[i][j] = max(D[i - 1][j], D[i - 1][j - weights[i - 1]] + values[i - 1])

    max_value = D[n][b]
    loaded_containers = []
    j = b
    for i in range(n, 0, -1):
        if D[i][j] != D[i - 1][j]:
            loaded_containers.append(i - 1)
            j -= weights[i - 1]

    return max_value, loaded_containers

def greedy_load_fixed_capacity(b, weights, values):
    n = len(weights)
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True, key=lambda x: x[0])

    loaded_containers = []
    total_weight = 0
    total_value = 0

    for ratio, container_idx in ratios:
        if total_weight + weights[container_idx] <= b:
            loaded_containers.append(container_idx)
            total_weight += weights[container_idx]
            total_value += values[container_idx]

    return total_value, loaded_containers



b = 500

time_greedy = []
time_dyn = []
quantity = []
quality = []

weights = []
values = []
max_containers = 1000
step = 50
start = 100

weights, values = generate_containers(200, weights, values, 1000)

for quant in range(b, max_containers, step):
    weights, values = [], []
    
    start_time = time.time()
    max_value_dyn, loaded_containers = optimal_load_dynamic_1(b, weights.copy(), values.copy())
    stop_time = time.time() - start_time
    time_dyn.append(stop_time)
    
    
    #print("Maksymalna pojemność ładunku:", b)
    
    print("used:",len(loaded_containers) ,"per dynamic for quant: ", quant)
    print("Maksymalna wartość ładunku:", max_value_dyn)
    print("Załadowane kontenery:", loaded_containers)
    max_value_gr = 0
    loaded_containers.clear()
    print("--------------")
    
    start_time = time.time()
    print(start_time)
    max_value_gr, loaded_containers = greedy_load_fixed_capacity(b, weights.copy(), values.copy())
    stop_time = time.time() - start_time
    print(time.time())
    time_greedy.append(stop_time)


    #print("Maksymalna pojemność ładunku:", b)
    print("used:",len(loaded_containers) ,"per greedy for quant: ", quant)
    print("Maksymalna wartość ładunku:", max_value_gr)
    print("Załadowane kontenery:", loaded_containers)

    error= (max_value_dyn-max_value_gr)/max_value_dyn
    print("error:", error)
    quality.append(error)
    print("\n--------------\n")
    quantity.append(quant)
#Stała ładowność statku, zmienna liczba kontenerów:


#print("dyn: ", time_dyn, "greedy: ", time_greedy, "error: ", quality)
f = open(r"D:\polibuda\2sem\aisd\zad5\data2.txt", "w+")
f.write("ilosc:\ttime_dynamic\ttime_greedy\tquality\n")
for i in range(0, len(time_dyn)):
    print(quantity[i], time_dyn[i], time_greedy[i], quality[i])
    f.write(str(quantity[i])+"\t"+str(time_dyn[i])+"\t"+ str(time_greedy[i])+ "\t"+ str(quality[i]) + "\n")
f.close()
    
