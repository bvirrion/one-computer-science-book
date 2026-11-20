def digit_sum(n):
    total = 0
    while n > 0:
        total = total + n % 10
        n = n // 10
    return total


# expected values worked out by hand
print("expected 10, got", digit_sum(2026))
print("expected 0, got", digit_sum(0))
print("expected 7, got", digit_sum(7))
print("expected 1, got", digit_sum(1000))
print("expected 45, got", digit_sum(123456789))
