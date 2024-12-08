import turtle

# 设置画布和画笔
window = turtle.Screen()
# 跳过绘画过程
# turtle.tracer(False)
window.bgcolor("white")
window.title("To Somebody~")
# 设置窗口大小
window.setup(400, 400)
love = turtle.Turtle()
love.color("red")
# 隐藏箭头
love.hideturtle()

love.begin_fill()
# 设置前进距离
fdd = 200

# 起点下移
love.penup()
love.goto(0, -150)
love.pendown()

# 校准方向为向上
love.setheading(90)
# 爱心右半绘制
love.right(45)
love.forward(fdd)
love.circle(fdd / 2, 180)

# 回归起点
love.penup()
love.goto(0, -150)
love.pendown()
# 校准方向为向上
love.setheading(90)

# 爱心左半绘制
love.left(45)
love.forward(fdd)
love.circle(-(fdd / 2), 180)

love.end_fill()

window.mainloop()
