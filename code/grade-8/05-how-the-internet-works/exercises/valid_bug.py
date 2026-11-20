def is_valid(address):
    """True when address is four whole numbers separated by dots."""
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
    return True
