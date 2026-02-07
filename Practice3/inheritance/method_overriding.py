# Example 1
class per:
    def lol(self):
        print("LOL")
class st(per):
    def lol(self):
        print("lol")
a = per()
b = st()
a.lol()
b.lol()
# Example 2
class person:
    def __init__(self, name, surname):
        self.name=name
        self.surname=surname
    def printname(self):
        print(self.name, self.surname)
class student(person):
    def __init__(self, name):
        self.name=name
        self.surname=name
    def printname(self):
        print(self.name)
a=person("Bobik", "Ebobik")
a.printname()
b=student("Bobekk")
b.printname()
# Example 3
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
        return super().printcoor()
x=coor(3, 4)
x.printcoor()
y=inver(-2,3)
y.printcoor()