import turtle as t

t.setup(600,600)
t.bgcolor('white')
t.hideturtle()
t.shape('turtle')
t.pensize(1)
t.pencolor('red')
t.speed(6)

t.fillcolor('yellow')
t.begin_fill()
t.up()
t.goto(0,-50)
t.down()
t.circle(50)
t.end_fill()

t.up()
t.goto(-50,-50)
t.down()
for i in range(4):
    t.forward(100)
    t.left(90)

t.ht()

t.done()
