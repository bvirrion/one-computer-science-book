from turtle import forward, left, done

n = 8               # the number of points
k = 3               # the number of full turns in all
for _ in range(n):
    forward(150)
    left(360 * k / n)
done()
