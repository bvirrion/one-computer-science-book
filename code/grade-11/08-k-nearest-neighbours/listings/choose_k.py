"""Choose k on the validation set: the smallest k with the fewest errors."""
from error_rate import error_rate, scaled, train, validation

errors = {k: error_rate(train, validation, k, scaled) for k in range(1, 16)}
best = min(errors.values())
chosen = min(k for k in errors if errors[k] == best)
print("lowest validation error:", f"{best:.1%}", "for k in",
      [k for k in errors if errors[k] == best])
print("chosen: k =", chosen)
