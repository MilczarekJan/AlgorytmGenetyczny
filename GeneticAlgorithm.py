import array
import matplotlib.pyplot as plt
import numpy as np
import random

class GeneticAlgorithm:
    def __init__(self, mutation_chance, crossover_chance, number_of_generations, population, function) -> None:
        self.MutationChance = mutation_chance
        self.CrossoverChance = crossover_chance
        self.NumberOfGenerations = number_of_generations
        self.StartingPopulation = population
        self.FitnessFunction = function
        self.FunctionDomain = (-1, 31)

    def fitness(self, x):
        if self.FitnessFunction == "Examined function":
            fitness_function = -0.2 * x**2 + 6*x + 7
            return fitness_function
        elif self.FitnessFunction == "Linear scaling":
            fitness_function = 5 * (-0.2 * x**2 + 6*x + 7)
            return fitness_function
        elif self.FitnessFunction == "Quadratic scaling":
            fitness_function = (-0.2 * x**2 + 6*x + 7)**2
            return fitness_function
        else:
            fitness_function = -0.2 * x**2 + 6*x + 7
            return fitness_function

    def reproduction(self, population, fitness_values):
        total_fitness = np.sum(fitness_values)
        selection_probabilities = fitness_values / total_fitness
        cumulative_probabilities = np.cumsum(selection_probabilities)
        new_population = []
        for _ in range(len(population)):
            r = np.random.random()
            selected_individual_index = np.searchsorted(cumulative_probabilities, r)
            new_population.append(population[selected_individual_index])
    
        return np.array(new_population)

    def mutation(self, population):

        returned_population = []

        for individual in population:
            if individual < 0:
                bin_repr = format(32 + individual, '06b')
            else:
                bin_repr = format(individual, '06b')

            mutated_bits = []
            for bit in bin_repr:
                if random.random() < self.MutationChance:
                    mutated_bits.append('0' if bit == '1' else '1')
                else:
                    mutated_bits.append(bit)

            mutated_bin_repr = ''.join(mutated_bits)
            mutated_integer_part = int(mutated_bin_repr, 2)
            if mutated_bin_repr[0] == '1':
                mutated_integer_part -= 32

            if mutated_integer_part > self.FunctionDomain[1]:
                returned_population.append(self.FunctionDomain[1])
            elif mutated_integer_part < self.FunctionDomain[0]:
                returned_population.append(self.FunctionDomain[0])
            else:
                returned_population.append(mutated_integer_part)
        return returned_population

    def crossover(self, population):
        mating_population = []
        stagnant_population = []
        mating_population_to_return = []
        mating_size = int(self.CrossoverChance*len(population))

        mating_population = list(population[:mating_size])
        stagnant_population = list(population[mating_size:])

        for parent1 in mating_population:
            
            mating_population.remove(parent1)
            if mating_population:
                parent2 = random.choice(mating_population)
                mating_population.remove(parent2)

                bin_repr1 = format(int(parent1) if parent1 >= 0 else 32 + int(parent1), '06b')
                bin_repr2 = format(int(parent2) if parent2 >= 0 else 32 + int(parent2), '06b')

                crossover_point = random.randint(1, 5)

                new_bin_repr1 = bin_repr1[:crossover_point] + bin_repr2[crossover_point:]
                new_bin_repr2 = bin_repr2[:crossover_point] + bin_repr1[crossover_point:]

                new_parent1 = int(new_bin_repr1, 2) - (32 if new_bin_repr1[0] == '1' else 0)
                new_parent2 = int(new_bin_repr2, 2) - (32 if new_bin_repr2[0] == '1' else 0)

                mating_population_to_return.append(new_parent1)
                mating_population_to_return.append(new_parent2)

        mating_population_to_return.extend(stagnant_population)
        return mating_population_to_return

    def startgenetic(self):
        population = np.random.randint(self.FunctionDomain[0], self.FunctionDomain[1] + 1, self.StartingPopulation)

        min_fitness_per_gen = []
        avg_fitness_per_gen = []
        max_fitness_per_gen = []

        for generation in range(self.NumberOfGenerations):
            np.random.shuffle(population) #zachowanie losowoœci
            fitness_values = np.array([self.fitness(ind) for ind in population]) # Ocena przystosowania ka¿dego osobnika
            population = self.reproduction(population, fitness_values) #reprodukcja
            population = self.crossover(population) #krzy¿owanie
            population = self.mutation(population) #mutacja
            # Zbieranie statystyk przystosowania
            min_fitness_per_gen.append(np.min(fitness_values))
            avg_fitness_per_gen.append(np.mean(fitness_values))
            max_fitness_per_gen.append(np.max(fitness_values))
        # Rysowanie wykresów fitness
        self.plot_fitness(min_fitness_per_gen, avg_fitness_per_gen, max_fitness_per_gen)

    def plot_fitness(self, min_fitness, avg_fitness, max_fitness):
        generations = range(self.NumberOfGenerations)
        fig, axs = plt.subplots(4, 1, figsize=(8, 12))

        axs[0].plot(generations, min_fitness, label="Min Fitness", color='blue')
        axs[0].set_xlabel("Generation")
        axs[0].set_ylabel("Min Fitness")
        axs[0].legend()
        axs[0].set_title("Min Fitness over Generations")

        axs[1].plot(generations, avg_fitness, label="Avg Fitness", color='green')
        axs[1].set_xlabel("Generation")
        axs[1].set_ylabel("Avg Fitness")
        axs[1].legend()
        axs[1].set_title("Avg Fitness over Generations")

        axs[2].plot(generations, max_fitness, label="Max Fitness", color='red')
        axs[2].set_xlabel("Generation")
        axs[2].set_ylabel("Max Fitness")
        axs[2].legend()
        axs[2].set_title("Max Fitness over Generations")

        x = np.linspace(self.FunctionDomain[0], self.FunctionDomain[1], 100)
        y = -0.2 * x**2 + 6*x + 7
        axs[3].plot(x, y, label="Examined Function", color='purple')
        axs[3].set_xlabel("x")
        axs[3].set_ylabel("f(x)")
        axs[3].legend()
        axs[3].set_title("Examined Function")

        plt.tight_layout()
        plt.show()







