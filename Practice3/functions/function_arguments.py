# Example 1
def hi(name):
  print(f"Hello, {name}")
hi("Bobik")
hi("Ebobik")
# Example 2
def name(a, b):
  return(f"{a} {b}")
name("Ebobik", "Bobik")
# Example 3
def calc(a, b):
  print(a+b)
calc(2, 3)
# Example 4
def all(int, str, float, bool, list, map):
  print(int)
  print(str)
  print(float)
  print(bool)
  print(*list)
  print(*((i, j) for i,j in map.items()))
all(5, ":)", 2.3, False, [2,3,5], {"key":"value"})