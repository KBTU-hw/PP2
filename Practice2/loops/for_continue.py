# Example 1
for i in range(10):
    if i%2==0: continue
    print("odd")
# Example 2
a="Hello World"
for i in a:
    if i=="l" or i==" ": continue
    print(i)
# Example 3
c=1
for i in range(10):
    if i<c: continue
    c*=i
print(c)