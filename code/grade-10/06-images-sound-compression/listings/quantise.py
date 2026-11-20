def quantise(value, levels):
    """Round a grey value 0..255 to the nearest of `levels` evenly spaced values."""
    step = 255 / (levels - 1)
    return round(round(value / step) * step)


greys = list(range(256))
for levels in (256, 16, 8, 2):
    errors = [abs(g - quantise(g, levels)) for g in greys]
    step = 255 / (levels - 1)
    print(f"{levels:3} levels: step {step:6.2f}  largest error {max(errors)}")
print([quantise(g, 8) for g in (0, 20, 100, 128, 200, 255)])
