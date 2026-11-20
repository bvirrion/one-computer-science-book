# For a packet going to router F, each router knows only the next router to pass it to.
next_step = {"A": "B", "B": "C", "C": "F", "D": "E", "E": "F"}

router = "A"
path = [router]
while router != "F":
    router = next_step[router]
    path.append(router)
print(" -> ".join(path), "in", len(path) - 1, "steps")
