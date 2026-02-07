# Example 1
students = [("Bobik", 3), ("Ebobik", 67), ("Aibar", 17)]
sorted_students = sorted(students, key=lambda x: -x[1])
print(sorted_students)
# Example 2
words = ["Bobik", "Ebobik", "Aibar"]
sorted_words = sorted(words, key=lambda x: (len(x), x[0]))
print(sorted_words)