from pyscipopt import Model
import numpy as np

def find_best_combination(arrays):
    num_arrays = len(arrays)
    num_indices = len(arrays[0])
    
    # SCIP Modell erstellen
    model = Model("Set Covering")
    
    # Binäre Variablen für jedes Unterarray
    x = {}
    for i in range(num_arrays):
        x[i] = model.addVar(vtype="B", name=f"x_{i}")
    
    # Jede Spalte (Index) muss mindestens einmal abgedeckt werden
    for j in range(num_indices):
        model.addCons(sum(x[i] for i in range(num_arrays) if arrays[i][j]) >= 1)
    
    # Zielfunktion: Minimierung der Anzahl der gewählten Unterarrays
    model.setObjective(sum(x[i] for i in range(num_arrays)), "minimize")
    
    # Problem lösen
    model.optimize()
    
    # Ergebnisse auslesen
    selected_indices = [i for i in range(num_arrays) if model.getVal(x[i]) > 0.5]
    return selected_indices
