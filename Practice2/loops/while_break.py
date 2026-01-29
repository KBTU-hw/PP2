# Example 1
i=0
while True:
    print(i)
    if i==5:
        break
    i+=1
# Example 2
i=1
while i<0:
    i+=1
else:
    print(f"{i} > 0")
# Example 3
a="Hello"
i=0
while i<len(a):
    if a[i]=="l":
        print("lol")
        break
    print(i)
    i+=1
