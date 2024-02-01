import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import random

class GeneticAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm")

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Number of Generations:").grid(row=0, column=0, padx=10, pady=5)
        self.num_generations_entry = ttk.Entry(self.root)
        self.num_generations_entry.grid(row=0, column=1, padx=10, pady=5)
        self.num_generations_entry.insert(0, "200")

        ttk.Label(self.root, text="K Value:").grid(row=2, column=0, padx=10, pady=5)
        self.k_value_entry = ttk.Entry(self.root)
        self.k_value_entry.grid(row=2, column=1, padx=10, pady=5)
        self.k_value_entry.insert(0, "10")

        ttk.Label(self.root, text="Crossover Type:").grid(row=3, column=0, padx=10, pady=5)
        self.crossover_type_var = tk.StringVar()
        self.crossover_type_var.set("one_point")
        crossover_type_options = ["one_point", "two_point", "uniform"]
        self.crossover_type_menu = ttk.Combobox(self.root, textvariable=self.crossover_type_var, values=crossover_type_options)
        self.crossover_type_menu.grid(row=3, column=1, padx=10, pady=5)

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

        sorted_indices = np.argsort(fitness_vals)[::-1] 
        selected_indices = sorted_indices[:num_parents]

        for i, idx in enumerate(selected_indices):
            parents[i, :] = population[idx, :]

        return parents

    def crossover(self, parents, offspring_size, crossover_type):
        offspring = np.empty(offspring_size)

        for k in range(0, offspring_size[0], 2):
            if k + 1 >= offspring_size[0]:
                continue

            parent1_idx = np.random.randint(0, parents.shape[0])
            parent2_idx = np.random.randint(0, parents.shape[0])

            if crossover_type == 'one_point':
                crossover_point = np.random.randint(1, offspring_size[1])
                offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
                offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
                offspring[k + 1, 0:crossover_point] = parents[parent2_idx, 0:crossover_point]
                offspring[k + 1, crossover_point:] = parents[parent1_idx, crossover_point:]

            elif crossover_type == 'two_point':
                crossover_point1 = np.random.randint(1, offspring_size[1] - 1)
                crossover_point2 = np.random.randint(crossover_point1 + 1, offspring_size[1])
                offspring[k, 0:crossover_point1] = parents[parent1_idx, 0:crossover_point1]
                offspring[k, crossover_point1:crossover_point2] = parents[parent2_idx, crossover_point1:crossover_point2]
                offspring[k, crossover_point2:] = parents[parent1_idx, crossover_point2:]
                offspring[k + 1, 0:crossover_point1] = parents[parent2_idx, 0:crossover_point1]
                offspring[k + 1, crossover_point1:crossover_point2] = parents[parent1_idx, crossover_point1:crossover_point2]
                offspring[k + 1, crossover_point2:] = parents[parent2_idx, crossover_point2:]

            elif crossover_type == 'uniform':
                mask = np.random.randint(0, 2, size=offspring_size[1]).astype(np.bool_)
                offspring[k, mask] = parents[parent1_idx, mask]
                offspring[k, ~mask] = parents[parent2_idx, ~mask]
                offspring[k + 1, mask] = parents[parent2_idx, mask]
                offspring[k + 1, ~mask] = parents[parent1_idx, ~mask]

        return offspring

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
            num_parents_mating = 5
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

            for generation in range(num_generations):
                fitness_vals = np.array([self.fitness(individual, k_value) for individual in population])
                mating_pool_idx, _, _ = self.parent_selection(len(population))
                parents = self.select_parents_based_on_fitness(population, fitness_vals, num_parents_mating)
                offspring_size = (len(population) - len(parents), population.shape[1])
                offspring_crossover = self.crossover(parents, offspring_size, crossover_type)
                offspring_mutation = self.mutation(offspring_crossover, parents)
                population[:len(parents)] = parents
                population[len(parents):] = offspring_mutation

                # print(f"Algorithm completed successfully!\nBest fitness: {best_solution_fitness}\nBest solution: {best_solution}")

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
