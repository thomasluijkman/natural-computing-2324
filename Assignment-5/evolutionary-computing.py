import os
import random
import matplotlib.pyplot as plt

# Parameters
K = 2
TARGET = 'ThisStuffIsHard'
TARGET_LENGTH = len(TARGET)
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
P_C = 1
MU = 1.0 / TARGET_LENGTH
POP_SIZE = 200
MAX_GENS = 1000000

# Fitness function
def string_similarity(a, b):
    # assumes target string and searching strings are all of the same length
    assert(len(a) == len(b))
    # higher fitness = better individual, so count the number of correct letters in string
    dist = 0
    for i in range(min(len(a), len(b))):
        if a[i] == b[i]:
            dist += 1
    return dist

fitness = string_similarity

# Evolutionary algorithms
def initialise_population():
    population = []
    for _ in range(POP_SIZE):
        population.append(''.join([random.choice(ALPHABET) for _ in range(TARGET_LENGTH)]))
    return population

def calc_population_fitness(population):
    pop_fitness = []
    for individual in population:
        pop_fitness.append(fitness(individual, TARGET))
    return pop_fitness

def get_parents_with_fitness(pop_with_fitness):
    sample = random.choices(pop_with_fitness, k=K)
    parent0 = max(sample, key=lambda item: item[1])[0]
    sample = random.choices(pop_with_fitness, k=K)
    parent1 = max(sample, key=lambda item: item[1])[0]
    return (parent0, parent1)

def find_fittest(population):
    max_fitness = 0
    index = 0
    for i in range(len(population)):
        this_fitness = fitness(population[i], TARGET)
        if this_fitness > max_fitness:
            max_fitness = this_fitness
            index = i
    return max_fitness, index

def crossover(a, b):
    assert(len(a) == len(b))
    cross_point = random.randrange(len(a))
    child_a = a[:cross_point] + b[cross_point:]
    child_b = b[:cross_point] + a[cross_point:]
    return [child_a, child_b]

def mutate(a):
    mutated = ''
    for i in range(len(a)):
        if random.random() <= MU:
            mutated += random.choice(ALPHABET)
        else:
            mutated += a[i]
    return a

def string_search_ga(verbose=True):
    # Step 1: Population of candidate solutions
    population = initialise_population()
    # Repeat steps 2-4
    i = 0
    while i < MAX_GENS:
        max_fitness, fittest_index = find_fittest(population)
        if verbose:
            print(f'Closest string in generation {i}:\t{population[fittest_index]} (fitness: {max_fitness})')
        if population[fittest_index] == TARGET:
            return i # only need to return time in generations to find target string
        new_population = []
        # Step 2: Determine fitness for every solution
        pop_fitness = calc_population_fitness(population)
        pop_with_fitness = list(zip(population, pop_fitness))
        for _ in range(int(POP_SIZE / 2)):
            # Step 3: Select parents for new generation
            parents = get_parents_with_fitness(pop_with_fitness)
            # Step 4a: Introduce variation via crossover
            new_population += crossover(parents[0], parents[1])
        assert(len(new_population) == POP_SIZE)
        # Step 4b: Introduce variation via mutation
        population = [mutate(individual) for individual in new_population]
        i += 1
    return -1 # negative return means max generations were reached without target string being found


def run_experiment():
    converged = string_search_ga(verbose=True)
    if(converged >= 0):
        print(f"Converged after {str(converged)} generations.")

def main():
    if not os.path.exists('results/ex3'):
        os.makedirs('results/ex3')
    run_experiment()
    

if __name__ == '__main__':
    main()