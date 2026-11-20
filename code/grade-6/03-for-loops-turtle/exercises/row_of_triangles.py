from turtle import forward, left, done

for _ in range(5):          # five triangles
    for _ in range(3):      # the three sides of one triangle
        forward(50)
        left(120)
    forward(50)             # move along to the next one
done()
