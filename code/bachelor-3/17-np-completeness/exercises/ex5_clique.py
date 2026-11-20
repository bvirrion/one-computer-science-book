"""ex5_clique.py -- exercise 5: 3-SAT to clique. One vertex per literal of each clause;
k = number of clauses. The buggy version also joins literals of the same clause."""
import itertools


def buggy(clauses):
    vertices = [(j, lit) for j, c in enumerate(clauses) for lit in c]
    edges = [(a, b) for a, b in itertools.combinations(range(len(vertices)), 2)
             if vertices[a][1] != -vertices[b][1]]
    return vertices, edges, len(clauses)


def fixed(clauses):
    # the fix: a clique must take one literal from each clause, so literals of the same
    # clause must not be joined
    vertices = [(j, lit) for j, c in enumerate(clauses) for lit in c]
    edges = [(a, b) for a, b in itertools.combinations(range(len(vertices)), 2)
             if vertices[a][0] != vertices[b][0] and vertices[a][1] != -vertices[b][1]]
    return vertices, edges, len(clauses)
