# Advanced JavaScript code sample
# This file contains various JavaScript constructs to test the converter
# Basic console output
print("JavaScript to Python Converter Demo")
# Variable declarations and operations
name = "Rohit"
age = 25
isStudent = True
greeting = "Hello, " + str(name) + "!"
print(greeting)
# Numeric operations
a = 10
b = 20
sum = a + b
difference = b - a
product = a * b
quotient = b / a
print("Sum: " + str(sum))
print("Difference: " + str(difference))
print("Product: " + str(product))
print("Quotient: " + str(quotient))
# For loop with different variations
print("Counting from 0 to 4:")
for i in range(0, 5, 1):
    print("Count: " + str(i))
    # For loop with different increment
    print("Counting by 2:")
    for i in range(0, 11, 2):
        print("Count: " + str(i))
        # While loop
        print("Countdown from 3:")
        count = 3
        while count >= 0:
            print("Countdown: " + str(count))
            count -= 1
            # Nested conditional statements
            userAge = 20
            hasLicense = True
            if userAge >= 18:
                print("You are an adult")
                if hasLicense:
                    print("You can drive")else:
                        print("You need to get a license to drive")else:
                            print("You are a minor")
                            print("You cannot drive yet")
                            # Function definition with return value
                            def calculateSum(a, b):
                                return a + b
                                # Function with conditional logic
                                def checkEligibility(age, hasExperience):
                                    if age >= 18 && hasExperience:
                                        return "Eligible"
                                        else if age >= 18:
                                            return "Partially eligible"else:
                                                return "Not eligible"
                                                # Function calls
                                                result = calculateSum(5, 10)
                                                print("Sum: " + str(result))
                                                eligibility = checkEligibility(25, True)
                                                print("Eligibility status: " + str(eligibility))
                                                # Array operations
                                                fruits = ["apple", "banana", "orange", "grape", "mango"]
                                                print("First fruit: " + fruits[0])
                                                print("Last fruit: " + str(fruits)[len(fruits) - 1])
                                                print("Number of fruits: " + str(len(fruits)))
                                                # Array iteration
                                                print("All fruits:")
                                                for i = 0; i < len(fruits); i += 1:
                                                    print(i + str(1) + ". " + str(fruits)[i])
                                                    # Simple class with methods
                                                    class Person:
                                                        def __init__(self, name, age):
                                                            self.name = name
                                                            self.age = age
                                                            self.isAdult = age >= 18
                                                            def greet(self):
                                                                print(f"Hello, my name is {self.name} and I am {self.age} years old.")
                                                                def canVote(self):
                                                                    if self.isAdult:
                                                                        return self.str(name) + " can vote"else:
                                                                            return self.str(name) + " cannot vote yet"
                                                                            # Class inheritance
                                                                            class Student extends Person {
                                                                            def __init__(self, name, age, grade):
                                                                                super(name, age)
                                                                                self.grade = grade
                                                                                def study(self):
                                                                                    print(self.str(name) + " is studying in grade " + str(self).grade)
                                                                                    def greet(self):
                                                                                        print("Hi, I'm " + self.name + ", a student in grade " + str(self).grade)
                                                                                        # Create objects
                                                                                        person = Person("Rohit", 25)
                                                                                        person.greet()
                                                                                        print(person.canVote())
                                                                                        student = Student("Aman", 16, 10)
                                                                                        student.greet()
                                                                                        student.study()
                                                                                        print(student.canVote())