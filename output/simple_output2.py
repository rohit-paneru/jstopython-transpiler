# Simple JavaScript test file
print("Testing simple JavaScript constructs")

# Variable declarations
name = "Rohit"
age = 25
isStudent = True

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
for (i = 0 i < 5 i += 1) {}

# For loop with body
for (i = 0 i < 3 i += 1) {
print("Iteration: " + str(i))
}

# For loop with different increment
for (i = 0 i <= 10 i += 2) {
print("Even number: " + str(i))
}

# While loop
count = 3
while count > 0:
    print("Count: " + str(count))
    count -= 1


    # If-else statement
    if age >= 18:
        print("You are an adult")
    else {
        print("You are a minor")
        }

        # Nested if-else
        if age >= 18:
            if (age >= 65) {
            print("You are a senior citizen")
        else {
            print("You are an adult, but not a senior citizen")
            }
        else:
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
                print("Number of fruits: " + str(len)(fruits))

                # Simple object
                person = {
                name: "Rohit",
                age: 25,
                greet: function () {
                print("Hello, my name is " + str(self).name)
                },
                }

                # Method call
                person.greet()
