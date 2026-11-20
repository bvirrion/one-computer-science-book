"""ipv6_text.py: an IPv6 address in text, expanded to its eight groups of 16 bits."""
import ipaddress


def expand(text):
    if "::" in text:
        head, tail = text.split("::")
        left = head.split(":") if head else []
        right = tail.split(":") if tail else []
        groups = left + ["0"] * (8 - len(left) - len(right)) + right
    else:
        groups = text.split(":")
    assert len(groups) == 8
    return [int(g, 16) for g in groups]


for text in ["2001:db8::1", "2001:db8:0:0:1::", "::1", "2001:DB8:0:0:8:800:200C:417A"]:
    groups = expand(text)
    full = ":".join(f"{g:04x}" for g in groups)
    assert full == ipaddress.IPv6Address(text).exploded
    print(f"{text:29} {full}")
