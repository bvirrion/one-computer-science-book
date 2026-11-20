def longest_equal_run(values):
    longest = 1
    run = 1
    for i in range(1, len(values)):
        if values[i] == values[i - 1]:
            run = run + 1
        else:
            run = 1
        if run > longest:
            longest = run
    return longest


print("expected 3, got", longest_equal_run([1, 2, 2, 2, 5, 5]))
print("expected 1, got", longest_equal_run([4, 3, 4]))
print("expected 4, got", longest_equal_run([7, 7, 7, 7]))
