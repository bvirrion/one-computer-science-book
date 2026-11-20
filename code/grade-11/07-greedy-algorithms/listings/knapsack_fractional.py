"""A sack of 15 kg, goods that can be cut: take the best value per kilogram first."""
GOODS = [("tea", 4, 60), ("rice", 10, 40), ("spices", 2, 50),
         ("coffee", 6, 72), ("flour", 8, 16)]          # name, kg, value


def fill(goods, capacity):
    load, value = [], 0
    for name, kg, worth in sorted(goods, key=lambda g: g[2] / g[1], reverse=True):
        take = min(kg, capacity)          # all of it, or what still fits
        if take == 0:
            break
        load.append((name, take))
        value += worth * take / kg
        capacity -= take
    return load, value


load, value = fill(GOODS, 15)
for name, kg in load:
    print(f"{name:7} {kg} kg")
print("value:", value)
