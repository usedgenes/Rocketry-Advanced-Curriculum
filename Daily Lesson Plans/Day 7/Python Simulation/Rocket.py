import turtle
import matplotlib.pyplot as plt
import numpy as np

COLORS = ['g','g','r','c','m','y','k']


class Rocket(turtle.Turtle):
    def __init__(self, screen_width, screen_height, mass, mmoi, horizontalPosition):
        screen = turtle.Screen()
        screen.setup(screen_width, screen_height)
        self.rocket = turtle.Turtle()
        turtle.setworldcoordinates(0, 0, screen_width, screen_height)
        self.rocket.speed(0)
        self.rocket.penup()
        self.rocket.setpos(0, 1000)
        self.rocket.pendown()
        self.rocket.forward(screen_width)
        self.rocket.penup()
        
        turtle.register_shape('rocket.gif')
        self.rocket.shape('rocket.gif')
        self.rocket.resizemode("user")
        self.rocket.penup();
        self.rocket.shapesize(0.5, 0.5, 0)
        self.rocket.setpos(horizontalPosition, 30)
        self.mass = mass
        self.mmoi = mmoi
    def moveRocket(self, x, y):
        self.rocket.setx(x)
        self.rocket.sety(y*3.28 + 30)
    def rotateRocket(self, angle):
        self.rocket.setheading(np.rad2deg(angle))
    def getX(self):
        return self.rocket.xcor()
    def getY(self):
        return self.rocket.ycor();