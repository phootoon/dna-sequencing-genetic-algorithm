import functions
import time

# Parameters for the genetic algorithm and DNA sequence generation
POPULATION_SIZE = 200
GENERATIONS = 500
MUTATION_RATE = 0.1
DNA_WORD_LENGTH = 6
TARGET_LENGTH = 509

# Parameters for file reading
FILE_PATH = 'data.txt'

if __name__ == '__main__':
    average_coverage = 0.0
    average_execution_time = 0.0
    repetitions = 10
    help_variable = 0
    max_val = float('-inf')  # Initialize to negative infinity to handle negative numbers
    min_val = float('inf')
    # Read DNA words from the file
    resoults = [[] for _ in range(repetitions)]
    for i in range(repetitions):
        generated_data = functions.openfile(FILE_PATH)

        # Test the genetic algorithm with the generated data
        best_sequence_str, execution_time, coverage_percentage = functions.test_genetic_algorithm(
            generated_data,
            POPULATION_SIZE,
            GENERATIONS,
            MUTATION_RATE,
            TARGET_LENGTH,
            DNA_WORD_LENGTH
        )

        print(f"Best Sequence: {best_sequence_str}")
        print(f"Execution Time: {execution_time} seconds")
        print(f"Coverage Percentage: {coverage_percentage}%")
        resoults[i].append(coverage_percentage)
        resoults[i].append(execution_time)

    for i in range(repetitions):
        # Update maximum value
        help_variable = resoults[i][0]
        if help_variable > max_val:
            max_val = help_variable
        if help_variable < min_val:
            min_val = help_variable
        average_coverage += help_variable
        average_execution_time += resoults[i][1]
    average_coverage = average_coverage/repetitions
    average_execution_time = average_execution_time/repetitions

        # Update minimum value
    print(average_coverage)
    print(average_execution_time)
    print(max_val)
    print(min_val)