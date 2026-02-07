# Example 1
numbers = [1, 2, 3, 4, 5, 6, 7]
odds = list(filter(lambda x: x % 2 != 0, numbers))
print(odds)
# Example 2
words = ["Bobik", "Ebobik", "Aibar"]
odds = list(filter(lambda x: "A" in x, words))
print(odds)