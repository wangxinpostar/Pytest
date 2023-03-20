import turtle as t

t.setup(600,600)
t.bgcolor('white')
t.hideturtle()
t.shape('turtle')
t.pensize(1)
t.pencolor('black')
t.speed(0)

t.fillcolor('black')
t.begin_fill()
t.seth(-30)
t.forward(30)
t.right(-90)
t.circle(30,-120)
t.right(-90)
t.forward(30)

n=120/40
for i in range(60):
    t.forward(150)
    t.left(90)
    t.circle(150,1)
    t.left(90)
    t.forward(150)
    t.right(179)
t.end_fill()

t.ht()

t.done()
