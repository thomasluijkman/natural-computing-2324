from agent import Agent, DecisionTables, LOOKUP_ACE, LOOKUP_PAIR, LOOKUP_REGULAR, TABLE_SIZE
from game import Actions, MIN_BET, MAX_BET
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import multiprocessing as mp
from known_strat import regular_table_known, ace_table_known, pair_table_known

K = 20
SEED = 42
POP_SIZE = 100
SIGMA = 4
MAX_GENS = 250
NR_ROUNDS = 100000
CROSSOVER = True
BET_TABLE_SIZE = 15
MU = 4/BET_TABLE_SIZE
CUR_STRAT = DecisionTables(lookup_table_regular=regular_table_known,lookup_table_ace=ace_table_known, lookup_table_pair=pair_table_known)

########################################
# Functions for evolutionary algorithm #
########################################

# Create population with random agents
def initialise_population(nr_decks=6):
    population = []
    known_strat = DecisionTables(lookup_table_regular=regular_table_known,lookup_table_ace=ace_table_known, lookup_table_pair=pair_table_known)
    for _ in range(POP_SIZE):
        population.append(Agent(NR_ROUNDS, decision_tables=known_strat, nr_decks=nr_decks))
    return population

def play_game(agent):
    agent.playGame()
    return agent

def run_experiment(population):
    with mp.Pool() as pool:
        updated_population = pool.map(play_game, population)
    return updated_population

# Returns a list with the fitness score for each individual
def calc_population_fitness(population):
    pop_fitness = []
    for individual in population:
        pop_fitness.append(individual.getAgentFitnessMoney())
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
        fitness = agent.getAgentFitnessMoney()
        if fitness > highest:
            highest = fitness
            best_agent = agent
    return best_agent, highest
        
def crossover(a, b):
    cross_point = random.randrange(len(a.betting_table.bets))
    child_a_bets = np.concatenate((a.betting_table.bets[:cross_point], b.betting_table.bets[cross_point:]))
    child_b_bets = np.concatenate((b.betting_table.bets[:cross_point], a.betting_table.bets[cross_point:]))
    child_a = Agent(NR_ROUNDS, a.decision_tables, child_a_bets)
    child_b = Agent(NR_ROUNDS, b.decision_tables, child_b_bets)
    return [child_a, child_b]

def mutate(agent):
    for index, bet in enumerate(agent.betting_table.bets):
        if random.random() <= MU:
            new_bet = bet + np.random.normal(loc=0, scale=SIGMA)
            new_bet = max(MIN_BET, new_bet)
            new_bet = min(MAX_BET, new_bet)
            agent.betting_table.updateBetCell(index, new_bet)
    return agent

def evolutionary_algorithm(verbose=True, nr_decks=6):
    global MU
    # Step 1: Population of candidate solutions
    population = initialise_population()
    # Repeat steps 2-4
    i = 0
    # Keep track of fitest agents
    fitness_over_gen = []
    #run for set amount of generations
    print("Running for " + str(MAX_GENS) + " generations with " + str(POP_SIZE) + " agents each with " + str(NR_ROUNDS) + " epochs each.")
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
    
    print(f'Fittest agent: {agents[-1].betting_table.bets}')

    # Save the last agent to a text file
    save_agent_to_file(agents[-1], "results/best_agent_table.txt", "results/best_agent.pkl")

    plot_fitness_over_generations(fitnesses)

def test_different_mu():
    global MU

    mus = []
    fitness_per_mu = []
    for i in np.arange(1, 11, 1):
        MU = i/BET_TABLE_SIZE
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

def test_different_agents():
    # Known strat
    known_fitnesses = []
    agent_fitness_pairs = evolutionary_algorithm(verbose=False)
    agents, fitnesses = zip(*agent_fitness_pairs)
    best_agent = max(agent_fitness_pairs, key=lambda item: item[1])[0]
    print(f'Fittest agent (known strat): {best_agent.betting_table.bets}')
    known_fitnesses.extend(fitnesses)

    with open('results/best_agent_ours.pkl', 'rb') as f:
        our_agent = pickle.load(f)
    global CUR_STRAT
    CUR_STRAT = our_agent.getAgentStrategy()
    print(CUR_STRAT)
    # Our strat
    our_fitnesses = []
    agent_fitness_pairs = evolutionary_algorithm(verbose=False)
    agents, fitnesses = zip(*agent_fitness_pairs)
    best_agent = max(agent_fitness_pairs, key=lambda item: item[1])[0]
    print(f'Fittest agent (our strat): {best_agent.betting_table.bets}')
    our_fitnesses.extend(fitnesses)
    
    # Plotting
    plt.plot(known_fitnesses, label='Known Strategy')
    plt.plot(our_fitnesses, label='Our Strategy')
    
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend(loc="lower right", ncol=2, bbox_to_anchor=(1.1,0))
    plt.title('Fitness over generations with known and unknown strategies')
    plt.grid(True)
    plt.savefig('results/fitness-different-strat.png')

def test_different_deck_count():
    with open('results/best_agent_mu5.pkl', 'rb') as f:
        our_agent = pickle.load(f)
    global CUR_STRAT
    CUR_STRAT = our_agent.getAgentStrategy()
    decks = []
    fitness_per_deck = []
    for i in np.arange(2, 9, 2):
        print(f'Testing with deck size = {i}')
        decks.append(i)
        agent_fitness_pairs = evolutionary_algorithm(verbose=False,nr_decks=i)
        _, fitnesses = zip(*agent_fitness_pairs)
        fitness_per_deck.append(fitnesses)
    
    iterations = len(decks)
    i = 0
    for fitnesses, deck in zip(fitness_per_deck, decks):
        RED = 255*(i/iterations)/255
        BLUE = 255*(1-(i/iterations))/255
        plt.plot(fitnesses, label=f'#Decks = {deck}', color=(RED,0,BLUE))
        i += 1
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend(loc="lower right", ncol=2, bbox_to_anchor=(1.1,0))
    plt.title('Fitness over generations with multiple deck counts')
    plt.grid(True)
    plt.savefig('results/fitness-different-deck-counts.png')

def main():
    random.seed(SEED)
    np.random.seed(SEED)
    # test_different_mu()
    # run_single_algorithm()
    test_different_agents()
    # test_different_deck_count()
    # with open('results/best_agent_ours.pkl', 'rb') as f:
    #     our_agent = pickle.load(f)
    # global CUR_STRAT
    # print(CUR_STRAT)
    # CUR_STRAT = our_agent.getAgentStrategy()
    # print(CUR_STRAT)

if __name__ == '__main__':
    main()
