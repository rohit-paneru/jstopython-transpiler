// parser.js
const babelParser = require("@babel/parser");

// Optional: Initial log to stderr to see if script even starts
// console.error(`--- [NODE_PARSER] parser.js started. PID: ${process.pid} ---`);

let jsCode = "";
process.stdin.setEncoding("utf8");

process.stdin.on("readable", () => {
  let chunk;
  while ((chunk = process.stdin.read()) !== null) {
    jsCode += chunk;
  }
});

process.stdin.on("end", () => {
  const logJsCode =
    jsCode.length > 100 ? jsCode.substring(0, 100) + "..." : jsCode;
  // console.error(`--- [NODE_PARSER] stdin 'end' event. Received JS code (first 100 chars): '${logJsCode}' ---`);
  try {
    const ast = babelParser.parse(jsCode, {
      sourceType: "module", // Recommended for modern JS
      plugins: [
        // Add any Babel plugins you need here if you extend JS syntax support
        // e.g., "jsx", "typescript"
      ],
      errorRecovery: true, // IMPORTANT: Allows Babel to parse even with some errors and list them
    });
    // console.error("--- [NODE_PARSER] Babel parsing successful. AST generated. Writing to stdout. ---");
    // Output AST as JSON to stdout for Python to consume
    process.stdout.write(JSON.stringify(ast, null, 2));
  } catch (error) {
    // This catch block is for errors thrown by babelParser.parse itself
    // console.error("--- [NODE_PARSER] EXCEPTION during babelParser.parse(). Formatting error for stderr. ---");
    // console.error(`--- [NODE_PARSER] Babel Error Message: ${error.message} ---`);
    const errorOutput = {
      error: "BabelParserException", // Custom type for easier identification by Python
      message: error.message,
      loc: error.loc, // Location information {line, column}
      description: error.description, // Babel specific
      stack: error.stack, // Include stack if available
    };
    process.stderr.write(JSON.stringify(errorOutput, null, 2));
    process.exit(1); // Indicate failure to the calling Python process
  }
});

// Catch other unexpected errors in the Node.js script itself
process.on("uncaughtException", (err, origin) => {
  // console.error(`--- [NODE_PARSER] UNCAUGHT EXCEPTION in parser.js. Origin: ${origin} ---`);
  // console.error(`--- [NODE_PARSER] Error Name: ${err.name}, Message: ${err.message} ---`);
  // console.error(`--- [NODE_PARSER] Stack: ${err.stack} ---`);
  const errorOutput = {
    error: "NodeScriptUncaughtException",
    message: err.message,
    name: err.name,
    origin: origin,
    stack: err.stack,
  };
  try {
    process.stderr.write(JSON.stringify(errorOutput, null, 2)); // Try to send JSON error
  } catch (e) {
    process.stderr.write(
      `Uncaught Node Exception (could not stringify): ${err.message}`
    );
  }
  process.exit(1); // Indicate failure
});

// console.error("--- [NODE_PARSER] Script setup complete. Waiting for stdin data. ---");
