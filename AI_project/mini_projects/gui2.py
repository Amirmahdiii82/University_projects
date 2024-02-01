import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import random


class GeneticAlgorithmGUI:
    def __init__(self, num_generations, num_parents_mating, k_value, crossover_type, population_size=(10, 10)):
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.k_value = k_value
        self.crossover_type = crossover_type
        self.population_size = population_size
        self.population = self.initial_population()

    def create_widgets(self):
        # Number of generations
        ttk.Label(self.root, text="Number of Generations:").grid(row=0, column=0, padx=10, pady=5)
        self.num_generations_entry = ttk.Entry(self.root)
        self.num_generations_entry.grid(row=0, column=1, padx=10, pady=5)
        self.num_generations_entry.insert(0, "200")

        # Number of parents mating
        ttk.Label(self.root, text="Number of Parents Mating:").grid(row=1, column=0, padx=10, pady=5)
        self.num_parents_entry = ttk.Entry(self.root)
        self.num_parents_entry.grid(row=1, column=1, padx=10, pady=5)
        self.num_parents_entry.insert(0, "5")

        # K value
        ttk.Label(self.root, text="K Value:").grid(row=2, column=0, padx=10, pady=5)
        self.k_value_entry = ttk.Entry(self.root)
        self.k_value_entry.grid(row=2, column=1, padx=10, pady=5)
        self.k_value_entry.insert(0, "10")

        # Crossover type
        ttk.Label(self.root, text="Crossover Type:").grid(row=3, column=0, padx=10, pady=5)
        self.crossover_type_var = tk.StringVar()
        self.crossover_type_var.set("one_point")
        crossover_type_options = ["one_point", "two_point", "uniform", "pmx"]  # Added "pmx" option
        self.crossover_type_menu = ttk.Combobox(self.root, textvariable=self.crossover_type_var, values=crossover_type_options)
        self.crossover_type_menu.grid(row=3, column=1, padx=10, pady=5)

        # Run button
        ttk.Button(self.root, text="Run Genetic Algorithm", command=self.run_genetic_algorithm).grid(row=4, column=0, columnspan=2, pady=10)

    def fitness(self, chromosome, k):
        unique_elements, counts = np.unique(chromosome, return_counts=True)
        return k - sum(counts - 1)

    def parent_selection(self, population_size):
        mu_rate = 0.5
        cross_rate = 0.3
        mu_pop_size = int(np.ceil(mu_rate * population_size))
        cross_pop_size = int(2 * np.ceil((cross_rate * population_size) / 2))
        child_pop_size = mu_pop_size + cross_pop_size
        mating_pool_index = random.sample(range(0, population_size), int(child_pop_size))
        return mating_pool_index, mu_pop_size, cross_pop_size

    def select_parents_based_on_fitness(self, population, fitness_vals, num_parents):
        parents = np.empty((num_parents, population.shape[1]))

        # Select parents based on fitness values
        sorted_indices = np.argsort(fitness_vals)[::-1]  # Sort in descending order
        selected_indices = sorted_indices[:num_parents]

        for i, idx in enumerate(selected_indices):
            parents[i, :] = population[idx, :]

        return parents


    def crossover(self, parents, offspring_size, crossover_type):
        # Crossover function with fixed 'pmx' crossover logic
        offspring = np.empty(offspring_size)
        # Crossover code logic here for types like 'one_point', 'two_point', and 'uniform'
        # PMX crossover logic:
        if crossover_type == 'pmx':
            # PMX crossover logic here
            for k in range(0, offspring_size[0], 2):
                # Choose two parents for PMX crossover
                parent1_idx = k % parents.shape[0]
                parent2_idx = (k + 1) % parents.shape[0]
                child1, child2 = self.pmx_crossover(parents[parent1_idx], parents[parent2_idx])
                offspring[k] = child1
                if k + 1 < offspring_size[0]:
                    offspring[k + 1] = child2
        return offspring

    def pmx_crossover(self, parent1, parent2):
        # PMX crossover full logic implementation
        size = len(parent1)
        p1, p2 = [0]*size, [0]*size

        # Initialize the position of each indices in the individuals
        for i in range(size):
            p1[parent1[i]] = i
            p2[parent2[i]] = i
        
        # Choose crossover points
        cxpoint1 = random.randint(0, size)
        cxpoint2 = random.randint(0, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else: # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        # Apply crossover between cx points
        for i in range(cxpoint1, cxpoint2):
            # Keep track of the swapped values
            temp1 = parent1[i]
            temp2 = parent2[i]
            parent1[i], parent2[i] = temp2, temp1
            p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
            p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
        
        # Map the same crossover in the other offspring
        for i in range(size):
            if i < cxpoint1 or i >= cxpoint2:
                while p1[parent1[i]] != i:
                    parent1[i], parent1[p1[parent1[i]]] = \
                        parent1[p1[parent1[i]]], parent1[i]
                while p2[parent2[i]] != i:
                    parent2[i], parent2[p2[parent2[i]]] = \
                        parent2[p2[parent2[i]]], parent2[i]
        return parent1, parent2

    def mutation(self, offspring_crossover, parents, num_mutations=1):
        unique_values = np.unique(parents)
        for i in range(offspring_crossover.shape[0]):
            mutation_indices = np.random.randint(0, offspring_crossover.shape[1], size=num_mutations)
            for idx in mutation_indices:
                possible_values = np.setdiff1d(unique_values, [offspring_crossover[i, idx]])
                offspring_crossover[i, idx] = np.random.choice(possible_values, size=1)
        return offspring_crossover

    def run_genetic_algorithm(self):
        try:
            num_generations = int(self.num_generations_entry.get())
            num_parents_mating = int(self.num_parents_entry.get())
            k_value = int(self.k_value_entry.get())
            crossover_type = self.crossover_type_var.get()

            # Generate initial population
            population = np.array([
                [5, 5, 15, 15, 2, 2, 7, 7, 17, 17],
                [1, 15, 15, 25, 25, 25, 12, 17, 22, 3],
                [10, 10, 10, 20, 20, 7, 2, 12, 12, 3],
                [1, 10, 15, 15, 2, 2, 7, 7, 12, 22],
                [5, 5, 20, 25, 20, 25, 12, 12, 17, 3],
                [10, 10, 20, 15, 25, 25, 2, 7, 22, 22],
                [5, 5, 15, 20, 20, 7, 7, 7, 12, 22],
                [10, 15, 15, 25, 20, 2, 2, 12, 17, 17],
                [10, 10, 20, 25, 25, 2, 7, 12, 12, 17],
                [5, 15, 20, 20, 2, 2, 2, 22, 22, 17]
            ])

            # Your genetic algorithm main loop
            for generation in range(num_generations):
                fitness_vals = np.array([self.fitness(individual, k_value) for individual in population])
                mating_pool_idx, _, _ = self.parent_selection(len(population))
                parents = self.select_parents_based_on_fitness(population, fitness_vals, num_parents_mating)
                offspring_size = (len(population) - len(parents), population.shape[1])
                offspring_crossover = self.crossover(parents, offspring_size, crossover_type)
                offspring_mutation = self.mutation(offspring_crossover, parents)
                population[:len(parents)] = parents
                population[len(parents):] = offspring_mutation

                print('Fitness values: {0}'.format([self.fitness(individual, k_value) for individual in population]))

            best_fitness_idx = np.argmax(fitness_vals)
            best_solution = population[best_fitness_idx]
            best_solution_fitness = fitness_vals[best_fitness_idx]

            messagebox.showinfo("Genetic Algorithm", f"Algorithm completed successfully!\nBest fitness: {best_solution_fitness}\nBest solution: {best_solution}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
