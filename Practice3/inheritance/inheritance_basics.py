# Example 1
class person:
    def __init__(self, name, surname):
        self.name=name
        self.surname=surname
    def printname(self):
        print(self.name, self.surname)
class student(person):
    def __init__(self, name, surname):
        self.name=name
        self.surname=name
a=person("Bobik", "Ebobik")
a.printname()
b=student("Bobekk", "LOll")
b.printname()
# Example 2
class coor:
    def __init__(self, xval, yval):
        self.x=xval
        self.y=yval
    def printcoor(self):
        print(self.x, self.y )
class inver(coor):
    def __init__(self, xval, yval):
        self.x=-xval
        self.y=-yval
    def printcoor(self):
        print(self.x, self.y)
x=coor(3, 4)
x.printcoor()
y=inver(-2,3)
y.printcoor()