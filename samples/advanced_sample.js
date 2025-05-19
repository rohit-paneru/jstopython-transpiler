// Advanced JavaScript code sample
// This file contains various JavaScript constructs to test the converter

// Basic console output
console.log("JavaScript to Python Converter Demo");

// Variable declarations and operations
let name = "Rohit";
const age = 25;
var isStudent = true;
let greeting = "Hello, " + name + "!";
console.log(greeting);

// Numeric operations
let a = 10;
let b = 20;
let sum = a + b;
let difference = b - a;
let product = a * b;
let quotient = b / a;
console.log("Sum: " + sum);
console.log("Difference: " + difference);
console.log("Product: " + product);
console.log("Quotient: " + quotient);

// For loop with different variations
console.log("Counting from 0 to 4:");
for (let i = 0; i < 5; i++) {
  console.log("Count: " + i);
}

// For loop with different increment
console.log("Counting by 2:");
for (let i = 0; i <= 10; i += 2) {
  console.log("Count: " + i);
}

// While loop
console.log("Countdown from 3:");
let count = 3;
while (count >= 0) {
  console.log("Countdown: " + count);
  count--;
}

// Nested conditional statements
let userAge = 20;
let hasLicense = true;

if (userAge >= 18) {
  console.log("You are an adult");

  if (hasLicense) {
    console.log("You can drive");
  } else {
    console.log("You need to get a license to drive");
  }
} else {
  console.log("You are a minor");
  console.log("You cannot drive yet");
}

// Function definition with return value
function calculateSum(a, b) {
  return a + b;
}

// Function with conditional logic
function checkEligibility(age, hasExperience) {
  if (age >= 18 && hasExperience) {
    return "Eligible";
  } else if (age >= 18) {
    return "Partially eligible";
  } else {
    return "Not eligible";
  }
}

// Function calls
let result = calculateSum(5, 10);
console.log("Sum: " + result);

let eligibility = checkEligibility(25, true);
console.log("Eligibility status: " + eligibility);

// Array operations
let fruits = ["apple", "banana", "orange", "grape", "mango"];
console.log("First fruit: " + fruits[0]);
console.log("Last fruit: " + fruits[fruits.length - 1]);
console.log("Number of fruits: " + fruits.length);

// Array iteration
console.log("All fruits:");
for (let i = 0; i < fruits.length; i++) {
  console.log(i + 1 + ". " + fruits[i]);
}

// Simple class with methods
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
    this.isAdult = age >= 18;
  }

  greet() {
    console.log(
      "Hello, my name is " + this.name + " and I am " + this.age + " years old."
    );
  }

  canVote() {
    if (this.isAdult) {
      return this.name + " can vote";
    } else {
      return this.name + " cannot vote yet";
    }
  }
}

// Class inheritance
class Student extends Person {
  constructor(name, age, grade) {
    super(name, age);
    this.grade = grade;
  }

  study() {
    console.log(this.name + " is studying in grade " + this.grade);
  }

  greet() {
    console.log("Hi, I'm " + this.name + ", a student in grade " + this.grade);
  }
}

// Create objects
let person = new Person("Rohit", 25);
person.greet();
console.log(person.canVote());

let student = new Student("Aman", 16, 10);
student.greet();
student.study();
console.log(student.canVote());
