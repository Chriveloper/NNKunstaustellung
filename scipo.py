from pyscipopt import Model

# Sample input dictionary where keys are art pieces, and values are lists of booleans (guard coverage)
art_visibility = {
    "art_1": [True, False, True],
    "art_2": [False, True, True],
    "art_3": [True, False, True],
}

# Number of guards (assuming it's the number of items in the boolean lists)
num_guards = len(next(iter(art_visibility.values())))

# Create the optimization model
model = Model("Guard Optimization")

# Create guard decision variables (1 if a guard is used, 0 otherwise)
guards = [model.addVar(f"guard_{i}", vtype="B") for i in range(num_guards)]

# Apply constraints: ensure each art piece is covered by at least one guard
for art, visibility in art_visibility.items():
    model.addCons(sum(guards[i] for i, can_see in enumerate(visibility) if can_see) >= 1)

# Objective function: Minimize the total number of guards used
model.setObjective(sum(guards), "minimize")

# Solve the model
model.optimize()

# Output results
if model.getStatus() == "optimal":
    print("Optimal solution found:")
    guard_assignments = [int(model.getVal(guard)) for guard in guards]
    for i, value in enumerate(guard_assignments):
        print(f"Guard {i + 1}: {'Active' if value else 'Not Active'}")
