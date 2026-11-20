from shift import encrypt

ciphertext = "gur obng yrnirf ng qnja"
for key in range(1, 26):
    print(f"{key:>2}: {encrypt(ciphertext, -key)}")
