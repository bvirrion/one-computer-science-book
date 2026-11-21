def line_total(price, quantity):
    return price * quantity


def show_line(name, price, quantity):
    total = line_total(price, quantity)
    print(f"{name:10} {quantity} x {price:5.2f} = {total:6.2f}")
    return total


def receipt():
    total = 0
    total = total + show_line("bread", 1.80, 2)
    total = total + show_line("apples", 0.45, 6)
    total = total + show_line("milk", 1.10, 3)
    print(f"{'TOTAL':22} {total:6.2f}")


receipt()
