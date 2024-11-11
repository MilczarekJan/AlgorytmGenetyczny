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

    def reproduction(self, population):
        # Obliczanie przystosowania ka�dego osobnika w populacji
        fitness_values = np.array([self.fitness(ind) for ind in population])
    
        # Obliczanie ca�kowitego przystosowania
        total_fitness = np.sum(fitness_values)
    
        # Obliczanie prawdopodobie�stw selekcji dla ka�dego osobnika
        selection_probabilities = fitness_values / total_fitness
    
        # Skumulowane prawdopodobie�stwa do selekcji
        cumulative_probabilities = np.cumsum(selection_probabilities)
    
        # Nowa populacja na podstawie selekcji ruletki
        new_population = []
        for _ in range(len(population)):
            # Wyb�r osobnika na podstawie skumulowanych prawdopodobie�stw
            r = np.random.random()
            selected_individual_index = np.searchsorted(cumulative_probabilities, r)
            new_population.append(population[selected_individual_index])
    
        return np.array(new_population)

    def mutate(self, individual):

        if individual < self.FunctionDomain[0] or individual > self.FunctionDomain[1]:
            raise ValueError("Osobnik jest poza dozwolonym zakresem.")

        # Konwersja liczby na 6-bitow� reprezentacj� binarn�
        if individual < 0:
            bin_repr = format(32 + individual, '06b')  # Kodowanie ujemnych liczb na 6 bitach
        else:
            bin_repr = format(individual, '06b')

        # Mutacja bit�w
        mutated_bits = []
        for bit in bin_repr:
            if random.random() < self.MutationChance:
                mutated_bits.append('0' if bit == '1' else '1')
            else:
                mutated_bits.append(bit)

        # Sk�adanie zmienionych bit�w
        mutated_bin_repr = ''.join(mutated_bits)
        mutated_integer_part = int(mutated_bin_repr, 2)
        if mutated_bin_repr[0] == '1':  # Sprawdzenie bitu znaku
            mutated_integer_part -= 32

        # Zwr�cenie osobnika po mutacji, ograniczone do przedzia�u
        if mutated_integer_part > self.FunctionDomain[1]:
            return self.FunctionDomain[1]
        elif mutated_integer_part < self.FunctionDomain[0]:
            return self.FunctionDomain[0]
        else:
            return mutated_integer_part

    def crossover(self, parent1, parent2):
        if random.random() < self.CrossoverChance:
            # Zamiana liczby na reprezentacj� binarn� (6-bitow� dla przedzia�u od -1 do 31)
            bin_repr1 = format(int(parent1) if parent1 >= 0 else 32 + int(parent1), '06b')
            bin_repr2 = format(int(parent2) if parent2 >= 0 else 32 + int(parent2), '06b')

            # Wyb�r losowego punktu krzy�owania od 1 do 5 (zawsze 6 bit�w, wi�c pe�ny zakres to 1-5)
            crossover_point = random.randint(1, 5)

            # Tworzenie nowych osobnik�w przez zamian� bit�w
            new_bin_repr1 = bin_repr1[:crossover_point] + bin_repr2[crossover_point:]
            new_bin_repr2 = bin_repr2[:crossover_point] + bin_repr1[crossover_point:]

            # Konwersja binarnej reprezentacji na liczby ca�kowite
            new_parent1 = int(new_bin_repr1, 2) - (32 if new_bin_repr1[0] == '1' else 0)
            new_parent2 = int(new_bin_repr2, 2) - (32 if new_bin_repr2[0] == '1' else 0)

            return new_parent1, new_parent2
        else:
            # Je�li krzy�owanie nie zachodzi, zwracamy rodzic�w bez zmian
            return parent1, parent2

    def startgenetic(self):
        # Generacja losowej pocz�tkowej populacji
        population = np.random.randint(self.FunctionDomain[0], self.FunctionDomain[1] + 1, self.StartingPopulation)

        # Statystyki do zbierania wynik�w
        min_fitness_per_gen = []
        avg_fitness_per_gen = []
        max_fitness_per_gen = []

        for generation in range(self.NumberOfGenerations):
            population = self.reproduction(population)
            for i in range(0, len(population), 2):
                if i + 1 < len(population):
                    parent1, parent2 = population[i], population[i + 1]
                    offspring1, offspring2 = self.crossover(parent1, parent2)
                    offspring1 = self.mutate(offspring1)
                    offspring2 = self.mutate(offspring2)
                    population[i], population[i + 1] = offspring1, offspring2
            # Ocena przystosowania ka�dego osobnika
            fitness_values = np.array([self.fitness(ind) for ind in population])
            # Zbieranie statystyk przystosowania
            min_fitness_per_gen.append(np.min(fitness_values))
            avg_fitness_per_gen.append(np.mean(fitness_values))
            max_fitness_per_gen.append(np.max(fitness_values))
        # Rysowanie wykres�w fitness
        self.plot_fitness(min_fitness_per_gen, avg_fitness_per_gen, max_fitness_per_gen)

    def plot_fitness(self, min_fitness, avg_fitness, max_fitness):
        generations = range(self.NumberOfGenerations)

        # Tworzenie uk�adu podzielonych osi (4 wiersze na wykresy)
        fig, axs = plt.subplots(4, 1, figsize=(8, 12))

        # Tworzenie wykresu minimalnego przystosowania
        axs[0].plot(generations, min_fitness, label="Min Fitness", color='blue')
        axs[0].set_xlabel("Generation")
        axs[0].set_ylabel("Min Fitness")
        axs[0].legend()
        axs[0].set_title("Min Fitness over Generations")

        # Tworzenie wykresu �redniego przystosowania
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

        # Dopasowanie wykres�w dla lepszej estetyki
        plt.tight_layout()
        plt.show()







