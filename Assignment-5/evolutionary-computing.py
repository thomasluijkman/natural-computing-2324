import os
import random
from numpy import mean
import matplotlib.pyplot as plt

# Parameters
SEED = 42
K = 2
TARGET = 'ThisStuffIsHard'
TARGET_LENGTH = len(TARGET)
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
P_C = 1
MU = 1.0 / TARGET_LENGTH
POP_SIZE = 200
MAX_GENS = 200

def print_parameters():
    print_string = f"""
Running evolutionary algorithm with the following parameters:
K               = {K}
Target          = {TARGET}
Alphabet        = {ALPHABET}
P_C             = {P_C}
mu              = {MU}
Population size = {POP_SIZE}
    """
    print(print_string)

# Fitness function
def string_similarity(a, b):
    # assumes target string and searching strings are all of the same length
    assert(len(a) == len(b))
    # higher fitness = better individual, so count the number of correct letters in string
    dist = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            dist += 1
    return float(dist) / TARGET_LENGTH

fitness = string_similarity

# Plotting
def plot_results(data, labels):
    plt.figure()
    ticks = range(1,len(data)+1)
    plt.violinplot(data)
    plt.xticks(ticks, labels)
    plt.ylabel('Number of generations')
    plt.savefig('results/ex3/graph.png')

def hamming_distance(a, b):
    # assumes target string and searching strings are all of the same length
    assert(len(a) == len(b))
    dist = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            dist += 1
    return dist

def mean_pairwise_distance(population, subsample_size=1):
    # subsample_size is a fraction of the total population
    total = []
    data = random.choices(population, k=int(subsample_size * len(population)))
    for point in data:
        for point2 in data:
            total.append(hamming_distance(point, point2))
    return mean(total)

def plot_distances(data, labels):
    plt.figure()
    colors = ['green', 'red', 'blue']
    for i in range(len(data)):
        for j in range(len(data[i])):
            plt.plot(data[i][j], lw=0.5, color=colors[i], label=labels[i])
    plt.xticks(range(0,20,2), [str(x) for x in range(0,200,20)])
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.grid(visible=True, which='both', axis='both')
    plt.legend(by_label.values(), by_label.keys())
    plt.ylabel('Mean pairwise Hamming distance')
    plt.xlabel('Generation')
    plt.savefig('results/ex3/distances.png')

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
    return mutated

def string_search_ga(verbose=False):
    # Step 1: Population of candidate solutions
    population = initialise_population()
    distances = []
    # Repeat steps 2-4
    i = 0
    while i < MAX_GENS:
        max_fitness, fittest_index = find_fittest(population)
        if i % 10 == 0:
            distances.append(mean_pairwise_distance(population))
        if verbose:
            print(f'Closest string in generation {i}:\t{population[fittest_index]} (fitness: {max_fitness})')
        if population[fittest_index] == TARGET:
            return i, distances # only need to return time in generations to find target string
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
    return -10, distances # negative return means max generations were reached without target string being found


def run_experiment(no_experiments=10, verbose=True):
    global MU
    # K = 2, MU = 1/L
    data = []
    dist_data = []
    if verbose:
        print_parameters()
    for i in range(no_experiments):
        if verbose:
            print(f"Running experiment {i} in current parameter set")
        gen_data, distances = string_search_ga()
        data.append(gen_data)
        dist_data.append(distances)
    return data, dist_data

def main():
    global MU
    random.seed(SEED)
    if not os.path.exists('results/ex3'):
        os.makedirs('results/ex3')
    initial_params, initial_dist = run_experiment()

    # MU = 0
    MU = 0
    no_mutation, no_mu_dist = run_experiment()

    # MU = 3/L
    MU = 3.0 / TARGET_LENGTH
    wild_mutation, wild_mu_dist = run_experiment()

    # plot data
    data = [initial_params, no_mutation, wild_mutation]
    dist_data = [initial_dist, no_mu_dist, wild_mu_dist]
    labels = ['MU = 1/L', 'MU = 0', 'MU = 3/L']
    plot_results(data, labels)
    plot_distances(dist_data, labels)

if __name__ == '__main__':
    main()