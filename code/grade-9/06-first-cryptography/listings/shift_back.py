from shift import encrypt

secret = encrypt("meet me at the lighthouse at nine", 3)
print("ciphertext:", secret)
print("decrypted: ", encrypt(secret, -3))        # move every letter back
