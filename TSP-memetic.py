#solving TSP using memetic algorithm

import random, sys


#generates a random number between 1 and the number of cities minus 1.
def Rand_City(size):
    return random.randint(1, size-1)


#checks if a city was seen before of not.
def Is_New(Gene, city):
    for c in Gene:
        if c == city:
            return False
    
    return True


#find the fitness using the given matrix
def Find_Fitness(Gene, cities):
    fitness = 0
    for i in range(0, len(Gene)-1):
        if cities[Gene[i]][Gene[i+1]] == 0:
            return sys.maxint
        else:
            fitness += cities[Gene[i]][Gene[i+1]]

    return fitness


#generates a Gene randomly or generates a path randomly
def Create_Gene(size):
    Gene = [0]
    for i in range(size-1):
        while True:
            new_city = Rand_City(size)
            if Is_New(Gene, new_city):
                Gene += [new_city]
                break
    
    Gene += [0]

    return Gene


def Give_2_rand_number(size):
    while True:
        change1 = Rand_City(size)
        change2 = Rand_City(size)
        if change1 != change2:
            break
    if change1 > change2:
        temp = change1
        change1 = change2
        change2 = temp
    
    return change1, change2


#gets 2 cities and swap them to make a mutation.
def Mutation(Gene):
    change1, change2 = Give_2_rand_number(len(Gene)-1)
    for i in range((change2 - change1 + 1)/2):
        temp = Gene[change1+i]
        Gene[change1+i] = Gene[change2-i]
        Gene[change2-i] = temp

    return Gene

def CrossOver(Gene1, Gene2):
    n = len(Gene1)-1
    i, j = Give_2_rand_number(n-1)
    mark = [0]*(n)
    new_gene = [0]*(n+1)
    
    for k in range(i, j+1):
        new_gene[k] = Gene1[k]
        mark[Gene1[k]] = 1

    p_old = (j+1)%n
    if p_old == 0:
        p_old = p_old+1
    p_new = p_old
    
    for _ in range(n):
        if mark[Gene2[p_old]] == 1:
            p_old = p_old+1
            p_old = p_old%n
            if p_old == 0:
                p_old = p_old+1
            continue
        
        if new_gene[p_new] == True:
            break
        
        new_gene[p_new] = Gene2[p_old]
        mark[Gene2[p_old]] = 1
        p_old, p_new = p_old+1, p_new+1
        p_old, p_new = p_old%n, p_new%n
        if p_old == 0:
            p_old = p_old+1
        if p_new == 0:
            p_new = p_new+1
        
    return new_gene


def swap(Gene,i,j):
    temp = Gene[i]
    Gene[i] = Gene[j]
    Gene[j] = temp

    return Gene


def LocalSearch(Gene, cities):
    best_local = (Gene[0][:], Gene[1])
    for i in range(1, len(Gene[0])-1):
        for j in range(i+1, len(Gene[0])-1):
            new_gene = swap(Gene[0][:],i,j)
            new_fitness = Find_Fitness(new_gene, cities)
            if new_fitness < best_local[1]:
                best_local = (new_gene, new_fitness)
    
    return best_local


#checks if the best fitness has changes during the last N times
def Do_it(last_costs):
    if last_costs[-1] == 0:
        return True
    for i in range(len(last_costs)-1):
        if last_costs[i] != last_costs[i+1]:
            return True
    
    return False


#append the best fitness to the list of last best fitnesses
def Append_Cost(last_costs, new_cost):
    prev = new_cost
    for i in range(len(last_costs)):
        new = last_costs[i]
        last_costs[i] = prev
        prev = new 


def TSP(cities, size, number_of_first_population, N, Mutation_Probability, Cross_Over_Probability, LocalSearch_Probability, end_point):
    Population = []
    #generate the first population
    for _ in range(number_of_first_population):
        Gene = Create_Gene(size)
        Fitness = Find_Fitness(Gene, cities)
        Population.append((Gene,Fitness))

    Population.sort(key=lambda x:x[1])
    Population = Population[:(len(Population)*N)/100+1]
    print("Best initial population:")    
    print(Population[0][0])
    print("Cost:")
    print(Population[0][1])

    generation = 2
    #lasts_costs save the last N generation's best fitness
    last_costs = []
    for _ in range(end_point):
        last_costs.append(0)
    #append the fitness of the first generation to last_costs
    last_costs[0] = Population[0][1]

    #repeats untill the best fitness does not change for N times
    while(Do_it(last_costs)):
        childs = []
        #make a cross over between 2
        crossed_over = []
        for _ in range(len(Population)):
            if Rand_City(101) >= (100-Cross_Over_Probability) & len(Population) > 1:
                while True:
                    i = random.randint(0,len(Population)-1)
                    j = random.randint(0,len(Population)-1)
                    if i != j:
                        break
                new_gene = CrossOver(Population[i][0][:], Population[j][0][:])
                new_fitness = Find_Fitness(new_gene, cities)
                childs.append((new_gene, new_fitness))

        #make a mutation in each parent and consider them as a child and append them to the generation
        for i in range(len(childs)):
            if Rand_City(101) >= (100-Mutation_Probability):
                new_gene = Mutation(childs[i][0][:])
                new_fitness = Find_Fitness(new_gene, cities)
                Population.append((new_gene, new_fitness))
            else:
                Population.append(childs[i][:])
        

        #local search
        for i in range(len(Population)):
            if Rand_City(101) >= (100-LocalSearch_Probability):
                best_local = LocalSearch(Population[i], cities)
                Population[i] = best_local

        
        #sort the generation by the fitness
        Population.sort(key=lambda x:x[1])
        #choose the N% of best fitnesses
        Population = Population[:(len(Population)*N)/100 + 1]

        print("generation number: ", generation)
        print("best population:")    
        print(Population[0][0])
        print("cost:")
        print(Population[0][1])
        Append_Cost(last_costs, Population[0][1])
        generation += 1


size = 29
cities = [
    [0, 97, 205, 139, 86, 60, 220, 65, 111, 115, 227, 95, 82, 225, 168, 103, 266, 205, 149, 120, 58, 257, 152, 52, 180, 136, 82, 34, 145],
    [97, 0, 129, 103, 71, 105, 258, 154, 112, 65, 204, 150, 87, 176, 137, 142, 204, 148, 148, 49, 41, 211, 226, 116, 197, 89, 153, 124, 74],
    [205, 129, 0, 219, 125, 175, 386, 269, 134, 184, 313, 201, 215, 267, 248, 271, 274, 236, 272, 160, 151, 300, 350, 239, 322, 78, 276, 220, 60],
    [139, 103, 219, 0, 167, 182, 180, 162, 208, 39, 102, 227, 60, 86, 34, 96, 129, 69, 58, 60, 120, 119, 192, 114, 110, 192, 136, 173, 173],
    [86, 71, 125, 167, 0, 51, 296, 150, 42, 131, 268, 88, 131, 245, 201, 175, 275, 218, 202, 119, 50, 281, 238, 131, 244, 51, 166, 95, 69],
    [60, 105, 175, 182, 51, 0, 279, 114, 56, 150, 278, 46, 133, 266, 214, 162, 302, 242, 203, 146, 67, 300, 205, 111, 238, 98, 139, 52, 120],
    [220, 258, 386, 180, 296, 279, 0, 178, 328, 206, 147, 308, 172, 203, 165, 121, 251, 216, 122, 231, 249, 209, 111, 169, 72, 338, 144, 237, 331],
    [65, 154, 269, 162, 150, 114, 178, 0, 169, 151, 227, 133, 104, 242, 182, 84, 290, 230, 146, 165, 121, 270, 91, 48, 158, 200, 39, 64, 210],
    [111, 112, 134, 208, 42, 56, 328, 169, 0, 172, 309, 68, 169, 286, 242, 208, 315, 259, 240, 160, 90, 322, 260, 160, 281, 57, 192, 107, 90],
    [115, 65, 184, 39, 131, 150, 206, 151, 172, 0, 140, 195, 51, 117, 72, 104, 153, 93, 88, 25, 85, 152, 200, 104, 139, 154, 134, 149, 135],
    [227, 204, 313, 102, 268, 278, 147, 227, 309, 140, 0, 320, 146, 64, 68, 143, 106, 88, 81, 159, 219, 63, 216, 187, 88, 293, 191, 258, 272],
    [95, 150, 201, 227, 88, 46, 308, 133, 68, 195, 320, 0, 174, 311, 258, 196, 347, 288, 243, 192, 113, 345, 222, 144, 274, 124, 165, 71, 153],
    [82, 87, 215, 60, 131, 133, 172, 104, 169, 51, 146, 174, 0, 144, 86, 57, 189, 128, 71, 71, 82, 176, 150, 56, 114, 168, 83, 115, 160],
    [225, 176, 267, 86, 245, 266, 203, 242, 286, 117, 64, 311, 144, 0, 61, 165, 51, 32, 105, 127, 201, 36, 254, 196, 136, 260, 212, 258, 234],
    [168, 137, 248, 34, 201, 214, 165, 182, 242, 72, 68, 258, 86, 61, 0, 106, 110, 56, 49, 91, 153, 91, 197, 136, 94, 225, 151, 201, 205],
    [103, 142, 271, 96, 175, 162, 121, 84, 208, 104, 143, 196, 57, 165, 106, 0, 215, 159, 64, 126, 128, 190, 98, 53, 78, 218, 48, 127, 214],
    [266, 204, 274, 129, 275, 302, 251, 290, 315, 153, 106, 347, 189, 51, 110, 215, 0, 61, 155, 157, 235, 47, 305, 243, 186, 282, 261, 300, 252],
    [205, 148, 236, 69, 218, 242, 216, 230, 259, 93, 88, 288, 128, 32, 56, 159, 61, 0, 105, 100, 176, 66, 253, 183, 146, 231, 203, 239, 204],
    [149, 148, 272, 58, 202, 203, 122, 146, 240, 88, 81, 243, 71, 105, 49, 64, 155, 105, 0, 113, 152, 127, 150, 106, 52, 235, 112, 179, 221],
    [120, 49, 160, 60, 119, 146, 231, 165, 160, 25, 159, 192, 71, 127, 91, 126, 157, 100, 113, 0, 79, 163, 220, 119, 164, 135, 152, 153, 114],
    [58, 41, 151, 120, 50, 67, 249, 121, 90, 85, 219, 113, 82, 201, 153, 128, 235, 176, 152, 79, 0, 236, 201, 90, 195, 90, 127, 84, 91],
    [257, 211, 300, 119, 281, 300, 209, 270, 322, 152, 63, 345, 176, 36, 91, 190, 47, 66, 127, 163, 236, 0, 273, 226, 148, 296, 238, 291, 269],
    [152, 226, 350, 192, 238, 205, 111, 91, 260, 200, 216, 222, 150, 254, 197, 98, 305, 253, 150, 220, 201, 273, 0, 112, 130, 286, 74, 155, 291],
    [52, 116, 239, 114, 131, 111, 169, 48, 160, 104, 187, 144, 56, 196, 136, 53, 243, 183, 106, 119, 90, 226, 112, 0, 130, 178, 38, 75, 180],
    [180, 197, 322, 110, 244, 238, 72, 158, 281, 139, 88, 274, 114, 136, 94, 78, 186, 146, 52, 164, 195, 148, 130, 130, 0, 281, 120, 205, 270],
    [136, 89, 78, 192, 51, 98, 338, 200, 57, 154, 293, 124, 168, 260, 225, 218, 282, 231, 235, 135, 90, 296, 286, 178, 281, 0, 213, 145, 36],
    [82, 153, 276, 136, 166, 139, 144, 39, 192, 134, 191, 165, 83, 212, 151, 48, 261, 203, 112, 152, 127, 238, 74, 38, 120, 213, 0, 94, 217],
    [34, 124, 220, 173, 95, 52, 237, 64, 107, 149, 258, 71, 115, 258, 201, 127, 300, 239, 179, 153, 84, 291, 155, 75, 205, 145, 94, 0, 162],
    [145, 74, 60, 173, 69, 120, 331, 210, 90, 135, 272, 153, 160, 234, 205, 214, 252, 204, 221, 114, 91, 269, 291, 180, 270, 36, 217, 162, 0]
    ]
number_of_first_population = 100
N = 60 #N%  of the best fitnesses will be chosen
Mutation_Probability = 50 #every gene have 50% probability to mutate
Cross_Over_Probability = 50
LocalSearch_Probability = 70
end_point = 200 #after 100 times that th best fitness didn't change it it will end
TSP(cities, size, number_of_first_population, N, Mutation_Probability, Cross_Over_Probability, LocalSearch_Probability, end_point)