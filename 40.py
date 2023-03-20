import turtle as t
t.pensize(1)
t.pencolor("black")
t.hideturtle()
c=["yellow","red","green","blue"]
for i in range(4):
    t.left(45)
    t.begin_fill()
    t.fillcolor(c[i])
    t.fd(100)
    t.left(90)
    t.circle(100,45)
    t.left(90)
    t.fd(100)
    t.end_fill()
t.done()