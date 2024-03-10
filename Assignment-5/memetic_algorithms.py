import random
import math
import os
import numpy as np
import matplotlib.pyplot as plt

SEED = 42

# ================= Memetic algorithm =================
# Function to calculate the distance between two cities
def calculate_distance(city1, city2):
    return math.dist(city1, city2) #math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# Function to calculate the distance matrix
def calculate_distance_matrix(cities):
    num_cities = len(cities)
    distances = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = calculate_distance(cities[i][1], cities[j][1])
            distances[i][j] = distance
            distances[j][i] = distance
    return distances

# Function to load cities from a file
def load_cities_from_file(filename):
    cities = []
    with open(filename, "r") as file:
        index = 0
        for line in file:
            x, y = map(float, line.strip().split())
            cities.append((index,[x, y]))
            index += 1
    return cities

# Function to calculate the total distance of a tour
def total_distance(tour, distances):
    total = 0
    for i in range(1, len(tour)):
        total += distances[tour[i-1][0]][tour[i][0]]
    return total

# Function for 2-opt local search
def two_opt(tour, distances, max_generation):
    distance = total_distance(tour, distances)
    fitness_scores = []
    improved = True
    gen = 0
    while improved and gen < 1500:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue  # No improvement, skip iteration
                new_tour = tour[:]
                new_tour[i:j] = tour[j-1:i-1:-1]  # Reverse segment
                if total_distance(new_tour, distances) < total_distance(tour, distances):
                    tour = new_tour
                    improved = True
        distance = total_distance(tour, distances)
        fitness_scores.append(1/distance)
        gen += 1
        print(improved)
    print(f"finished two opt after {gen} gernations")
    return tour, distance, fitness_scores

# ================= Evolutionary algorithm =================
def fitness(individual, distances):
    tour_distance = total_distance(individual, distances)
    return 1 / tour_distance

def initialise_population(tour, population_size):
    population = []
    for _ in range(population_size):
        city_list = tour.copy()
        random.shuffle(city_list)
        population.append(city_list)
    return population

def find_fittest(population, distances):
    max_fitness = 0
    index = 0
    for i in range(len(population)):
        this_fitness = fitness(population[i], distances)
        if this_fitness > max_fitness:
            max_fitness = this_fitness
            index = i
    return max_fitness, index

def calc_population_fitness(population, distances):
    pop_fitness = []
    for individual in population:
        pop_fitness.append(fitness(individual, distances))
    return pop_fitness

def get_parents_with_fitness(pop_with_fitness, tournament_size):
    sample = random.choices(pop_with_fitness, k=tournament_size)
    parent0 = max(sample, key=lambda item: item[1])[0]
    sample = random.choices(pop_with_fitness, k=tournament_size)
    parent1 = max(sample, key=lambda item: item[1])[0]
    return (parent0, parent1)

def mutate(individual, mu):
    mutated = []
    if random.random() <= mu:
        mutation_loc1 = 0
        mutation_loc2 = 0
        while True:
            rand1 = random.randrange(1, len(individual))
            rand2 = random.randrange(1, len(individual))
            if rand1 != rand2:
                mutation_loc1 = rand1
                mutation_loc2 = rand2
                break
        mutated = individual.copy()
        mutated[mutation_loc1] = individual[mutation_loc2]
        mutated[mutation_loc2] = individual[mutation_loc1]
    else:
        mutated = individual
    return mutated

def crossover(parent1, parent2):
    assert(len(parent1) == len(parent2))
    cut_points = []
    while len(cut_points) == 0:
        rand1 = random.randrange(1, len(parent1))
        rand2 = random.randrange(1, len(parent1))
        if rand1 != rand2:
            if rand1 < rand2:
                cut_points += [rand1, rand2]
            else: 
                cut_points += [rand2, rand1]
    parent1_keep = parent1[cut_points[0]:cut_points[1]]
    parent2_keep = parent2[cut_points[0]:cut_points[1]]
    parent1_complements = [e for e in parent1 if e not in parent2_keep]
    parent2_complements = [e for e in parent2 if e not in parent1_keep]
    child1 = parent2_complements[-(cut_points[0]):] + parent1_keep + parent2_complements[:(len(parent1) - cut_points[1])]
    child2 = parent1_complements[-(cut_points[0]):] + parent2_keep + parent1_complements[:(len(parent1) - cut_points[1])]
    return child1, child2

def tsp_ea(tour, distances, generations, population_size, tournament_size, mu):
    # Step 1: Population of candidate solutions
    population = initialise_population(tour, population_size)
    # Repeat steps 2-4
    i = 0
    while i < generations:
        new_population = []
        # Step 2: Determine fitness for every solution
        pop_fitness = calc_population_fitness(population, distances)
        pop_with_fitness = list(zip(population, pop_fitness))
        for _ in range(int(population_size / 2)):
            # Step 3: Select parents for new generation
            parents = get_parents_with_fitness(pop_with_fitness, tournament_size)
            # Step 4a: Introduce variation via crossover
            new_population += crossover(parents[0], parents[1])
        assert(len(new_population) == population_size)
        if mu > 0:
            population = [mutate(individual, mu) for individual in new_population]
        else:
            population = new_population.copy()
        i += 1
    max_fitness, index = find_fittest(population, distances)
    best_tour = population[index]
    best_distance = total_distance(best_tour, distances)
    print(f"finished evolutionary algorithm after {generations} generations")
    return best_tour, best_distance, max_fitness 

# Code was adapted from: https://stackoverflow.com/questions/47719924/reading-in-tsp-file-python
def load_tsp_file(filename):
    cities = []
    with open(filename, 'r') as f:
        _ = f.readline() # NAME
        _ = f.readline() # TYPE
        _ = f.readline() # COMMENT
        dimension = f.readline().strip().split(":")[1] # DIMENSION
        line = ""
        while line != "DISPLAY_DATA_SECTION":
            line = f.readline().strip()

        # Read node list
        for _ in range(int(dimension)):
            index, x, y = f.readline().strip().split()
            cities.append((int(index)-1, [float(x), float(y)]))

    assert(len(cities) != 0)
    return cities

# Example usage:
if __name__ == "__main__":
    # Load cities from file
    random.seed(SEED)
    
    filename = "file-tsp.txt"
    print(f"Load data from {filename} and solve TSP problem.")
    cities = load_cities_from_file(filename)


    # Calculate distance matrix
    distances = calculate_distance_matrix(cities)
    
    # Set parameters
    num_generations = 1500
    population_size = 50
    tournament_size = 5
    mu = 0.01

    # Call the memetic algorithm function
    best_solution, best_distance, fitness_scores = two_opt(cities, distances, num_generations)

    # Call evolutionary algorithm function
    best_solution_ea, best_distance_ea, fitness_score_ea = tsp_ea(cities, distances, num_generations, population_size, tournament_size, mu)
    
    print(fitness_scores)
    print("Best solution:", [i[0] for i in best_solution])
    print("Best distance:", best_distance)

    
    print("=====================================================================")

    print(fitness_score_ea)
    print("Best solution:", [i[0] for i in best_solution_ea])
    print("Best distance:", best_distance_ea)
    
    
    print("=====================================================================")

    filename_tsp = "dantzig42.tsp"
    print(f"Load data from {filename_tsp} and solve TSP problem.")
    cities_tsp = load_tsp_file(filename_tsp)

    population_size = 42

    # Calculate distance matrix
    distances = calculate_distance_matrix(cities_tsp)

    # Call the memetic algorithm function
    best_solution_tsp, best_distance_tsp, fitness_scores_tsp = two_opt(cities_tsp, distances, num_generations)

    # Call evolutionary algorithm function
    best_solution_ea_tsp, best_distance_ea_tsp, fitness_score_ea_tsp = tsp_ea(cities_tsp, distances, num_generations, population_size, tournament_size, mu)
    
    print(fitness_scores_tsp)
    print(f"Best solution for {filename_tsp}:", [i[0] for i in best_solution_tsp])
    print(f"Best distance for {filename_tsp}:", best_distance_tsp)

    
    print("=====================================================================")

    print(fitness_score_ea_tsp)
    print("Best solution:", [i[0] for i in best_solution_ea_tsp])
    print("Best distance:", best_distance_ea_tsp)


    
