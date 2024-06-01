import random

def preproccesing(array, l):
    arraylen = len(array)
    solutions = [[] for _ in range(arraylen)]
    for i in range(arraylen):
        solutions[i].append(i)
        helpvalueup = i
        helpvaluedown = i
        for j in range(arraylen):
            if i != j:
                if array[helpvalueup][:l - 1] == array[j][1:l]:
                    solutions[i].append(j)
                    helpvalueup = j
                elif array[helpvaluedown][1:l] == array[j][:l - 1]:
                    solutions[i].insert(0, j)
                    helpvaluedown = j
    return solutions

def joinwords(indexarray, array, l):
    newarray = [[] for _ in range(len(indexarray))]
    arraylen = len(indexarray)
    for i in range(arraylen):
        stringofthearray = ''
        for j in range(len(indexarray[i])):
            stringofthearray += array[indexarray[i][j]]
        newarray[i] = stringofthearray
    return newarray

def deletethesame(array):
    for i in range(len(array) - 1, -1, -1):
        for j in range(len(array) - 1, -1, -1):
            if i != j:
                if array[i][0] == array[j][0] and array[i][-1] == array[j][-1]:
                    del array[i]
                    i -= 1
    return array

def openfile(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        return lines

def fitness(sequence, target_length):
    length_diff = abs(len(sequence) - target_length)
    return 1 / (1 + length_diff)

def create_population(joined_words, population_size, target_length):
    population = []
    for _ in range(population_size):
        individual = []
        current_length = 0
        while current_length < target_length:
            word = random.choice(joined_words)
            individual.append(word)
            current_length += len(word)
        if current_length > target_length:
            individual = individual[:-1]  # Remove the last word if it exceeds the target length
        population.append(individual)
    return population

def select_parents(population, target_length):
    population.sort(key=lambda x: fitness(''.join(x), target_length), reverse=True)
    return population[:len(population) // 2]

def crossover(parent1, parent2, target_length):
    crossover_point = random.randint(0, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1[:target_length], child2[:target_length]

def mutate(individual, mutation_rate, joined_words, target_length):
    if random.random() < mutation_rate:
        i = random.randint(0, len(individual) - 1)
        j = random.randint(0, len(joined_words) - 1)
        individual[i] = joined_words[j]
        current_length = sum(len(word) for word in individual)
        while current_length < target_length:
            word = random.choice(joined_words)
            individual.append(word)
            current_length += len(word)
        if current_length > target_length:
            individual = individual[:-1]  # Remove the last word if it exceeds the target length
    return individual
