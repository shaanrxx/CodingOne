## Week 7

## Finish the draw_polygon function

import turtle as t

tu = t.Turtle()


tu.penup()
tu.goto(-50, 100)
tu.pendown()

num_sides = 3

while num_sides != 10:
    for _ in range(num_sides):
        angle = 360 / num_sides
        tu.forward(100)
        tu.right(angle)
    num_sides += 1

screen = t.Screen()
screen.exitonclick()
