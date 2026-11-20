"""The same key stream used twice: the two messages leak through their xor."""
from xor_stream import key_stream, xor_bytes

key = 314159
m1 = b"Meet at the bridge at noon"
m2 = b"Bring the map and a torch."
c1 = xor_bytes(m1, key_stream(key, len(m1)))
c2 = xor_bytes(m2, key_stream(key, len(m2)))

leak = xor_bytes(c1, c2)                         # the listener computes this
print("c1 xor c2 == m1 xor m2:", leak == xor_bytes(m1, m2))
guess = b"Meet at the "                  # a likely start for a message
print("guessing the start of m1 reveals:", xor_bytes(leak, guess).decode())
