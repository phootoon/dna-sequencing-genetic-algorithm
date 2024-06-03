import random


def preprocess_spectrum(fragments, l):
    def can_merge(f1, f2):
        """Check if the last l-1 characters of f1 match the first l-1 characters of f2."""
        return f1[-(l - 1):] == f2[:(l - 1)]

    used = set()
    new_spectrum = []

    for i in range(len(fragments)):
        if i in used:
            continue
        chain = fragments[i]
        used.add(i)

        while True:
            found = False
            for j in range(len(fragments)):
                if j not in used and can_merge(chain, fragments[j]):
                    chain += fragments[j][-(l - 1):][-1]  # Add only the non-overlapping character
                    used.add(j)
                    found = True
                    break
            if not found:
                break

        new_spectrum.append(chain)

    return new_spectrum


def openfile(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        return lines


def calculate_overlap(seq1, seq2, l):
    """Calculate the number of overlapping letters from the beginning and end of the sequences."""
    min_length = min(len(seq1), len(seq2))
    overlap_begin = sum(1 for i in range(min(l - 2, min_length)) if seq1[i] == seq2[i])
    overlap_end = sum(1 for i in range(min(l - 2, min_length)) if seq1[-(i + 1)] == seq2[-(i + 1)])
    return overlap_begin + overlap_end


def fitness(sequence, target_length, l):
    length_diff = abs(len(sequence) - target_length)

    # Calculate overlap fitness
    overlap_fitness = 0
    for i in range(len(sequence) - 1):
        overlap_fitness += calculate_overlap(sequence[i], sequence[i + 1], l)

    # Combine the length fitness and overlap fitness
    return 1 / (1 + length_diff) + overlap_fitness / 40


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


def select_parents(population, target_length, l):
    population.sort(key=lambda x: fitness(''.join(x), target_length, l), reverse=True)
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
