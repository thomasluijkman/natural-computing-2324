import os
import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return abs(x)

def f2(x):
    return x*x

def f3(x):
    return 2*(x*x)

def f4(x):
    return (x*x) + 20

individuals = [2,3,4]
labels = 'x=2', 'x=3', 'x=4'
fitness_functions = [f1,f2,f3,f4]
population_fitness = []

def plot_selection_pressure(population, fitness, function_name, plot, title=True):
    if not os.path.exists('results/ex1'):
        os.makedirs('results/ex1')
    population_fitness = [fitness(pop) for pop in population]
    print(f'Population fitness using fitness function {function_name}:\n{population_fitness}')
    plot.pie(population_fitness, labels=labels, startangle=90)
    if title:
        plot.set_title(f'Fitness function: {function_name}')

def main():
    plt.figure()
    fig, axs = plt.subplots(2,2)
    for i in range(4):
        function_name = f'f{i+1}'
        fitness_function = fitness_functions[i]
        row = int(i/2)
        col = i % 2
        plot_selection_pressure(individuals, fitness_function, function_name, axs[row][col])
    fig.savefig('results/ex1/combined.png')


if __name__ == '__main__':
    main()
