document.addEventListener("DOMContentLoaded", function () {
  // Get DOM elements
  const jsCodeTextarea = document.getElementById("js-code");
  const pyCodeTextarea = document.getElementById("py-code");
  const convertBtn = document.getElementById("convert-btn");
  const clearBtn = document.getElementById("clear-btn");
  const copyBtn = document.getElementById("copy-btn");
  const downloadBtn = document.getElementById("download-btn");
  const statusMessage = document.getElementById("status-message");
  const conversionInfo = document.getElementById("conversion-info");

  // Sample JavaScript code for demonstration
  const sampleJsCode = `// Sample JavaScript code
function calculateSum(numbers) {
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
    }
    return sum;
}

class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        console.log("Hello, my name is " + this.name + " and I am " + this.age + " years old.");
    }
}

const numbers = [1, 2, 3, 4, 5];
const total = calculateSum(numbers);
console.log("The sum is: " + total);

const person = new Person("John", 30);
person.greet();`;

  // Set sample code
  jsCodeTextarea.value = sampleJsCode;

  // Convert button click handler
  convertBtn.addEventListener("click", function () {
    const jsCode = jsCodeTextarea.value.trim();

    if (!jsCode) {
      setStatus("Please enter some JavaScript code.", "error");
      return;
    }

    setStatus("Converting...", "");

    // Call the conversion function
    convertJsToPy(jsCode);
  });

  // Clear button click handler
  clearBtn.addEventListener("click", function () {
    jsCodeTextarea.value = "";
    pyCodeTextarea.value = "";
    setStatus("", "");
    conversionInfo.textContent = "";
  });

  // Copy button click handler
  copyBtn.addEventListener("click", function () {
    if (!pyCodeTextarea.value) {
      setStatus("No Python code to copy.", "error");
      return;
    }

    pyCodeTextarea.select();
    document.execCommand("copy");
    setStatus("Python code copied to clipboard!", "success");
  });

  // Download button click handler
  downloadBtn.addEventListener("click", function () {
    if (!pyCodeTextarea.value) {
      setStatus("No Python code to download.", "error");
      return;
    }

    const blob = new Blob([pyCodeTextarea.value], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "converted_code.py";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    setStatus("Python file downloaded!", "success");
  });

  // Function to set status message
  function setStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = type;
  }

  // Function to convert JS to Python using the existing converter
  function convertJsToPy(jsCode) {
    // First try server-side conversion
    serverSideConversion(jsCode, function (error, pythonCode) {
      if (!error && pythonCode) {
        // Server-side conversion succeeded
        pyCodeTextarea.value = pythonCode;
        setStatus("Conversion complete!", "success");
        conversionInfo.textContent = "Server-side conversion";
      } else {
        // Server-side conversion failed, use client-side fallback
        const clientSidePythonCode = clientSideConverter(jsCode);
        pyCodeTextarea.value = clientSidePythonCode;
        setStatus("Conversion complete!", "success");
        conversionInfo.textContent = "Client-side conversion";
      }
    });
  }

  // Function to attempt server-side conversion
  function serverSideConversion(jsCode, callback) {
    // Save the JavaScript code to sample.js
    saveToFile(jsCode, "sample.js", function (error) {
      if (error) {
        callback(error);
        return;
      }

      // Run the converter using the fetch API
      runConverter(function (error) {
        if (error) {
          callback(error);
          return;
        }

        // Read the output.py file
        readOutputFile(function (error, pythonCode) {
          if (error) {
            callback(error);
            return;
          }

          // Return the Python code
          callback(null, pythonCode);
        });
      });
    });
  }

  // Client-side JavaScript to Python converter (fallback)
  function clientSideConverter(jsCode) {
    // Simple JavaScript to Python converter
    let pyCode = "";

    // No comment header needed

    // Process the JavaScript code line by line
    const lines = jsCode.split("\n");
    let indentLevel = 0;
    let inClass = false;
    let inFunction = false;

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim();

      // Skip empty lines
      if (line === "") {
        pyCode += "\n";
        continue;
      }

      // Convert comments
      if (line.startsWith("//")) {
        pyCode += "# " + line.substring(2) + "\n";
        continue;
      }

      // Convert console.log
      if (line.includes("console.log(")) {
        line = line.replace("console.log(", "print(");
        // Handle string concatenation
        line = line.replace(/ \+ /g, " + str(");
        // Add closing parentheses for str() calls
        const openParens = (line.match(/str\(/g) || []).length;
        const closeParens = line.split(")").length - 1;
        for (let j = 0; j < openParens; j++) {
          // Insert before the last )
          line =
            line.substring(0, line.lastIndexOf(")")) +
            ")" +
            line.substring(line.lastIndexOf(")"));
        }
        pyCode += "    ".repeat(indentLevel) + line + "\n";
        continue;
      }

      // Convert variable declarations
      if (
        line.startsWith("let ") ||
        line.startsWith("var ") ||
        line.startsWith("const ")
      ) {
        const parts = line.split("=");
        const varName = parts[0].replace(/let |var |const /g, "").trim();
        let value = parts.length > 1 ? parts.slice(1).join("=").trim() : "";

        // Remove semicolon if present
        if (value.endsWith(";")) {
          value = value.substring(0, value.length - 1);
        }

        pyCode += "    ".repeat(indentLevel) + varName + " = " + value + "\n";
        continue;
      }

      // Convert for loops
      if (line.startsWith("for (")) {
        // Extract loop parts
        const loopParts = line.substring(4, line.indexOf(")")).split(";");
        if (loopParts.length === 3) {
          const init = loopParts[0].trim();
          const condition = loopParts[1].trim();
          const increment = loopParts[2].trim();

          // Extract variable name and initial value
          const varName = init
            .split("=")[0]
            .replace(/let |var |const /g, "")
            .trim();
          const startValue = init.split("=")[1].trim();

          // Extract end condition
          let endValue = "";
          if (condition.includes("<")) {
            endValue = condition.split("<")[1].trim();
          } else if (condition.includes("<=")) {
            endValue = condition.split("<=")[1].trim() + " + 1";
          }

          // Extract step value
          let step = "1";
          if (increment.includes("++")) {
            step = "1";
          } else if (increment.includes("--")) {
            step = "-1";
          } else if (increment.includes("+=")) {
            step = increment.split("+=")[1].trim();
          } else if (increment.includes("-=")) {
            step = "-" + increment.split("-=")[1].trim();
          }

          pyCode +=
            "    ".repeat(indentLevel) +
            `for ${varName} in range(${startValue}, ${endValue}, ${step}):\n`;
          indentLevel++;
        }
        continue;
      }

      // Convert function declarations
      if (line.startsWith("function ")) {
        const funcName = line.substring(9, line.indexOf("("));
        const params = line.substring(line.indexOf("(") + 1, line.indexOf(")"));

        pyCode += "    ".repeat(indentLevel) + `def ${funcName}(${params}):\n`;
        indentLevel++;
        inFunction = true;
        continue;
      }

      // Convert class declarations
      if (line.startsWith("class ")) {
        const className = line.substring(6, line.indexOf("{")).trim();

        pyCode += "    ".repeat(indentLevel) + `class ${className}:\n`;
        indentLevel++;
        inClass = true;
        continue;
      }

      // Convert constructor
      if (line.startsWith("constructor(")) {
        const params = line.substring(line.indexOf("(") + 1, line.indexOf(")"));

        pyCode +=
          "    ".repeat(indentLevel) + `def __init__(self, ${params}):\n`;
        indentLevel++;
        continue;
      }

      // Convert class methods
      if (
        inClass &&
        line.includes("(") &&
        line.includes(")") &&
        line.includes("{") &&
        !line.startsWith("if") &&
        !line.startsWith("for")
      ) {
        const methodName = line.substring(0, line.indexOf("(")).trim();
        let params = line.substring(line.indexOf("(") + 1, line.indexOf(")"));

        if (params.trim() !== "") {
          params = "self, " + params;
        } else {
          params = "self";
        }

        pyCode +=
          "    ".repeat(indentLevel) + `def ${methodName}(${params}):\n`;
        indentLevel++;
        continue;
      }

      // Convert if statements
      if (line.startsWith("if (")) {
        const condition = line.substring(4, line.indexOf(")"));

        pyCode += "    ".repeat(indentLevel) + `if ${condition}:\n`;
        indentLevel++;
        continue;
      }

      // Convert else if statements
      if (line.startsWith("else if (") || line.startsWith("} else if (")) {
        const condition = line.substring(
          line.indexOf("if (") + 4,
          line.indexOf(")")
        );

        pyCode += "    ".repeat(indentLevel - 1) + `elif ${condition}:\n`;
        continue;
      }

      // Convert else statements
      if (line === "else {" || line === "} else {") {
        pyCode += "    ".repeat(indentLevel - 1) + "else:\n";
        continue;
      }

      // Handle closing braces
      if (line === "}") {
        indentLevel = Math.max(0, indentLevel - 1);
        continue;
      }

      // Convert return statements
      if (line.startsWith("return ")) {
        const returnValue = line.substring(7).replace(";", "");

        pyCode += "    ".repeat(indentLevel) + `return ${returnValue}\n`;
        continue;
      }

      // Handle this references in classes
      if (inClass && line.includes("this.")) {
        line = line.replace(/this\./g, "self.");

        // Remove semicolon if present
        if (line.endsWith(";")) {
          line = line.substring(0, line.length - 1);
        }

        pyCode += "    ".repeat(indentLevel) + line + "\n";
        continue;
      }

      // Handle other lines
      if (!line.startsWith("{") && !line.startsWith("}")) {
        // Remove semicolon if present
        if (line.endsWith(";")) {
          line = line.substring(0, line.length - 1);
        }

        pyCode += "    ".repeat(indentLevel) + line + "\n";
      }
    }

    return pyCode;
  }

  // Function to save JavaScript code to a file
  function saveToFile(content, filename, callback) {
    // Use the Python endpoint to save the file
    tryPythonSave(content, function (error) {
      if (!error) {
        callback(null);
        return;
      }

      // Failed to save
      callback("Failed to save JavaScript code. Server might not be running.");
    });
  }

  // Try to save using Python endpoint
  function tryPythonSave(content, callback) {
    fetch("/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: content }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          callback(null);
        } else {
          callback(data.error || "Unknown error");
        }
      })
      .catch((error) => {
        console.error("Python Save Error:", error);
        callback(error.message);
      });
  }

  // Function to run the converter
  function runConverter(callback) {
    // Use the Python endpoint to run the converter
    tryPythonConverter(function (error) {
      if (!error) {
        callback(null);
        return;
      }

      // Failed to convert
      callback("Failed to run converter. Server might not be running.");
    });
  }

  // Try to convert using Python endpoint
  function tryPythonConverter(callback) {
    fetch("/convert")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          callback(null);
        } else {
          callback(data.error || "Unknown error");
        }
      })
      .catch((error) => {
        console.error("Python Convert Error:", error);
        callback(error.message);
      });
  }

  // Function to read the output file
  function readOutputFile(callback) {
    // Try the direct file access first
    tryDirectFileAccess(function (error, data) {
      if (!error) {
        callback(null, data);
        return;
      }

      // If direct access fails, try the Python endpoint
      tryPythonGetOutput(function (error, data) {
        if (!error) {
          callback(null, data);
          return;
        }

        // Both methods failed
        callback("Failed to read output file. Server might not be running.");
      });
    });
  }

  // Try to read file directly
  function tryDirectFileAccess(callback) {
    fetch("output/output.py")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to read output file: " + response.status);
        }
        return response.text();
      })
      .then((data) => {
        callback(null, data);
      })
      .catch((error) => {
        console.error("Direct File Access Error:", error);
        callback(error.message);
      });
  }

  // Try to get output using Python endpoint
  function tryPythonGetOutput(callback) {
    fetch("/getOutput")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          callback(null, data.code);
        } else {
          callback(data.error || "Unknown error");
        }
      })
      .catch((error) => {
        console.error("Python Get Output Error:", error);
        callback(error.message);
      });
  }
});
