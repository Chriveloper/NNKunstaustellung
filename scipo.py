from pyscipopt import Model

# Sample input dictionary where keys are guards, and values are lists of booleans (which art pieces they cover)
guard_coverage = {
    "guard_1": [True, False, True, True, False, False, False],
    "guard_2": [False, True, True, False, False, True, False],
    "guard_3": [True, False, True, False, True, False, True],
    "guard_4": [False, False, True, False, True, False, False]
}

# Number of art pieces (assumed from boolean lists)
num_art_pieces = len(next(iter(guard_coverage.values())))

# Create the optimization model
model = Model("Guard Optimization")

# Create guard decision variables (1 if a guard is used, 0 otherwise)
guards = {guard: model.addVar(guard, vtype="B") for guard in guard_coverage.keys()}

# Apply constraints: ensure each art piece is covered by at least one active guard
for art_idx in range(num_art_pieces):
    model.addCons(
        sum(guards[guard] for guard, coverage in guard_coverage.items() if coverage[art_idx]) >= 1
    )

# Objective function: Minimize the total number of guards used
model.setObjective(sum(guards.values()), "minimize")

# Solve the model
model.optimize()

# Output results
if model.getStatus() == "optimal":
    print("Optimal solution found:")
    for guard, var in guards.items():
        print(f"{guard}: {'Active' if model.getVal(var) > 0.5 else 'Not Active'}")
