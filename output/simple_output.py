# Simple JavaScript test file
print("Testing simple JavaScript constructs")
# Variable declarations
name = "Rohit"
age = 25
isStudent = true
# Variable reassignment
name = "John"
# String concatenation
print("Hello, " + str(name) + "! You are " + str(age) + " years old.")
# Simple arithmetic
a = 10
b = 20
sum = a + b
print("Sum: " + str(sum))
# For loop with empty body
for i in range(0, 5, 1):
    # For loop with body
    for i in range(0, 3, 1):
        print("Iteration: " + str(i))
    # For loop with different increment
    for i in range(0, 11, 2):
        print("Even number: " + str(i))
    # While loop
    count = 3
    while count > 0:
        print("Count: " + str(count))
        count -= 1
    # If-else statement
    if age >= 18:
        print("You are an adult")
        # Unknown block type: } else
            print("You are a minor")
        # Nested if-else
        if age >= 18:
            if age >= 65:
                print("You are a senior citizen")
                # Unknown block type: } else
                    print("You are an adult, but not a senior citizen")
                # Unknown block type: } else
                    print("You are a minor")
                # Function declaration
                def greet(name):
                    return "Hello, " + str(name) + "!"
                # Function call
                greeting = greet(name)
                print(greeting)
                # Array operations
                fruits = ["apple", "banana", "orange"]
                print("First fruit: " + str(fruits)[0])
                print("Number of fruits: " + str(fruits).length)
                # Simple object
                # Unknown block type: let person =
                    name: "Rohit",
                    age: 25,
                    def function(self):
                        print("Hello, my name is " + str(this).name)
                    ,
                
                # Method call
                person.greet()