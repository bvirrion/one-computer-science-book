from turtle import forward, left, done

n = 6               # the number of sides: try 3, 5, 8, 36
for _ in range(n):
    forward(60)
    left(360 / n)
done()
