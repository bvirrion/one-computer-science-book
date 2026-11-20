"""ex6_col_to_sat.py -- exercise 6: 3-colouring to SAT. Variable var(v, c) says "vertex
v has colour c"; each vertex gets at least one colour and at most one, and the two ends
of an edge never share one."""
import itertools


def colouring_to_sat(n, edges, colours=3):
    def var(v, c):
        return v * colours + c + 1
    clauses = [[var(v, c) for c in range(colours)] for v in range(n)]
    for v in range(n):
        clauses += [[-var(v, a), -var(v, b)]
                    for a, b in itertools.combinations(range(colours), 2)]
    for u, v in edges:
        clauses += [[-var(u, c), -var(v, c)] for c in range(colours)]
    return clauses
