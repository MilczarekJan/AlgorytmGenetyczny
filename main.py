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
    ttk.Label(frm, text="Fitness function:", padding=10).grid(column=0, row=2, sticky=W)
    ttk.Label(frm, text="Function domain:", padding=10).grid(column=0, row=3, sticky=W)
    ttk.Label(frm, text="Min:", padding=10).grid(column=1, row=3, sticky=E)
    ttk.Label(frm, text="Max:", padding=10).grid(column=3, row=3, sticky=E)

    mutation = ttk.Entry(frm)
    mutation.grid(column=0, row=1,  padx=10, sticky=W)
    crossover = ttk.Entry(frm)
    crossover.grid(column=1, row=1, padx=10, sticky=W)
    generations = ttk.Entry(frm)
    generations.grid(column=2, row=1, padx=10, sticky=W)
    minx = ttk.Entry(frm)
    minx.grid(column=2, row=3, padx=10, sticky=W)
    maxx = ttk.Entry(frm)
    maxx.grid(column=4, row=3, padx=10, sticky=W)

    options = ["Examined function", "Linear scaling", "Quadratic scaling"]
    combo = ttk.Combobox(frm, values=options)
    combo.grid(column=1, row=2, padx=10, sticky=W)
    ttk.Button(frm, text="Start algorithm", command=lambda: startalgorithm(mutation, crossover, generations, minx, maxx, combo)).grid(column=2, row=4)
    root.mainloop()

def startalgorithm(mutation, crossover, generations, minx, maxx, combo):
    mutation_value = mutation.get()
    crossover_value = crossover.get()
    generations_value = generations.get()
    minx_value = minx.get()
    maxx_value = maxx.get()
    function_value = combo.get()
    genalgorithm = GeneticAlgorithm(mutation_value, crossover_value, generations_value, function_value, (minx_value, maxx_value))
    genalgorithm.show()


if __name__ == '__main__':
    main()