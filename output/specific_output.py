# Sample JavaScript code
greeting = "Hello, World!"
pi = 3.14159

def add(a, b):
    return a + b

result = add(5, 7)
print(greeting)
print(f"The result is: {result}")

# Simple class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

john = Person("John", 30)
print(john.greet())

# Conditionals
if result > 10:
    print("Result is greater than 10")
else:
    print("Result is not greater than 10")

# Arrays and loops
numbers = [1, 2, 3, 4, 5]
sum = 0

for i in range(len(numbers)):
    sum += numbers[i]

print(f"Sum of numbers: {sum}")
