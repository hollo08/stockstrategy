class Canvas:
    def draw_pic(self, shape):
        print('\n--开始绘图--')
        shape.draw(self)
class Rectangle:
    def draw(self, canvas):
        print('即开始绘制矩形' )
class Triangle:
    def draw(self, canvas):
        print('即开始绘制三角形')
class Circle:
    def draw(self, canvas):
        print('即开始绘制圆形')
class Line:
    def draw(self, canvas):
        print('即开始绘制直线')
class Arc:
    def draw(self, canvas):
        print('即开始绘制圆弧')

c = Canvas()
# 传入Rectangle参数，绘制矩形
c.draw_pic(Rectangle())
# 传入Triangle参数，绘制三角形
c.draw_pic(Triangle())
# 传入Circle参数，绘制圆形
c.draw_pic(Circle())
# 传入Line参数，绘制直线
c.draw_pic(Line())
# 传入Line参数，绘制圆弧
c.draw_pic(Arc())
