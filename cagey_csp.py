# =============================
# Student Names: Tirthkumar Patel
# Group ID: 067
# Date: Jan 26, 2026
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    """
    creating a CAGEY grid CSP using binery not equal constraints. 
    """
    n = cagey_grid[0]
    var_array = []
    var_matrix = {}

    for row in range(1, n+1):
        for col in range(1, n+1):
            var_name = f"Cell({row},{col})"
            var = Variable(var_name, list(range(1, n+1)))
            var_array.append(var)
            var_matrix[(row, col)] = var
    csp = CSP(f"BinaryNE-Cagey-{n}x{n}", var_array)  #creating CSP

    #adding binary not-equal constraints for rows 
    for row in range(1, n+1):   
        for col1 in range(1, n+1):
            for col2 in range(col1 + 1, n+1):
                var1 = var_matrix[(row, col1)]
                var2 = var_matrix[(row, col2)]

                con_name = f"Row{row}:({col1},{col2})"
                constraint = Constraint(con_name, [var1, var2])
                #adding all satisfying tuples where values are different
                sat_tuples = []
                for val1 in range(1, n+1):
                    for val2 in range(1, n+1):
                        if val1 != val2:
                            sat_tuples.append((val1, val2))
                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    #adding binary not-equal constraints for columns
    for col in range(1, n+1):
        for row1 in range(1, n+1):
            for row2 in range(row1+1, n+1):
                var1 = var_matrix[(row1, col)]
                var2 = var_matrix[(row2, col)]

                con_name = f"Col{col}:({row1},{row2})"
                constraint = Constraint(con_name, [var1, var2])

                sat_tuples = []
                for val1 in range(1, n+1):
                    for val2 in range(1, n+1):
                        if val1 != val2:
                            sat_tuples.append((val1, val2))
                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)
    
    return csp, var_array


def nary_ad_grid(cagey_grid):
    ## IMPLEMENT
    """
    creating a CAGEY grid CSP model using n-ary all different constraints.
    """

    n = cagey_grid[0]
    var_array = []
    var_matrix = {}

    for row in range(1, n+1):
        for col in range(1, n+1):
            var_name = f"Cell({row},{col})"
            var = Variable(var_name, list(range(1, n+1)))
            var_array.append(var)
            var_matrix[(row, col)] = var
    #creating CSP 
    csp = CSP(f"NaryAD-Cagey-{n}x{n}", var_array)

    #adding n-ary all-different constraints for all row
    for row in range(1, n+1):
        row_vars = [var_matrix[(row, col)] for col in range(1, n+1)]
        con_name = f"Row{row}-AllDiff"
        constraint = Constraint(con_name, row_vars)
        #generating all permutations of 1 to n as satisfying tuples
        sat_tuples = list(itertools.permutations(range(1, n+1)))
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)

    #adding n-ary all-different constraints for all row
    for col in range(1, n+1):
        col_vars = [var_matrix[(row, col)] for row in range(1, n+1)]
        con_name = f"Col{col}-AllDiff"
        constraint = Constraint(con_name, col_vars)

        sat_tuples = list(itertools.permutations(range(1, n+1)))
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)

    return csp, var_array


def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    """
    creating a complete CAGEY CSP using both grid and cage constraint.
    This uses n-ary all different for grid plus cage constraints. 
    """
    n = cagey_grid[0]
    cages = cagey_grid[1]

    #starting with n-ary grid model 
    csp, var_array = nary_ad_grid(cagey_grid)

    #creating a mapping from row and col to variable for easy access
    var_matrix = {}

    for row in range(1, n+1):
        for col in range(1, n+1):
            idx = (row - 1)*n + (col -1)
            var_matrix[(row, col)] = var_array[idx]

    #storing operator variable
    operator_vars = []


    for cage_idx, cage in enumerate(cages):
        target = cage[0]
        cells = cage[1]
        operation = cage[2]

        #getting the var in this cage 
        cage_vars = [var_matrix[cell] for cell in cells]
        num_vars = len(cage_vars)

        #complete cage constraint logic
        if operation == '?':
            ops = ['+', '-', '*', '/', '%']
            var_names_str = ', '.join([f"Var-Cell({r},{c})" for r, c in cells])
            op_var_name = f"Cage_op({target}:?:[{var_names_str}])"
            op_var = Variable(op_var_name, ops)
            operator_vars.append(op_var)

            con_name = f"Cage{cage_idx}({target}:?)"
            constraint = Constraint(con_name, [op_var] + cage_vars)

            sat_tuples = []
            for values in itertools.product(range(1, n+1), repeat = num_vars):
                for op in ops:

                    if num_vars == 1:
                        if values[0] == target:
                            sat_tuples.append((op,) + values)
                    else:
                        found_valid = False

                        for perm in itertools.permutations(values):
                            valid = True

                            if op == '%':
                                sum_remaining = sum(perm[1:])
                                result = sum_remaining % perm[0]
                                valid = (result == target)
                            else:
                                result = perm[0]
                                for i in range(1, num_vars):
                                    if op == '+':
                                        result = result + perm[i]
                                    elif op == '-':
                                        result = result - perm[i]
                                    elif op == '*':
                                        result = result * perm[i]
                                    elif op == '/':
                                        if perm[i] == 0:
                                            valid = False
                                            break 
                                        if result % perm[i] != 0:
                                            valid = False 
                                            break
                                        result = result // perm[i]
                                if valid:
                                    valid = (result == target)
                                
                            if valid:
                                found_valid = True
                                break
                        if found_valid:
                            for perm in set(itertools.permutations(values)):
                                sat_tuples.append((op,) + perm)
                            
            constraint.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(constraint)
        else:

            #start
            ops = [operation]
            var_names_str = ', '.join([f"Var-Cell({r},{c})" for r,  c in cells])
            op_var_name = f"Cage_op({target}:{operation}:[{var_names_str}])"
            op_var = Variable(op_var_name, ops)
            operator_vars.append(op_var)

            con_name = f"Cage{cage_idx}({target}:{operation})"
            constraint = Constraint(con_name, [op_var] + cage_vars)

            sat_tuples = []
            for values in itertools.product(range(1, n+1), repeat = num_vars):
                if num_vars == 1:
                    if values[0] == target:
                        sat_tuples.append((operation,) + values)
                else:
                    found_valid = False
                    for perm in itertools.permutations(values):
                        valid = True

                        if operation == '%':
                            sum_remaining = sum(perm[1:])
                            result = sum_remaining % perm[0]
                            valid = (result == target)
                        else:
                            result = perm[0]
                            for i in range(1, num_vars):
                                if operation == '+':
                                    result = result + perm[i]
                                elif operation == '-':
                                    result = result - perm[i]
                                elif operation == '*':
                                    result = result * perm[i]
                                elif operation == '/':
                                    if perm[i] == 0:
                                        valid = False
                                        break
                                    if result % perm[i] != 0:
                                        valid = False
                                        break
                                    result = result // perm[i]
                            if valid:
                                valid = (result == target)

                        if valid:
                            found_valid = True
                            break

                    if found_valid:
                        for perm in set(itertools.permutations(values)):
                            sat_tuples.append((operation,) + perm)
            
            constraint.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(constraint)

    #adding operator var to CSP and var_array
    for op_var in operator_vars:
        csp.add_var(op_var)
        var_array.append(op_var)

    return csp, var_array
                            
    
