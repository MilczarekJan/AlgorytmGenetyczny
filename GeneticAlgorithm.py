class GeneticAlgorithm:
    def __init__(self, mutation_chance, crossover_chance, number_of_generations, function, domain) -> None:
        self.MutationChance = mutation_chance
        self.CrossoverChance = crossover_chance
        self.NumberOfGenerations = number_of_generations
        self.FitnessFunction = function
        self.FunctionDomain = domain

    def show(self):
        print(self.MutationChance)
        print(self.CrossoverChance)
        print(self.NumberOfGenerations)
        print(self.FitnessFunction)
        print(self.FunctionDomain)






