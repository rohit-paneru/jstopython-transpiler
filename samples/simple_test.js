// Simple JavaScript test file
console.log("Testing simple JavaScript constructs");

// Variable declarations
let name = "Rohit";
const age = 25;
var isStudent = true;

// Variable reassignment
name = "John";

// String concatenation
console.log("Hello, " + name + "! You are " + age + " years old.");

// Simple arithmetic
let a = 10;
let b = 20;
let sum = a + b;
console.log("Sum: " + sum);

// For loop with empty body
for (let i = 0; i < 5; i++) {}

// For loop with body
for (let i = 0; i < 3; i++) {
  console.log("Iteration: " + i);
}

// For loop with different increment
for (let i = 0; i <= 10; i += 2) {
  console.log("Even number: " + i);
}

// While loop
let count = 3;
while (count > 0) {
  console.log("Count: " + count);
  count--;
}

// If-else statement
if (age >= 18) {
  console.log("You are an adult");
} else {
  console.log("You are a minor");
}

// Nested if-else
if (age >= 18) {
  if (age >= 65) {
    console.log("You are a senior citizen");
  } else {
    console.log("You are an adult, but not a senior citizen");
  }
} else {
  console.log("You are a minor");
}

// Function declaration
function greet(name) {
  return "Hello, " + name + "!";
}

// Function call
let greeting = greet(name);
console.log(greeting);

// Array operations
let fruits = ["apple", "banana", "orange"];
console.log("First fruit: " + fruits[0]);
console.log("Number of fruits: " + fruits.length);

// Simple object
let person = {
  name: "Rohit",
  age: 25,
  greet: function () {
    console.log("Hello, my name is " + this.name);
  },
};

// Method call
person.greet();
