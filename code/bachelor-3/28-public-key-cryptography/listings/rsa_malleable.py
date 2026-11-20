"""rsa_malleable.py -- two weaknesses of textbook RSA. It is deterministic: whoever
can guess the message can check the guess. It is malleable: anyone can turn the
encryption of m into the encryption of 2m without knowing m."""

import random

from rsa import decrypt, encrypt, keygen

pub, priv = keygen(1024, random.Random(28))
n, e = pub["n"], pub["e"]

vote = encrypt(pub, int.from_bytes(b"no", "big"))  # a council member's secret vote
for guess in (b"yes", b"no"):  # Eve encrypts each candidate with the public key
    print(
        f"Eve's guess {guess.decode()!r} matches:",
        encrypt(pub, int.from_bytes(guess, "big")) == vote,
    )

amount = 1500
c = encrypt(pub, amount)  # a payment order, encrypted to the treasurer
forged = c * pow(2, e, n) % n  # (2^e) (m^e) = (2m)^e mod n
print("the treasurer decrypts the forged order:", decrypt(priv, forged))
