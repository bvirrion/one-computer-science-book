"""The basic gates, on the bits 0 and 1."""


def NOT(a):
    return 1 - a


def AND(a, b):
    return a & b


def OR(a, b):
    return a | b


def XOR(a, b):
    return a ^ b


def NOR(a, b):
    return NOT(OR(a, b))
