import tkinter
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Mutation chance:", padding=10).grid(column=0, row=0)
ttk.Label(frm, text="Crossover chance:", padding=10).grid(column=1, row=0)
ttk.Label(frm, text="Max number of generations:", padding=10).grid(column=2, row=0)

Mutation = ttk.Entry(frm).grid(column=0, row=1, padx=15)
Crossover = ttk.Entry(frm).grid(column=1, row=1, padx=15)
Generations = ttk.Entry(frm).grid(column=2, row=1, padx=15)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()