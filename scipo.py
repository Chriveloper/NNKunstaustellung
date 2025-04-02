from pyscipopt import Model


def getCombination(guardAreas):
    # Number of art pieces (assumed from boolean lists)
    print(guardAreas)
    num_art_pieces = len(guardAreas[0])  # Assume each row corresponds to a guard
    
    # Create the optimization model
    model = Model("Guard Optimization")
    
    # Create guard decision variables (1 if a guard is used, 0 otherwise)
    guards = {guard: model.addVar(f"guard_{guard}", vtype="B") for guard in range(len(guardAreas))}
    
    # Apply constraints: ensure each art piece is covered by at least one active guard
    for art_idx in range(num_art_pieces):
        model.addCons(
            sum(guards[guard] for guard in range(len(guardAreas)) if guardAreas[guard][art_idx]) >= 1
        )
    
    # Objective function: Minimize the total number of guards used
    model.setObjective(sum(guards.values()), "minimize")
    
    # Solve the model
    model.optimize()

    # Output results
    if model.getStatus() == "optimal":
        active_guards = []
        for guard, var in guards.items():
            if model.getVal(var) > 0.5:  # Check if the guard is active (1)
                active_guards.append(guard)
        return active_guards
    else:
        return "No optimal solution found"

