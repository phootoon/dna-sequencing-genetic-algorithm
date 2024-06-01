import functions

# Parameters for the genetic algorithm
POPULATION_SIZE = 100
GENERATIONS = 1000
MUTATION_RATE = 0.01
DNA_WORD_LENGTH = 10
TARGET_LENGTH = 206

# Read and preprocess the data
if __name__ == '__main__':
    file_path = 'data.txt'
    data = functions.openfile(file_path)
    processeddata = functions.preproccesing(data, DNA_WORD_LENGTH)
    processednorepetitions = functions.deletethesame(processeddata)
    joined_words = functions.joinwords(processednorepetitions, data, DNA_WORD_LENGTH)

    # Run the genetic algorithm
    def genetic_algorithm():
        population = functions.create_population(joined_words, POPULATION_SIZE, TARGET_LENGTH)
        for generation in range(GENERATIONS):
            parents = functions.select_parents(population, TARGET_LENGTH)
            offspring = []
            for i in range(0, len(parents), 2):
                if i + 1 < len(parents):
                    child1, child2 = functions.crossover(parents[i], parents[i + 1], TARGET_LENGTH)
                    offspring.append(functions.mutate(child1, MUTATION_RATE, joined_words, TARGET_LENGTH))
                    offspring.append(functions.mutate(child2, MUTATION_RATE, joined_words, TARGET_LENGTH))
            population = parents + offspring
            best_sequence = max(population, key=lambda x: functions.fitness(''.join(x), TARGET_LENGTH))
            best_fitness = functions.fitness(''.join(best_sequence), TARGET_LENGTH)
            print(f"Generation {generation}: Best Fitness = {best_fitness}")
            if len(''.join(best_sequence)) == TARGET_LENGTH:
                break
        return best_sequence

    # Get the best sequence
    best_sequence = genetic_algorithm()
    best_sequence_str = ''.join(best_sequence)
    print("Best Sequence:", best_sequence_str)
    print("Best Sequence Length:", len(best_sequence_str))
    print("Indexes of words in best sequence:", [joined_words.index(word) for word in best_sequence])
