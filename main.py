import functions

l = 10

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = 'data.txt'
    data = functions.openfile(file_path)
    processeddata = functions.preproccesing(data,l)
    print((processeddata)," - iloś elementów po precossenigu", len(data), " - ilość elementó początkowych")
    listofindexestodelete=[]
    processednorepetitions = functions.deletethesame(processeddata)
    # print((processednorepetitions))
    joined_words = functions.joinwords(processednorepetitions,data,l)
    # print(joined_words)

    # Define parameters for the genetic algorithm
    pc_count = len(joined_words[0])
    task_times = [1] * len(joined_words)  # Assuming each task takes equal time, modify as needed
    starting_solution = [0] * len(joined_words)
    pop_size = 100
    max_generations = 1000
    mutation_probability = 0.05
    task_count = len(joined_words)

    # Solve the sequencing problem using the genetic algorithm
    best_fitness, best_solution = functions.solve_pcmax(pc_count, task_times, starting_solution, pop_size, max_generations,
                                              mutation_probability, task_count)
    print("Best fitness:", best_fitness)
    print("Best solution:", best_solution)
    counter = 0
    finalarray = []
    for i in best_solution:
        counter += len(joined_words[i])
        finalarray.append(joined_words[i])

    print(counter)
    print(finalarray)





    # pc_count = len(processednorepetitions)  # Number of unique DNA segments
    # task_times = [len(data[i]) for i in
    #               range(len(data))]  # Assuming each task time corresponds to the length of the segment
    # starting_solution = [functions.random.randint(0, pc_count - 1) for _ in range(len(data))]
    # pop_size = 50  # Population size for the genetic algorithm
    # max_generations = 1000  # Maximum number of generations
    # mutation_probability = 0.01  # Mutation probability
    # task_count = len(data)  # Number of tasks
    #
    # best_fitness, best_solution = functions.solve_pcmax(pc_count, task_times, starting_solution, pop_size, max_generations,
    #                                           mutation_probability, task_count)
    #
    # print(f"Best Fitness: {best_fitness}")
    # print(f"Best Solution: {best_solution}")
    #
    # # Convert the best solution indices to actual sequences
    # assembled_dna = [data[idx] for idx in best_solution]
    #
    # print(f"Assembled DNA Sequence: {''.join(assembled_dna)}")
    #
