"""Problem: when a signed 32-bit count of seconds since 1970 runs out, and what then."""
from datetime import UTC, datetime, timedelta

EPOCH = datetime(1970, 1, 1, tzinfo=UTC)
BITS = 32


def to_date(seconds):
    return EPOCH + timedelta(seconds=seconds)


def wrap_signed(x, n):
    """The n-bit two's complement reading of x, as a signed n-bit register keeps it."""
    u = x % 2**n
    return u - 2**n if u >= 2 ** (n - 1) else u


if __name__ == "__main__":
    largest = 2 ** (BITS - 1) - 1
    print("largest value:", largest)
    print("last instant: ", to_date(largest))
    after = wrap_signed(largest + 1, BITS)
    print("one second later the register holds", after)
    print("which reads as", to_date(after))
    print("unsigned 32 bits last:", to_date(2**BITS - 1))
    years = (2**63 - 1) / (86400 * 365.2425)
    print(f"signed 64 bits last for about {years / 1e9:.0f} billion years")
