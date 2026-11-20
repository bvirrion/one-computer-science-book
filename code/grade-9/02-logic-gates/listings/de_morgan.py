from gates import AND, NOT, OR

print("a b | NOT(a AND b)  (NOT a) OR (NOT b) | NOT(a OR b)  (NOT a) AND (NOT b)")
for a in [0, 1]:
    for b in [0, 1]:
        left = f"{NOT(AND(a, b)):^12}  {OR(NOT(a), NOT(b)):^18}"
        right = f"{NOT(OR(a, b)):^11}  {AND(NOT(a), NOT(b)):^19}"
        print(f"{a} {b} | {left} | {right}".rstrip())
