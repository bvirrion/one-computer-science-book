def is_valid(address):
    """True when address is four numbers from 0 to 255 separated by dots."""
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or int(part) > 255:
            return False
    return True
