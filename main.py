import matplotlib.pyplot as plt
import numpy as np
import sys
from tkinter import *
from tkinter import ttk
from GeneticAlgorithm import GeneticAlgorithm

def main():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Mutation chance:", padding=10).grid(column=0, row=0, sticky=W)
    ttk.Label(frm, text="Crossover chance:", padding=10).grid(column=1, row=0, sticky=W)
    ttk.Label(frm, text="Max number of generations:", padding=10).grid(column=2, row=0, sticky=W)
    ttk.Label(frm, text="Starting population:", padding=10).grid(column=3, row=0, sticky=W)
    ttk.Label(frm, text="Fitness function:", padding=10).grid(column=0, row=2, sticky=W)

    mutation = ttk.Entry(frm)
    mutation.grid(column=0, row=1,  padx=10, sticky=W)
    crossover = ttk.Entry(frm)
    crossover.grid(column=1, row=1, padx=10, sticky=W)
    generations = ttk.Entry(frm)
    generations.grid(column=2, row=1, padx=10, sticky=W)
    population = ttk.Entry(frm)
    population.grid(column=3, row=1, padx=10, sticky=W)

    options = ["Examined function", "Linear scaling", "Quadratic scaling"]
    combo = ttk.Combobox(frm, values=options)
    combo.grid(column=1, row=2, padx=10, sticky=W)
    ttk.Button(frm, text="Start algorithm", command=lambda: startalgorithm(mutation, crossover, generations, population, combo)).grid(column=2, row=4)
    root.mainloop()

def startalgorithm(mutation, crossover, generations, population, combo):
    mutation_value = float(mutation.get())
    crossover_value = float(crossover.get())
    generations_value = int(generations.get())
    population_value = int(population.get())
    function_value = combo.get()
    genalgorithm = GeneticAlgorithm(mutation_value, crossover_value, generations_value, population_value, function_value)
    genalgorithm.startgenetic()

if __name__ == '__main__':
    main()