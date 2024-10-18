import numpy as np
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, mutation_chance, crossover_chance, number_of_generations, population, function) -> None:
        self.MutationChance = mutation_chance
        self.CrossoverChance = crossover_chance
        self.NumberOfGenerations = number_of_generations
        self.StartingPopulation = population
        self.FitnessFunction = function
        self.FunctionDomain = (-1, 31)

    def show(self):
        print(self.MutationChance)
        print(self.CrossoverChance)
        print(self.NumberOfGenerations)
        print(self.FitnessFunction)
        print(self.FunctionDomain)

    def startgenetic(self):
        span = abs(int(self.FunctionDomain[1]) - int(self.FunctionDomain[0]))
        x = np.linspace(int(self.FunctionDomain[0]), int(self.FunctionDomain[1]), span)
        examined_function = -0.2 * x**2 + 6*x + 7

        match self.FitnessFunction:
            case "Examined function":
                fitness_function = -0.2 * x**2 + 6*x + 7
            case "Linear scaling":
                fitness_function = 5*(-0.2 * x**2 + 6*x + 7)
            case "Quadratic scaling":
                fitness_function = (-0.2 * x**2 + 6*x + 7)^2
            case _:
                fitness_function = -0.2 * x**2 + 6*x + 7


        #fig, ax = plt.subplots()
        #ax.plot(x, fitness_function)
        #plt.show()






