import math

#1
x=int(input())
print(math.radians(x))
#2
h=int(input())
a=int(input())
b=int(input())
print((a+b)*h/2)
#3
n=int(input())
l=int(input())
pi=math.pi
t=math.tan(pi/n)
print(f"{(n*l**2)/(4*t):.2f}")
#4
s=int(input())
k=int(input())
print(f"{s*k:.2f}")