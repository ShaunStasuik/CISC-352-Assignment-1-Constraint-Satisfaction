# =============================
# Student Names:
#   Shaun Stasuik
#   Daryan Lindsay
#   Tirthkumar Patel
# Group ID: 067
# Course: CISC 352 – Artificial Intelligence
# Assignment: CSP Heuristics
# File: heuristics.py
# Date: Jan 26, 2026
# =============================
# Description:
# This file implements variable-ordering and value-ordering
# heuristics for CSP backtracking search, such as:
#  - Minimum Remaining Values (MRV)
#  - Degree heuristic
#  - Least Constraining Value (LCV)
#
# These heuristics guide search to improve efficiency.
# =============================


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    best_var = None
    best_degree = -1

    for v in csp.get_all_vars():
        if v.is_assigned():
            continue

        degree = 0
        for con in csp.get_cons_with_var(v):
            for u in con.get_scope():
                if u is not v and not u.is_assigned():
                    degree += 1
                    break   # count each constraint once

        if degree > best_degree:
            best_degree = degree
            best_var = v

    return best_var

def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    pass
    best_var = None
    best_size = float('inf')

    for v in csp.get_all_vars():
        if v.is_assigned():
            continue

        size = v.cur_domain_size()
        if size < best_size:
            best_size = size
            best_var = v

    return best_var
