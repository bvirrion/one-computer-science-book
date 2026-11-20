def same_network(a, b):
    """True when the two addresses share their first three bytes."""
    return a.split(".")[:3] == b.split(".")[:3]
