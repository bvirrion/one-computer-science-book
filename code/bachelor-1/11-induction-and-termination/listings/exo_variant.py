"""exo_variant.py: exercise 5; the student's variant is n."""


def steps(n, step):
    print(f"steps({n}, {step})")
    if n <= 0:
        return 0
    if step == 0:
        return steps(n, 1)  # start moving
    return 1 + steps(n - step, step)


print("result", steps(3, 0))
