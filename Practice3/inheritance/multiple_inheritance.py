# Example 1
class Flyer:
    def move(self):
        return "I can fly"

class Swimmer:
    def move(self):
        return "I can swim"

class Duck(Flyer, Swimmer):
    def move(self):
        return Flyer.move(self) + " and " + Swimmer.move(self)
d = Duck()
print(d.move())
# Example 2
class cx:
    def __init__(self, xval):
        self.x=xval
    def printcoor(self):
        print(self.x)

class cy:
    def __init__(self, yval):
        self.y=yval
    def printcoor(self):
        print(self.y)

class coor(cx, cy):
    def __init__(self, xval, yval):
        cx.__init__(self, xval)
        cy.__init__(self, yval)
    def printcoor(self):
        print(self.x, self.y)
x = cx(2)
x.printcoor()
y = cy(5)
y.printcoor()
c = coor(3, 4)
c.printcoor()
# Example 3
class Name:
    def __init__(self, name, **fulname):
        super().__init__(**fulname)
        self.name=name

class Surname:
    def __init__(self, surname, **fulname):
        super().__init__(**fulname)
        self.surname=surname

class person(Name, Surname):
    def __init__(self, name, surname):
        super().__init__(name=name, surname=surname)
    def printfulname(self):
        print(self.name, self.surname)

a = person("Bobik", "Ebobik")
a.printfulname()