# Example 1
def numbers(*num):
  print(num[2])
  print(type(num))
numbers("2", "3", "5")
# Example 2
def hum(hum, *num):
  print(hum, num[1])
hum("Bobik", "2", "3", "5")
# Example 3
def suum(*itn):
  s=0
  for i in itn:
    s+=i
  return(s)
print(suum(2, 3, 5))
