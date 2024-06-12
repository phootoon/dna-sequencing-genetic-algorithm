import random
import numpy as np


# Helper function to calculate overlap between two fragments
def overlap(a, b):
    max_overlap = min(len(a), len(b)) - 1
    for i in range(max_overlap, 0, -1):
        if a[-i:] == b[:i]:
            return i
    return 0


# Preprocessing to reduce the size of the spectrum
def preprocess(spectrum):
    merged_spectrum = []
    used = set()

    for fragment in spectrum:
        if fragment in used:
            continue
        chain = [fragment]
        used.add(fragment)

        while True:
            last_fragment = chain[-1]
            found = False
            for next_fragment in spectrum:
                if next_fragment in used:
                    continue
                if overlap(last_fragment, next_fragment) == len(last_fragment) - 1:
                    chain.append(next_fragment)
                    used.add(next_fragment)
                    found = True
                    break
            if not found:
                break

        merged_fragment = ''.join([chain[0]] + [f[-1] for f in chain[1:]])
        merged_spectrum.append(merged_fragment)

    return merged_spectrum


# Function to calculate fitness of a sequence
def fitness(sequence, n, l):
    total_overlap = sum(overlap(sequence[i], sequence[i + 1]) for i in range(len(sequence) - 1))
    bonus = 100 if len(sequence) == n + l - 1 else 100 / abs(len(sequence) - (n + l - 1))
    return total_overlap + bonus


# Function to perform crossover between two parents
def crossover(parent1, parent2):
    length = len(parent1)
    if length < 4:
        return parent1, parent2  # No crossover if not enough points
    cut_points = sorted(random.sample(range(1, length), 3))
    child1 = parent1[:cut_points[0]] + parent2[cut_points[0]:cut_points[1]] + parent1[
                                                                              cut_points[1]:cut_points[2]] + parent2[
                                                                                                             cut_points[
                                                                                                                 2]:]
    child2 = parent2[:cut_points[0]] + parent1[cut_points[0]:cut_points[1]] + parent2[
                                                                              cut_points[1]:cut_points[2]] + parent1[
                                                                                                             cut_points[
                                                                                                                 2]:]
    return child1, child2


# Function to perform mutation on an offspring
def mutate(offspring):
    for i in range(len(offspring)):
        if random.random() < 0.1:
            j = random.randint(0, len(offspring) - 1)
            offspring[i], offspring[j] = offspring[j], offspring[i]


# Local optimization function
def local_optimization(sequence, n, l):
    best_fitness = fitness(sequence, n, l)
    best_sequence = sequence[:]

    for i in range(len(sequence) - 1):
        for j in range(i + 1, len(sequence)):
            new_sequence = sequence[:i] + sequence[i:j][::-1] + sequence[j:]
            new_fitness = fitness(new_sequence, n, l)
            if new_fitness > best_fitness:
                best_fitness = new_fitness
                best_sequence = new_sequence[:]

    return best_sequence


# Main genetic algorithm function
def genetic_algorithm(spectrum, n, l):
    population_size = 120
    generations = 0
    max_generations = 500
    no_improvement_generations = 200
    population = [random.sample(spectrum, len(spectrum)) for _ in range(population_size)]
    best_fitness = 0
    best_sequence = []

    while generations < max_generations:
        population = sorted(population, key=lambda seq: -fitness(seq, n, l))
        new_population = population[:population_size // 2]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            child1 = local_optimization(child1, n, l)
            child2 = local_optimization(child2, n, l)
            new_population.extend([child1, child2])

        population = new_population
        generations += 1

        current_best_fitness = fitness(population[0], n, l)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_sequence = population[0]
            no_improvement_generations = 0
        else:
            no_improvement_generations += 1

        if no_improvement_generations >= 400:
            break

    return best_sequence


# Read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return data


# Example usage with the uploaded file
file_path = 'data.txt'
spectrum = read_data(file_path)
preprocessed_spectrum = preprocess(spectrum)
n = 206
l = 10
best_sequence = genetic_algorithm(preprocessed_spectrum, n, l)
print("Best sequence:", best_sequence)
