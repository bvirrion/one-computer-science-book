import dis


def count_down(n):
    while n > 0:
        n = n - 1
    return n


dis.dis(count_down)
