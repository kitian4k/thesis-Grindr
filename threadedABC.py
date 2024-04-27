import numpy as np
import time
import threading

# Rastrigin function
def rastrigin_function(x):
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))

# Initialize control parameters
SN = 10000  # Number of food sources
MCN = 100000  # Maximum number of cycles
limit = 50  # Maximum number of exploitations for a solution
dimensionality = 2  # Dimensionality of the search space

# Shared variables among threads
food_sources_lock = threading.Lock()
trial_lock = threading.Lock()
cyc_lock = threading.Lock()
start_time_lock = threading.Lock()

food_sources = np.random.uniform(-5.12, 5.12, size=(SN, dimensionality))  # Initial random positions
trial = np.zeros(SN)  # Initialize trial counters
cyc = 1  # Initial cycle
start_time = None  # Start time

# Function for Employed Bees' Phase
def employed_bees_phase():
    global food_sources, trial
    for i in range(SN):
        # Generate a neighbor solution
        x_hat = food_sources[i] + np.random.uniform(-0.5, 0.5, size=(dimensionality,))

        # Update solution if it is better
        if rastrigin_function(x_hat) < rastrigin_function(food_sources[i]):
            with food_sources_lock:
                food_sources[i] = x_hat
                trial[i] = 0
        else:
            with trial_lock:
                trial[i] += 1

# Function for Onlooker Bees' Phase
def onlooker_bees_phase():
    global food_sources, trial
    probabilities = 1 / (1 + np.exp(-trial))  # Use trial as a measure of fitness
    onlooker_indices = np.random.choice(SN, size=SN, p=probabilities / probabilities.sum())

    for i in onlooker_indices:
        # Generate a neighbor solution
        x_hat = food_sources[i] + np.random.uniform(-0.5, 0.5, size=(dimensionality,))

        # Update solution if it is better
        if rastrigin_function(x_hat) < rastrigin_function(food_sources[i]):
            with food_sources_lock:
                food_sources[i] = x_hat
                trial[i] = 0
        else:
            with trial_lock:
                trial[i] += 1

# Function for Scout Bee Phase
def scout_bee_phase():
    global food_sources, trial
    max_trial_index = np.argmax(trial)
    if trial[max_trial_index] > limit:
        with food_sources_lock:
            food_sources[max_trial_index] = np.random.uniform(-5.12, 5.12, size=(dimensionality,))
            trial[max_trial_index] = 0

# Record start time
with start_time_lock:
    start_time = time.time()

# Thread for Employed Bees' Phase
employed_thread = threading.Thread(target=employed_bees_phase)

# Thread for Onlooker Bees' Phase
onlooker_thread = threading.Thread(target=onlooker_bees_phase)

# Thread for Scout Bee Phase
scout_thread = threading.Thread(target=scout_bee_phase)

# Start all threads
employed_thread.start()
onlooker_thread.start()
scout_thread.start()

# Wait for all threads to finish
employed_thread.join()
onlooker_thread.join()
scout_thread.join()

# Record end time
end_time = time.time()

# Find the best solution
best_solution = food_sources[np.argmin([rastrigin_function(x) for x in food_sources])]

print("Best solution:", best_solution)
print("Objective function value at best solution:", rastrigin_function(best_solution))
print("Time taken:", end_time - start_time, "seconds")
