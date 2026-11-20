from turtle import forward, left, penup, pendown, done

for square in range(5):
    size = 20 + 10 * square      # 20, 30, 40, 50, 60
    for _ in range(4):           # one square
        forward(size)
        left(90)
    penup()
    forward(size + 15)           # move to the next square
    pendown()
done()
