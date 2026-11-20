keys = 1
for choices in range(26, 0, -1):
    keys = keys * choices
seconds = keys / 1_000_000_000          # a billion keys per second
years = seconds / (365 * 24 * 3600)
print(f"{years:,.0f} years")
