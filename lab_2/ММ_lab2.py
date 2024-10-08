import numpy as np

# objective function:
# maximize z = 2x1 - x2 + 3x3 + x4

# subject to:
# 2x1 + x2 - 3x3          = 10      (1)
# x1      + x3 + x4       = 7       (2)
# -3x1         - 2x3 + x5 = 4       (3)

# xj >= 0 for j = 1 to 5

def simplex_method():
    # variables order: x1, x2, x3, x4, x5 | RHS
    tableau = np.array([
        [ 2,  1, -3,  0,  0, 10],
        [ 1,  0,  1,  1,  0,  7],
        [-3,  0, -2,  0,  1,  4],
        [-2, -1,  3,  1,  0,  0]    # objective function row (max z)
    ], dtype=float)

    # indicate which variables are basic and non-basic
    basic_vars = [2, 3, 4]  # (x3, x4, x5)
    non_basic_vars = [0, 1]  # (x1, x2)

    num_vars = 5  # variables x1 to x5
    num_constraints = 3  # constraints

    iteration = 0

    while True:
        print(f"\nIteration {iteration}")
        print("Tableau:")
        print(tableau)

        # check if the solution is optimal by checking if there are any positive coefficients
        z_row = tableau[-1, :-1]
        if all(coef <= 0 for coef in z_row):  # no positive coefficients
            print("Optimal solution found.")
            break

        # choose entering variable (variable with the highest positive coefficient)
        entering_var_index = np.argmax(z_row)
        print(f"Entering variable: x{entering_var_index + 1}")

        # determine the leaving variable
        ratios = []
        for i in range(num_constraints):
            row = tableau[i]
            coef = row[entering_var_index]
            rhs = row[-1]
            if coef > 0:
                ratio = rhs / coef
                ratios.append((ratio, i))
            else:
                ratios.append((np.inf, i))

        if all(ratio[0] == np.inf for ratio in ratios):
            print("Unbounded solution.")
            return

        # choose the pivot row (leaving variable)
        _, pivot_row_index = min(ratios, key=lambda x: x[0])
        leaving_var_index = basic_vars[pivot_row_index]
        print(f"Leaving variable: x{leaving_var_index + 1}")

        # pivot operation
        pivot_element = tableau[pivot_row_index, entering_var_index]
        tableau[pivot_row_index] = tableau[pivot_row_index] / pivot_element

        # update the rest of the tableau
        for i in range(len(tableau)):
            if i != pivot_row_index:
                row_factor = tableau[i, entering_var_index]
                tableau[i] = tableau[i] - row_factor * tableau[pivot_row_index]

        # update basic and non-basic variables
        basic_vars[pivot_row_index] = entering_var_index
        non_basic_vars = [i for i in range(num_vars) if i not in basic_vars]

        iteration += 1

    # extract the solution
    solution = np.zeros(num_vars)
    for i in range(num_constraints):
        var_index = basic_vars[i]
        solution[var_index] = tableau[i, -1]

    z_value = -tableau[-1, -1]

    print("\nOptimal Solution:")
    for i in range(num_vars):
        print(f"x{i+1} = {solution[i]}")
    print(f"Optimal value of z = {z_value}")

if __name__ == "__main__":
    simplex_method() 
    
# result 

"""
Iteration 0
Tableau:
[[ 2.  1. -3.  0.  0. 10.]
 [ 1.  0.  1.  1.  0.  7.]
 [-3.  0. -2.  0.  1.  4.]
 [-2. -1.  3.  1.  0.  0.]]
Entering variable: x3
Leaving variable: x4

Iteration 1
Tableau:
[[  5.   1.   0.   3.   0.  31.]
 [  1.   0.   1.   1.   0.   7.]
 [ -1.   0.   0.   2.   1.  18.]
 [ -5.  -1.   0.  -2.   0. -21.]]
Optimal solution found.

Optimal Solution:
x1 = 0.0
x2 = 0.0
x3 = 7.0
x4 = 0.0
x5 = 18.0
Optimal value of z = 21.0

""" 