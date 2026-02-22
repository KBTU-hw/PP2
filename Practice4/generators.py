# ex 1
def square(n):
    for i in range(n+1):
        yield i**2
a=int(input())
print(",".join(str(x) for x in square(a)))
# ex 2
def even(n):
    c=0
    while c<=n:
        yield c
        c+=2
b=int(input())
print(",".join(str(x) for x in even(b)))
# ex 3
def div_3_4(n):
    c=0
    while c<=n:
        yield c
        c+=12
d=int(input())
print(",".join(str(x) for x in div_3_4(d)))
#4
def squareS(x, y):
    for i in range(x, y+1):
        yield i**2
x, y= map(int, input().split())
for i in squareS(x, y):
    print(i)
#5
def inver(c):
    for i in range(c,-1,-1):
        yield i
z=int(input())
print(",".join(str(i) for i in inver(z)))
