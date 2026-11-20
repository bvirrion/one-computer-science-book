for c in "Aa0 ~":
    print(repr(c), ord(c), hex(ord(c)), format(ord(c), "07b"))
print(chr(66), chr(98), chr(0x41 + 25))
print(ord("a") - ord("A"), chr(ord("g") - 32))
