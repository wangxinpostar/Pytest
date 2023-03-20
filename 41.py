import turtle as t
t.pensize(1)
t.hideturtle()
t.pencolor("black")
t.setup(0.7,0.7)

t.penup()
t.goto(150,-100)
t.pendown()

t.begin_fill()
t.fillcolor("green")
for i in range(3):
    t.left(120)
    t.fd(450)
t.end_fill()

t.back(150)
t.left(60)
t.back(150)

t.begin_fill()
t.fillcolor("green")
for i in range(3):
    t.fd(450)
    t.left(120)
t.end_fill()

t.fd(150)

t.begin_fill()
t.fillcolor("red")
for i in range(6):
    t.fd(150)
    t.left(60)
t.end_fill()

t.done()