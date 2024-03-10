import pickle
import matplotlib.pyplot as plt
import numpy as np

with open('num_runs_ea42.data', 'rb') as f:
        data = pickle.load(f)

# # Plotting seprate
# plt.figure(figsize=(10, 6))  # Adjust figure size if needed
# for i, run_data in enumerate(data):
#     generation = range(1, len(run_data) + 1)  # Generating x-axis data (generations)
#     plt.plot(generation, run_data, label=f"Run {i+1}")

# plt.title(f'Fitness Over {len(data[0])} Generations')
# plt.xlabel('Generation')
# plt.ylabel('Fitness')
# plt.legend()
# plt.grid(True)
# plt.savefig("./results/ex5/ea.png")

# Calculate average fitness across all runs for each generation
average_fitness = np.mean(data, axis=0)

# Plotting
plt.figure(figsize=(12, 6))  # Adjust figure size if needed

# Plot individual runs
for i, run_data in enumerate(data):
    generation = range(1, len(run_data) + 1)  # Generating x-axis data (generations)
    plt.plot(generation, run_data, label=f"Run {i+1}")

# Plot average fitness
generation = range(1, len(average_fitness) + 1)  # Generating x-axis data (generations)
plt.plot(generation, average_fitness, color='black', linestyle='--', label='Average')

plt.title(f'Fitness Over {len(data[0])} Generations (Simple EA)')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)
plt.savefig("./results/ex5/ea42.png")




