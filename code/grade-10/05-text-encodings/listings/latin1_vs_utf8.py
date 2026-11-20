word = "été"
for encoding in ("latin-1", "utf-8", "utf-16-le"):
    data = word.encode(encoding)
    print(f"{encoding:9}  {len(data)} bytes  {data.hex(' ')}")

data = bytes([0x63, 0x61, 0x66, 0xE9])
print(data.decode("latin-1"), ascii(data.decode("mac_roman")))
