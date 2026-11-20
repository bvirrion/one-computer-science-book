from barcode import is_valid

code = 5901234123457
caught = 0
changes = 0
place = 1                            # 1, 10, 100, ...: the place of a digit
for _ in range(13):
    digit = code // place % 10
    for new in range(10):
        if new != digit:
            changes = changes + 1
            wrong = code + (new - digit) * place
            if not is_valid(wrong):
                caught = caught + 1
    place = place * 10
print(caught, "caught out of", changes)
