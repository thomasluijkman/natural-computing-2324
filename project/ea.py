from agent import Agent, DecisionTables, LOOKUP_ACE, LOOKUP_PAIR, LOOKUP_REGULAR
from game import Actions
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import multiprocessing as mp

K = 20
SEED = 42
POP_SIZE = 100
TABLE_SIZE = (16*10)+(8*10)+(10*10) #360
MU = 10 / TABLE_SIZE
MAX_GENS = 250
NR_ROUNDS = 100000
CROSSOVER = True

########################################
# Functions for evolutionary algorithm #
########################################

# Create population with random agents
def initialise_population():
    population = []
    for _ in range(POP_SIZE):
        population.append(Agent())
    return population

# Let every agent play Blackjack for [NR_ROUNDS] rounds
# def run_experiment(population):
#     i = 1
#     for agent in population:
#         i += 1
#         agent.playGame(NR_ROUNDS)

def play_game(agent):
    agent.playGame(NR_ROUNDS)
    return agent

def run_experiment(population):
    with mp.Pool() as pool:
        updated_population = pool.map(play_game, population)
    return updated_population

# Returns a list with the fitness score for each individual
def calc_population_fitness(population):
    pop_fitness = []
    for individual in population:
        pop_fitness.append(individual.getAgentFitness(NR_ROUNDS))
    return pop_fitness

# Returns the two best individuals from a random selection of [K] individuals in the population
def get_parents_with_fitness(pop_with_fitness):
    sample = random.choices(pop_with_fitness, k=K)
    parent0 = max(sample, key=lambda item: item[1])[0]
    sample = random.choices(pop_with_fitness, k=K)
    parent1 = max(sample, key=lambda item: item[1])[0]
    return (parent0, parent1)

# Finds the fittest individual in a population
def find_fittest(population):
    highest = -sys.maxsize - 1
    best_agent = None
    for agent in population:
        fitness = agent.getAgentFitness(NR_ROUNDS)
        if fitness > highest:
            highest = fitness
            best_agent = agent
    return best_agent, highest
        
def crossover_rows(a, b):
    a_tables = a.decision_tables.getAllTables()
    b_tables = b.decision_tables.getAllTables()

    child1_tables = []
    child2_tables = []

    for (table_a, table_b) in list(zip(a_tables, b_tables)):
        # Get the dimensions of the arrays
        rows, cols = table_a.shape

        # Randomly select the row index for crossover
        crossover_point = random.randint(1, rows-2)

        # Initialize an empty array to store the result
        child1_table = np.empty((rows, cols), dtype=table_a.dtype)
        child2_table = np.empty((rows, cols), dtype=table_a.dtype)

        # Copy rows from array a and b based on the crossover point
        child1_table[:crossover_point, :] = table_a[:crossover_point, :]
        child1_table[crossover_point:, :] = table_b[crossover_point:, :]

        child2_table[:crossover_point, :] = table_b[:crossover_point, :]
        child2_table[crossover_point:, :] = table_a[crossover_point:, :]

        child1_tables.append(child1_table)
        child2_tables.append(child2_table)

    child1 = Agent(decision_tables=DecisionTables(all_tables=child1_tables))
    child2 = Agent(decision_tables=DecisionTables(all_tables=child2_tables))

    return [child1, child2]

def crossover_quadrants(a, b):
    a_tables = a.decision_tables.getAllTables()
    b_tables = b.decision_tables.getAllTables()

    child1_tables = []
    child2_tables = []

    for (table_a, table_b) in list(zip(a_tables, b_tables)):
        rows, cols = table_a.shape

        c_row = random.randint(1, rows-2)
        c_col = random.randint(1, cols-2)

        # Initialize an empty array to store the result
        child1_table = np.empty((rows, cols), dtype=table_a.dtype)
        child2_table = np.empty((rows, cols), dtype=table_b.dtype)

        # Copy the children from four quadrants
        # # Quadrant 1
        child1_table[:c_row, :c_col] = table_a[:c_row, :c_col]
        child2_table[:c_row, :c_col] = table_b[:c_row, :c_col]

        # # Quadrant 2
        child1_table[c_row:, :c_col] = table_b[c_row:, :c_col]
        child2_table[c_row:, :c_col] = table_a[c_row:, :c_col]

        # # Quadrant 3
        child1_table[:c_row, c_col:] = table_a[:c_row, c_col:]
        child2_table[:c_row, c_col:] = table_b[:c_row, c_col:]

        # # Quadrant 4
        child1_table[c_row:, c_col:] = table_b[c_row:, c_col:]
        child2_table[c_row:, c_col:] = table_a[c_row:, c_col:]

        child1_tables.append(child1_table)
        child2_tables.append(child2_table)

    child1 = Agent(decision_tables=DecisionTables(all_tables=child1_tables))
    child2 = Agent(decision_tables=DecisionTables(all_tables=child2_tables))

    return [child1, child2]


def mutate(agent):
    tables = agent.decision_tables.getAllTables()
    for table_num, table in enumerate(tables):
        for x_pos, x in enumerate(table):
            for y_pos, y in enumerate(x):
                if random.random() <= MU:
                    if table_num == LOOKUP_PAIR: # If pairs table
                        new_action = random.choice(list(Actions))
                    else:
                        new_action = random.choice([Actions.HT,Actions.ST, Actions.DH, Actions.DS])
                    tables[table_num][x_pos][y_pos] = new_action
    new_agent = Agent(tables)
    return new_agent

crossover = crossover_quadrants

def evolutionary_algorithm(verbose=True):
    global MU
    # Step 1: Population of candidate solutions
    population = initialise_population()
    # Repeat steps 2-4
    i = 0
    # Keep track of fitest agents
    fitness_over_gen = []
    #run for set amount of generations
    print("Running for " + str(MAX_GENS) + " generations with " + str(POP_SIZE) + " agents each with " + str(NR_ROUNDS) + " epochs each.")
    mu_start = 10
    mu_end = 1
    mu_decrement = (mu_start - mu_end) / MAX_GENS
    MU = 10 / TABLE_SIZE
    while i < MAX_GENS:
        print(f'Generation {i+1}/{MAX_GENS}') if verbose else None
        population = run_experiment(population)
        fitness_over_gen.append(find_fittest(population))
        new_population = []
        # Step 2: Determine fitness for every solution
        pop_fitness = calc_population_fitness(population)
        pop_with_fitness = list(zip(population, pop_fitness))
        for _ in range(int(POP_SIZE / 2)):
            # Step 3: Select parents for new generation
            parents = get_parents_with_fitness(pop_with_fitness)
            # Step 4a: Introduce variation via crossover
            new_population += crossover(parents[0], parents[1]) if CROSSOVER else parents
        assert(len(new_population) == POP_SIZE)
        # Step 4b: Introduce variation via mutation
        if MU > 0:
            population = [mutate(individual) for individual in new_population]
        else:
            population = new_population.copy()
        i += 1
        MU = (mu_start - i*mu_decrement) / TABLE_SIZE
    population = run_experiment(population)
    fitness_over_gen.append(find_fittest(population))
    return fitness_over_gen

def plot_fitness_over_generations(fitnesses):
    generations = range(1, len(fitnesses) + 1)
    plt.plot(generations, fitnesses)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness Over Generations')
    plt.grid(True)
    plt.savefig("results/fitness.png")

def save_agent_to_file(agent, filename_txt, filename_pickle):
    with open(filename_txt, 'w') as file:
        file.write(str(agent)) 
    with open(filename_pickle, 'wb') as file:
        pickle.dump(agent, file) # Pickling in case we want to run experiments on the best agent.

def run_single_algorithm():
    agent_fitness_pairs = evolutionary_algorithm()
    agents, fitnesses = zip(*agent_fitness_pairs)
    print(f'Fittest agent: {fitnesses[-1]}\nDecision tables: {str(agents[-1])}')

    # Save the last agent to a text file
    save_agent_to_file(agents[-1], "results/best_agent_table.txt", "results/best_agent.pkl")

    plot_fitness_over_generations(fitnesses)

def test_crossovers():
    def test_crossover_func(function, fun_name):
        global crossover
        crossover = function
        crossover_result = []
        for i in range(10):
            print(f'Testing iteration {i+1} of 10 with crossover function {fun_name}')
            print(f'Started current test at {time.strftime("%H:%M:%S",time.localtime())}')
            agent_fitness_pairs = evolutionary_algorithm(verbose=True)
            _, fitnesses = zip(*agent_fitness_pairs)
            avg_over_five = np.average(fitnesses[-5:])
            crossover_result.append(avg_over_five)
        return crossover_result
    
    rows_result = test_crossover_func(crossover_rows, 'crossover_rows')
    quad_result = test_crossover_func(crossover_quadrants, 'crossover_quadrants')

    with open('crossover_test_result.txt', 'w+') as f:
        f.write('ROWS TEST RESULT:\n')
        f.write(str(rows_result) + '\n')
        f.write('QUADRANTS TEST RESULT:\n')
        f.write(str(quad_result) + '\n')

def test_different_mu():
    global MU

    mus = []
    fitness_per_mu = []
    for i in np.arange(1, 10, 1):
        MU = i/TABLE_SIZE
        print(f'Testing with MU = {MU}')
        mus.append(i)
        agent_fitness_pairs = evolutionary_algorithm(verbose=False)
        _, fitnesses = zip(*agent_fitness_pairs)
        fitness_per_mu.append(fitnesses)
    
    iterations = len(mus)
    i = 0
    for fitnesses, mu in zip(fitness_per_mu, mus):
        RED = 255*(i/iterations)/255
        BLUE = 255*(1-(i/iterations))/255
        plt.plot(fitnesses, label=f'MU = {mu}/TS', color=(RED,0,BLUE))
        i += 1
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend(loc="lower right", ncol=2, bbox_to_anchor=(1.1,0))
    plt.title('Fitness over generations with multiple mutation values')
    plt.grid(True)
    plt.savefig('results/fitness-different-mu.png')

def main():
    random.seed(SEED)
    # test_different_mu()
    run_single_algorithm()

if __name__ == '__main__':
    main()
