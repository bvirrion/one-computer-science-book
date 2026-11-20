from toymachine import assemble

code = assemble(open("add_two.toy").read())
for address in range(0, 10, 2):
    first, second = code[address], code[address + 1]
    print(f"{address:3}: {first:3} {second:3}   {first:08b} {second:08b}")
