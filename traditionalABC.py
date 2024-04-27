import numpy as np
import time

# Rastrigin function
def rastrigin_function(x):
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))

# Initialize control parameters
SN = 10000  # Number of food sources
MCN = 100000  # Maximum number of cycles
limit = 50  # Maximum number of exploitations for a solution
dimensionality = 2  # Dimensionality of the search space

# Shared variables
food_sources = np.random.uniform(-5.12, 5.12, size=(SN, dimensionality))  # Initial random positions
trial = np.zeros(SN)  # Initialize trial counters

# Main ABC loop
start_time = time.time()

for cyc in range(1, MCN + 1):
    # Employed Bees' Phase
    for i in range(SN):
        x_hat = food_sources[i] + np.random.uniform(-0.5, 0.5, size=(dimensionality,))
        if rastrigin_function(x_hat) < rastrigin_function(food_sources[i]):
            food_sources[i] = x_hat
            trial[i] = 0
        else:
            trial[i] += 1

    # Onlooker Bees' Phase
    probabilities = 1 / (1 + np.exp(-trial))
    onlooker_indices = np.random.choice(SN, size=SN, p=probabilities / probabilities.sum())
    
    for i in onlooker_indices:
        x_hat = food_sources[i] + np.random.uniform(-0.5, 0.5, size=(dimensionality,))
        if rastrigin_function(x_hat) < rastrigin_function(food_sources[i]):
            food_sources[i] = x_hat
            trial[i] = 0
        else:
            trial[i] += 1

    # Scout Bee Phase
    max_trial_index = np.argmax(trial)
    if trial[max_trial_index] > limit:
        food_sources[max_trial_index] = np.random.uniform(-5.12, 5.12, size=(dimensionality,))
        trial[max_trial_index] = 0

end_time = time.time()

# Find the best solution
best_solution = food_sources[np.argmin([rastrigin_function(x) for x in food_sources])]

print("Best solution:", best_solution)
print("Objective function value at best solution:", rastrigin_function(best_solution))
print("Time taken:", end_time - start_time, "seconds")
