from agent import Agent, DecisionTables
from game import Actions
import random
import sys
import numpy as np

K = 2
SEED = 42
POP_SIZE = 200
TABLE_SIZE = (16*10)+(8*10)+(10*10)
MU = 1 / TABLE_SIZE
RUNS_PER_AGENT = 100
MAX_GENS = 100
NR_ROUNDS = 10

# Evolutionary algorithms
def initialise_population():
    population = []
    for _ in range(POP_SIZE):
        population.append(Agent())
    return population

def evolutionary_algorithm():
    # Step 1: Population of candidate solutions
    population = initialise_population()
    distances = []
    # Repeat steps 2-4
    i = 0
    while i < MAX_GENS:
        print(f'Generation {i}/{MAX_GENS}')
        run_experiment(population, NR_ROUNDS)
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
        if MU > 0:
            population = [mutate(individual) for individual in new_population]
        else:
            population = new_population.copy()
        i += 1
    return find_fittest(population) # negative return means max generations were reached without target string being found

def run_experiment(population, nr_rounds):
    i = 1
    for agent in population:
        print(f'{i}')
        i += 1
        agent.playGame(nr_rounds)

def calc_population_fitness(population):
    pop_fitness = []
    for individual in population:
        pop_fitness.append(individual.getAgentFitness())
    return pop_fitness

def get_parents_with_fitness(pop_with_fitness):
    sample = random.choices(pop_with_fitness, k=K)
    parent0 = max(sample, key=lambda item: item[1])[0]
    sample = random.choices(pop_with_fitness, k=K)
    parent1 = max(sample, key=lambda item: item[1])[0]
    return (parent0, parent1)

def find_fittest(population):
    highest = -sys.maxint - 1
    for i, agent in enumerate(population):
        if agent.getAgentFitness() > highest:
            highest = agent.getAgentFitness()
    return i
        
def crossover(a, b):
    a_tables = a.decision_tables.getAllTables()
    b_tables = b.decision_tables.getAllTables()

    assert(len(a_tables) == len(b_tables))

    child1_tables = []
    child2_tables = []

    parents_tables = list(zip(a_tables, b_tables))
    for i, (table_a, table_b) in enumerate(parents_tables):
        # Get the dimensions of the arrays
        rows, cols = table_a.shape

        # Randomly select the row index for crossover
        crossover_point = np.random.randint(1, rows)

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

    assert(len(a_tables) == len(child1_tables))
    assert(len(b_tables) == len(child2_tables))
    assert(len(child1_tables) == 3)
    assert(len(child2_tables) == 3)

    child1 = Agent(decision_tables=DecisionTables(child1_tables[0], child1_tables[1], child1_tables[2]))
    child2 = Agent(decision_tables=DecisionTables(child2_tables[0], child2_tables[1], child2_tables[2]))

    return [child1, child2]

def mutate(agent):
    tables = agent.decision_tables.getAllTables()
    for table_num, table in enumerate(tables):
        for x_pos, x in enumerate(table):
            for y_pos, y in enumerate(x):
                if random.random() <= MU:
                    if table_num == 2: # If pairs table
                        new_action = random.choice(list(Actions))
                    else:
                        new_action = random.choice([Actions.HT,Actions.ST, Actions.DH, Actions.DS])
                    agent.decision_tables.updateTableCell(table_num, (x_pos,y_pos), new_action)
    return agent

def main():
    random.seed(SEED)
    print(evolutionary_algorithm())



if __name__ == '__main__':
    main()

