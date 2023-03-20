import turtle as t

t.setup(600,600)
t.bgcolor('white')

t.shape('turtle')
t.pensize(1)
t.speed(0)

r=120
t.up()
t.fd(r)
t.down()

for n in range(12):
    t.fillcolor('yellow')
    t.begin_fill()
    t.left(30)
    for i in range(2):
        t.fd(80)
        t.right(60)
        t.fd(80)
        t.right(120)
    t.end_fill()
    t.left(60)
    t.circle(r,30)
    t.right(90)

t.up()
t.goto(0,-120)
t.down()
t.pencolor('red')
t.circle(120)

t.ht()
t.done()
