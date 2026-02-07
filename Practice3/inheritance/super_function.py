# Example 1
class person:
    def __init__(self, name):
        self.name=name
class student(person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade=grade
a=student("Bobik", 99)
print(a.name, a.grade)
# Example 2
class coor:
    def __init__(self, xval, yval):
        self.x=xval
        self.y=yval
    def printcoor(self):
        print(self.x, self.y )
class inver(coor):
    def __init__(self, xval, yval):
        super().__init__(xval, yval)
    def printcoor(self):
        super().printcoor()
        print(-self.x, -self.y)
x=coor(3, 4)
x.printcoor()
y=inver(-2,3)
y.printcoor()