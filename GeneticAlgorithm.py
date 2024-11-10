import numpy as np
import matplotlib.pyplot as plt
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

    def mutate(self, individual):
        integer_part = int(individual)
        fractional_part = individual - integer_part

        if integer_part < 0:
            bin_repr = format(32 + integer_part, '05b')  # Kodowanie ujemnych na 5 bitach
        else:
            bin_repr = format(integer_part, '05b')

        mutated_bits = []
        for bit in bin_repr:
            if random.random() < self.MutationChance:
                mutated_bits.append('0' if bit == '1' else '1')
            else:
                mutated_bits.append(bit)

        mutated_bin_repr = ''.join(mutated_bits)
        mutated_integer_part = int(mutated_bin_repr, 2) - (32 if mutated_bin_repr[0] == '1' else 0)
        mutated_individual = mutated_integer_part + fractional_part
        if mutated_individual > self.FunctionDomain[1]:
            return self.FunctionDomain[1]
        elif mutated_individual < self.FunctionDomain[0]:
            return self.FunctionDomain[0]
        else:
            return mutated_individual

    def crossover(self, parent1, parent2):
        if random.random() < self.CrossoverChance:
            # Rozdziel czêœæ ca³kowit¹ i u³amkow¹
            int_part1, frac_part1 = divmod(int(parent1), 1)
            int_part2, frac_part2 = divmod(int(parent2), 1)

            # Zamieñ na binarne reprezentacje
            bin_repr1 = format(int(int_part1), '05b')  # Pierwszy rodzic
            bin_repr2 = format(int(int_part2), '05b')  # Drugi rodzic

            # WeŸ 2 najbardziej znacz¹ce bity z pierwszego rodzica i 3 najmniej znacz¹ce bity z drugiego rodzica
            new_bin_repr = bin_repr1[:2] + bin_repr2[-3:]

            # Zamieñ z powrotem na liczbê ca³kowit¹
            new_int_part = int(new_bin_repr, 2)

            # Z³¹cz z czêœci¹ u³amkow¹ pierwszego rodzica
            new_individual = new_int_part + frac_part1
            return new_individual
        else:
            # Jeœli nie zachodzi krzy¿owanie, zwróæ losowego rodzica
            return parent1 if random.random() < 0.5 else parent2


    def startgenetic(self):
        # Generacja losowej pocz¹tkowej populacji
        population = np.random.uniform(self.FunctionDomain[0], self.FunctionDomain[1], self.StartingPopulation)

        # Statystyki do zbierania wyników
        min_fitness_per_gen = []
        avg_fitness_per_gen = []
        max_fitness_per_gen = []

        for generation in range(self.NumberOfGenerations):
            # Ocena przystosowania ka¿dego osobnika
            fitness_values = np.array([self.fitness(ind) for ind in population])

            # Zbieranie statystyk przystosowania
            min_fitness_per_gen.append(np.min(fitness_values))
            avg_fitness_per_gen.append(np.mean(fitness_values))
            max_fitness_per_gen.append(np.max(fitness_values))

            # Selekcja osobników: wybieramy najlepszych na podstawie przystosowania
            sorted_indices = np.argsort(fitness_values)[::-1]  # Sortujemy od najlepszego do najgorszego
            selected_individuals = population[sorted_indices[:self.StartingPopulation//2]]  # Najlepsza po³owa

            # Tworzenie nowej populacji przez krzy¿owanie
            new_population = []
            while len(new_population) < self.StartingPopulation:
                parent1, parent2 = random.choices(selected_individuals, k=2)
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                new_population.append(offspring)
            population = np.array(new_population)

        # Rysowanie wykresów fitness
        self.plot_fitness(min_fitness_per_gen, avg_fitness_per_gen, max_fitness_per_gen)
        
        # Rysowanie funkcji badanej
        self.plot_examined_function()

    def plot_fitness(self, min_fitness, avg_fitness, max_fitness):
        generations = range(self.NumberOfGenerations)

        # Tworzenie uk³adu podzielonych osi (4 wiersze na wykresy)
        fig, axs = plt.subplots(4, 1, figsize=(8, 12))

        # Tworzenie wykresu minimalnego przystosowania
        axs[0].plot(generations, min_fitness, label="Min Fitness", color='blue')
        axs[0].set_xlabel("Generation")
        axs[0].set_ylabel("Min Fitness")
        axs[0].legend()
        axs[0].set_title("Min Fitness over Generations")

        # Tworzenie wykresu œredniego przystosowania
        axs[1].plot(generations, avg_fitness, label="Avg Fitness", color='green')
        axs[1].set_xlabel("Generation")
        axs[1].set_ylabel("Avg Fitness")
        axs[1].legend()
        axs[1].set_title("Avg Fitness over Generations")

        # Tworzenie wykresu maksymalnego przystosowania
        axs[2].plot(generations, max_fitness, label="Max Fitness", color='red')
        axs[2].set_xlabel("Generation")
        axs[2].set_ylabel("Max Fitness")
        axs[2].legend()
        axs[2].set_title("Max Fitness over Generations")

        # Rysowanie funkcji badanej na czwartej osi
        x = np.linspace(self.FunctionDomain[0], self.FunctionDomain[1], 100)
        y = -0.2 * x**2 + 6*x + 7
        axs[3].plot(x, y, label="Examined Function", color='purple')
        axs[3].set_xlabel("x")
        axs[3].set_ylabel("f(x)")
        axs[3].legend()
        axs[3].set_title("Examined Function")

        # Dopasowanie wykresów dla lepszej estetyki
        plt.tight_layout()
        plt.show()







