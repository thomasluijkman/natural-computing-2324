import os
import random
import matplotlib.pyplot as plt

SEED = 42

LENGTH = 100
LENGTH_FL = float(LENGTH)
MU = 1/LENGTH_FL
GENERATIONS = 1500

fitness = sum

def generate_bitstring():
    bitstring = []
    for _ in range(LENGTH):
        if random.random() < 0.5:
            bitstring.append(0)
        else:
            bitstring.append(1)
    return bitstring

def ga_v1(bitstring):
    fitness_gens = []
    old_bits = bitstring.copy()
    for _ in range(GENERATIONS):
        new_bits = old_bits.copy()

        # mutate bits with a probability of MU
        for i in range(LENGTH):
            if random.random() < MU:
                new_bits[i] = 1 - new_bits[i]
        
        # compare bits and pick one with best fitness
        if fitness(new_bits) > fitness(old_bits):
            old_bits = new_bits.copy()
        fitness_gens.append(fitness(old_bits))
    plt.plot(range(GENERATIONS), fitness_gens, color='green')

def ga_v2(bitstring):
    fitness_gens = []
    old_bits = bitstring.copy()
    for _ in range(GENERATIONS):
        new_bits = old_bits.copy()

        # mutate bits with a probability of MU
        for i in range(LENGTH):
            if random.random() < MU:
                new_bits[i] = 1 - new_bits[i]
        
        # compare bits and pick one with best fitness
        old_bits = new_bits.copy()
        fitness_gens.append(fitness(old_bits))
    plt.plot(range(GENERATIONS), fitness_gens, color='red')
        

def main():
    if not os.path.exists('results/ex2'):
        os.makedirs('results/ex2')

    random.seed(SEED)
    plt.figure()
    
    for _ in range(10):
        bitstring = generate_bitstring()
        ga_v1(bitstring)
        ga_v2(bitstring)

    
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.xlim(0,1500)
    plt.grid()
    plt.legend()
    plt.savefig('results/ex2/graph.png')

if __name__ == '__main__':
    main()