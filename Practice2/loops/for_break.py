# Example 1
a=int(input())
for i in range(10):
    if i==a: break
    print(i)
# Example 2
s="Hello"
for i in s:
    if i=="l":
        print("lol")
        break
    print(i)
# Example 3
b=0
for i in range(10):
    if b>30: break
    b+=i
print(b)