def weighted_sum(code):
    """The digits of code, from the right, times 1, 3, 1, 3, ..."""
    total = 0
    weight = 1
    while code > 0:
        total = total + weight * (code % 10)
        code = code // 10
        weight = 4 - weight          # 1 becomes 3, 3 becomes 1
    return total


def check_digit(first12):
    """The digit that makes the weighted sum of the 13 digits a multiple of 10."""
    return (10 - weighted_sum(first12 * 10) % 10) % 10


def is_valid(code):
    return weighted_sum(code) % 10 == 0


if __name__ == "__main__":
    print(weighted_sum(5901234123457))
    print(check_digit(590123412345))
    print(is_valid(5901234123457), is_valid(5901234123458))
