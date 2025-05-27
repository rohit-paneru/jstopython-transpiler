// scripts.js
document.addEventListener("DOMContentLoaded", () => {
  const jsInput = document.getElementById("js-input");
  const pythonOutput = document.getElementById("python-output");
  const transpileBtn = document.getElementById("transpile-btn");
  const clearJsBtn = document.getElementById("clear-js-btn");
  const copyPyBtn = document.getElementById("copy-py-btn");
  const statusMessage = document.getElementById("status-message");

  //  initial example JavaScript in the input area
  jsInput.value = `// Example JavaScript
let myVariable = 42;
const greeting = \`Hello, \${'World'}!\`; // Template literal
console.log(greeting);
console.log(Math.floor(myVariable / 2));

function calculateSum(a, b) {
  let result = a + b;
  if (result > 50) {
    console.log('Sum is greater than 50');
  } else if (result === 50) {
    console.log('Sum is exactly 50');
  } else {
    console.log('Sum is less than 50');
  }
  return result;
}

let total = calculateSum(myVariable, 10);
console.log(\`Total sum: \${total}\`);

const simpleArrow = (x) => x * 2;
console.log(simpleArrow(5));

if (true && (myVariable < 100 || false)) {
    console.log('Complex condition met');
}
`;

  async function handleTranspile() {
    const jsCode = jsInput.value;
    if (!jsCode.trim()) {
      statusMessage.textContent =
        "JavaScript input is empty. Nothing to transpile.";
      statusMessage.className = "error";
      pythonOutput.value = "";
      return;
    }

    statusMessage.textContent = "Transpiling... Please wait.";
    statusMessage.className = "processing";
    transpileBtn.disabled = true;
    pythonOutput.value = ""; // Clear previous output

    try {
      console.log(
        "Frontend: Sending request to /transpile with JS code:",
        jsCode.substring(0, 100) + "..."
      );
      const response = await fetch("/transpile", {
        // Relative path to our Flask backend
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ js_code: jsCode }),
      });

      console.log(
        "Frontend: Received response from /transpile. Status:",
        response.status
      );

      // Try to get text first for debugging if it's not JSON
      const responseText = await response.text();
      console.log(
        "Frontend: Response text from /transpile:",
        responseText.substring(0, 500) + "..."
      );

      if (!response.ok && response.status !== 200) {
        // Handle HTTP errors (like 500, 400 from request validation if not JSON response)
        throw new Error(
          `Server responded with status: ${response.status}. Response body: ${responseText}`
        );
      }

      // Now parse the text as JSON
      const data = JSON.parse(responseText);
      console.log("Frontend: Parsed JSON data from /transpile:", data);

      if (data.error) {
        pythonOutput.value = `# --- TRANSPILATION ERROR --- \n${data.error}`;
        statusMessage.textContent = `Error: ${data.error.split("\n")[0]}`; // Show first line
        statusMessage.className = "error";
      } else if (data.python_code !== undefined) {
        // Check for python_code existence
        pythonOutput.value = data.python_code;
        statusMessage.textContent = "Transpilation successful!";
        statusMessage.className = "success";
      } else {
        pythonOutput.value = `# --- UNEXPECTED RESPONSE --- \nReceived unexpected data structure from server.`;
        statusMessage.textContent = "Error: Unexpected response from server.";
        statusMessage.className = "error";
      }
    } catch (error) {
      console.error("Frontend: Fetch or JSON parsing error:", error);
      pythonOutput.value = `# --- CLIENT-SIDE OR NETWORK ERROR --- \n${error.message}\nCheck browser console and server logs.`;
      statusMessage.textContent = `Error: ${error.message.split("\n")[0]}`;
      statusMessage.className = "error";
    } finally {
      transpileBtn.disabled = false;
    }
  }

  transpileBtn.addEventListener("click", handleTranspile);

  // Ctrl+Enter or Cmd+Enter in textarea to transpile
  jsInput.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault(); // Prevent newline
      handleTranspile();
    }
  });

  clearJsBtn.addEventListener("click", () => {
    jsInput.value = "";
    pythonOutput.value = "";
    statusMessage.textContent = "JavaScript input cleared. Ready.";
    statusMessage.className = ""; // Reset class
    jsInput.focus();
  });

  copyPyBtn.addEventListener("click", async () => {
    if (!pythonOutput.value.trim() || pythonOutput.value.startsWith("# ---")) {
      statusMessage.textContent = "Nothing valid to copy from Python output.";
      statusMessage.className = "error";
      return;
    }
    try {
      await navigator.clipboard.writeText(pythonOutput.value);
      statusMessage.textContent = "Python output copied to clipboard!";
      statusMessage.className = "success";
    } catch (err) {
      console.error("Frontend: Failed to copy text to clipboard:", err);
      statusMessage.textContent =
        "Failed to copy Python output. Try manual selection and copy.";
      statusMessage.className = "error";
    }
  });
});
