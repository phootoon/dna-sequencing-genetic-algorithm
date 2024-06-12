import random
import time

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


def fitness(sequence_indexes, target_length, processed_data, l):
    sequence = [processed_data[idx] for idx in sequence_indexes]
    length_diff = abs(len(''.join(sequence)) - target_length)

    # Calculate overlap fitness using indexes to look up words in processed_data
    overlap_fitness = 0
    wordlength_fitness = 0
    for i in range(len(sequence_indexes) - 1):
        word1 = processed_data[sequence_indexes[i]]
        word2 = processed_data[sequence_indexes[i + 1]]
        overlap_fitness += calculate_overlap(word1, word2, l)

        wordlength_fitness += len(processed_data[sequence_indexes[i]])-10

    return (1 / (1 + length_diff))*10 + (overlap_fitness / 60) + (wordlength_fitness/40)


def calculate_overlap(seq1, seq2, l):
    """Calculate the number of overlapping letters using l-2 letters from the end of seq1 and the beginning of seq2."""
    overlap_length = l - 2
    overlap_begin = 0
    lenseq1 = len(seq1)
    for i in range(overlap_length):
        if seq1[lenseq1-overlap_length+i] == seq2[i]:
            overlap_begin+=1

    return overlap_begin


def create_population(processed_data, population_size, target_length):
    population = []
    data_length = len(processed_data)
    for _ in range(population_size):
        individual = []
        current_length = 0
        while current_length < target_length:
            word_index = random.randint(0, data_length - 1)
            individual.append(word_index)
            current_length += len(processed_data[word_index])
        if current_length > target_length:
            individual.pop()  # Remove the last word if it exceeds the target length
        population.append(individual)
    return population

def select_parents(population, target_length, processed_data, l):
    population.sort(key=lambda x: fitness(x, target_length, processed_data, l), reverse=True)
    return population[:len(population) // 2]

def crossover(parent1, parent2, target_length):
    crossover_point = random.randint(0, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1[:target_length], child2[:target_length]

def mutate(individual, mutation_rate, processed_data, target_length):
    data_length = len(processed_data)
    if random.random() < mutation_rate:
        i = random.randint(0, len(individual) - 1)
        j = random.randint(0, data_length - 1)
        individual[i] = j
        current_length = sum(len(processed_data[idx]) for idx in individual)
        while current_length < target_length:
            word_index = random.randint(0, data_length - 1)
            individual.append(word_index)
            current_length += len(processed_data[word_index])
        if current_length > target_length:
            individual.pop()  # Remove the last word if it exceeds the target length
    return individual


def genetic_algorithm(processed_data, population_size, generations, mutation_rate, target_length, dna_word_length):
    population = create_population(processed_data, population_size, target_length)

    best_individuals = []

    for generation in range(generations):
        parents = select_parents(population, target_length, processed_data, dna_word_length)

        # Elitism: Preserve the best individual
        best_individual = max(parents, key=lambda x: fitness(x, target_length, processed_data, dna_word_length))
        best_individuals.append(best_individual)

        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = crossover(parents[i], parents[i + 1], target_length)
                offspring.append(mutate(child1, mutation_rate, processed_data, target_length))
                offspring.append(mutate(child2, mutation_rate, processed_data, target_length))

        # Include the best individuals from the previous generation (elitism)
        population = parents + offspring

        # Add best individuals back into the population
        population.extend(best_individuals)

        # Trim population to maintain size
        population = population[:population_size]

        # Calculate the best fitness
        best_sequence = max(population, key=lambda x: fitness(x, target_length, processed_data, dna_word_length))
        best_fitness = fitness(best_sequence, target_length, processed_data, dna_word_length)

        # Print progress
        if generation % 10 == 0 or generation == generations - 1:
            print(f"Generation {generation}: Best Fitness = {best_fitness}")

        # Adaptive mutation rate: Decrease if the best solution is not improving
        if len(best_individuals) > 10 and all(
                fitness(ind, target_length, processed_data, dna_word_length) == best_fitness for ind in
                best_individuals[-10:]):
            mutation_rate = min(1.0, mutation_rate + 0.01)
        else:
            mutation_rate = max(0.01, mutation_rate - 0.01)

    return best_sequence


def calculate_efficiency(best_sequence, target_sequence):
    """Calculate the percentage of correctly sequenced bases."""
    match_count = sum(1 for a, b in zip(best_sequence, target_sequence) if a == b)
    efficiency = (match_count / len(target_sequence)) * 100
    return efficiency

def generate_dna_sequence(length):
    """Generate a random DNA sequence of a given length."""
    return ''.join(random.choice('ACGT') for _ in range(length))

def introduce_errors(sequence, positive_error_rate, negative_error_rate):
    """Introduce positive and negative errors into the DNA sequence."""
    sequence_list = list(sequence)

    # Introduce positive errors (insertions)
    num_positive_errors = int(len(sequence) * positive_error_rate)
    for _ in range(num_positive_errors):
        insert_pos = random.randint(0, len(sequence_list))
        insert_base = random.choice('ACGT')
        sequence_list.insert(insert_pos, insert_base)

    # Introduce negative errors (deletions)
    num_negative_errors = int(len(sequence) * negative_error_rate)
    for _ in range(num_negative_errors):
        if sequence_list:
            del_pos = random.randint(0, len(sequence_list) - 1)
            sequence_list.pop(del_pos)

    return ''.join(sequence_list)

def generate_dna_words_with_errors(num_words, word_length, positive_error_rate, negative_error_rate):
    """Generate a list of DNA words with specified errors."""
    words = [generate_dna_sequence(word_length) for _ in range(num_words)]
    words_with_errors = [introduce_errors(word, positive_error_rate, negative_error_rate) for word in words]
    return words_with_errors

def test_genetic_algorithm(data, population_size, generations, mutation_rate, target_length, dna_word_length):
    processed_data = preprocess_spectrum(data, dna_word_length)

    start_time = time.time()
    best_sequence_indexes = genetic_algorithm(
        processed_data,
        population_size,
        generations,
        mutation_rate,
        target_length,
        dna_word_length
    )
    end_time = time.time()

    best_sequence_str = ''.join([processed_data[idx] for idx in best_sequence_indexes])

    # Use the data directly as target sequence for coverage calculation
    coverage = calculate_coverage(best_sequence_str, ''.join(data))
    coverage_percentage = calculate_coverage_percentage(coverage)

    print("Best Sequence:", best_sequence_str)
    print("Best Sequence Length:", len(best_sequence_str))
    print("Indexes of words in best sequence:", best_sequence_indexes)
    print("Execution Time:", end_time - start_time, "seconds")
    print("Coverage Percentage:", coverage_percentage, "%")

    return best_sequence_str, end_time - start_time, coverage_percentage

def calculate_coverage(best_sequence, target_sequence):
    coverage = [0] * len(target_sequence)
    best_sequence_str = best_sequence
    len_best = len(best_sequence_str)

    for i in range(len(target_sequence)):
        for j in range(len_best):
            if target_sequence[i:i + len_best - j] == best_sequence_str[j:]:
                for k in range(len_best - j):
                    if i + k < len(target_sequence):
                        coverage[i + k] = 1  # Mark position as covered
                break  # Exit loop once match is found
    return coverage

def calculate_coverage_percentage(coverage):
    covered_bases = sum(1 for count in coverage if count > 0)
    total_bases = len(coverage)
    coverage_percentage = (covered_bases / total_bases) * 100
    return coverage_percentage
