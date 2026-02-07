# Example 1
class person:
    def __init__(self, name, age):
        self.name=name
        self.age=age
    def hi(self):
        print(f"I'm {self.name}, {self.age} years old")
a=person("Bobik", 3)
a.hi()
# Example 2
class coor:
    def __init__(self, xval, yval):
        self.x=xval
        self.y=yval
    def dist(self, x0, y0):
        x=(self.x-x0)**2
        y=(self.y-y0)**2
        d=(x+y)**(1/2)
        print(d)
b=coor(3, 4)
b.dist(0, 0)