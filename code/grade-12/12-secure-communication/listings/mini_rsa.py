"""A miniature RSA key pair: encrypt with the public key, sign with the private key."""
import hashlib


def make_keys(p, q, e):
    """From two primes and an exponent: public key (n, e), private key (n, d)."""
    n, phi = p * q, (p - 1) * (q - 1)
    d = pow(e, -1, phi)                          # d * e = 1 modulo phi
    return (n, e), (n, d)


def apply(key, x):
    n, k = key
    return pow(x, k, n)                          # x**k modulo n


def digest_number(message, n):
    """The SHA-256 digest of the message, as a number reduced modulo n."""
    return int.from_bytes(hashlib.sha256(message.encode()).digest(), "big") % n


def sign(private, message):
    return apply(private, digest_number(message, private[0]))


def verify(public, message, signature):
    return apply(public, signature) == digest_number(message, public[0])


if __name__ == "__main__":
    public, private = make_keys(61, 53, 17)
    print("public key (n, e):", public, "  private key (n, d):", private)
    c = apply(public, 65)
    print("65 encrypted:", c, "  decrypted:", apply(private, c))
    s = sign(private, "Pay Bea 20")
    print("signature of 'Pay Bea 20':", s)
    print("checked on 'Pay Bea 20':", verify(public, "Pay Bea 20", s))
    print("checked on 'Pay Bea 90':", verify(public, "Pay Bea 90", s))
