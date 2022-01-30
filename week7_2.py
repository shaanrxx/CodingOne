## Week 7 part 2

## Implement a Random Walker using Turtle Graphics

from turtle import Turtle, Screen
from random import choice
import random
import turtle

t = Turtle()
t.pensize(6)
t.hideturtle()
t.speed(7)

def change_color():
    R = random.random()
    G = random.random()
    B = random.random()

    turtle.color(R, G, B)

directions = [0, 90, 180, 270]

while True:
    #t.colour(randomcolour.RandomColour().generate)
    change_color()
    t.setheading(choice(directions))
    t.forward(20)
    #random_color()








Screen().exitonclick()