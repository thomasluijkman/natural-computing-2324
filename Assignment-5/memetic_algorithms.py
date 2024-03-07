import random
import math
import os
import numpy as np
import matplotlib.pyplot as plt

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
    fitness_score = 0
    improved = True
    gen = 0
    while improved:
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
        fitness_score = 1/distance
    return tour, distance, fitness_score

# ================= Evolutionary algorithm =================
def crossover(parent1, parent2):
    if len(parent1) != len(parent2):
        raise Exception("Parents are different size")
    cut_points = []
    while len(cut_points) == 0:
        rand1 = random.randrange(0, len(parent1))
        rand2 = random.randrange(0, len(parent1))
        if rand1 != rand2:
            if rand1 < rand2:
                cut_points += [rand1, rand2]
            else: 
                cut_points += [rand2, rand1]
    parent1_keep = parent1[cut_points[0]:cut_points[1]]
    parent2_keep = parent2[cut_points[0]:cut_points[1]]
    parent1_complements = [e for e in parent1 if e not in parent2_keep]
    parent2_complements = [e for e in parent2 if e not in parent1_keep]
    child1 = parent2_complements[:cut_points[0]] + parent1_keep + parent2_complements[-(len(parent1)-rand2):]
    child2 = parent1_complements[:cut_points[0]] + parent2_keep + parent1_complements[-(len(parent1)-rand2):]
    return cut_points, child1, child2



# Example usage:
if __name__ == "__main__":
    # Load cities from file
    filename = "file-tsp.txt"
    cities = load_cities_from_file(filename)

    cut_points, chil1, child2 = crossover([3, 5, 7,  2, 1, 6, 4, 8], [2, 5,7, 6, 8, 1,3, 4])
    print(f"Cut points: {str(cut_points)}")
    print(f"Cchild1: {str(chil1)}")
    print(f"Child2: {str(child2)}")
    # Calculate distance matrix
    distances = calculate_distance_matrix(cities)
    
    # Set parameters
    num_generations = 100
    population_size = 50
    tournament_size = 5
    
    # Call the memetic algorithm function
    best_solution, best_distance, fitness_scores = two_opt(cities, distances, num_generations)
    
    print("Best solution:", best_solution)
    print("Best distance:", best_distance)

    if not os.path.exists('results/ex4'):
        os.makedirs('results/ex4')

    plt.figure()
    plt.plot(range(num_generations), fitness_scores, color='red', label='Memetic algorithm')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.xlim(0,num_generations+1)
    plt.grid()
    plt.legend()
    plt.savefig('results/ex4/fitness.png')
