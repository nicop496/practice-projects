import turtle as t

def sun(times, n):
    if times == 0:
        return
    t.forward(n)
    t.left(179)
    sun(times-1, n-5)

def circle(radius, distance_between_lines, grades=360*2):
    if grades <= distance_between_lines:
        return

    t.left(360-grades)
    grades -= distance_between_lines
    t.right(360-grades)
    t.forward(radius)
    t.backward(radius)
    circle(radius, distance_between_lines, grades=grades-distance_between_lines)

t.bgcolor("black")
t.speed(0)
t.color("yellow")

#circle(300, 10)
sun(300, -10)

t.mainloop()
