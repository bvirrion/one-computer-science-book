for a in [False, True]:
    for b in [False, True]:
        if a:
            if b:
                first = "yes"
            else:
                first = "no"
        else:
            first = "no"
        if a and b:
            second = "yes"
        else:
            second = "no"
        print(a, b, first, second)
