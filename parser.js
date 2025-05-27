const babelParser = require("@babel/parser");

let jsCode = "";
process.stdin.setEncoding("utf8");

process.stdin.on("readable", () => {
  let chunk;
  while ((chunk = process.stdin.read()) !== null) {
    jsCode += chunk;
  }
});

process.stdin.on("end", () => {
  if (!jsCode.trim()) {
    process.stderr.write(
      JSON.stringify(
        {
          error: "EmptyInputError",
          message: "No JavaScript code was provided to parse.",
        },
        null,
        2
      )
    );
    process.exit(1);
  }

  try {
    const ast = babelParser.parse(jsCode, {
      sourceType: "module",
      plugins: [
        "classProperties",
        "classPrivateProperties",
        "classPrivateMethods",
        "dynamicImport",
        "exportDefaultFrom",
        "exportNamespaceFrom",
        "logicalAssignment",
        "optionalChaining",
        "nullishCoalescingOperator",
        "topLevelAwait",
        "asyncGenerators",
        "objectRestSpread",
        "throwExpressions",
        "numericSeparator",
        "importMeta",
        "optionalCatchBinding",
        "bigInt",
        "doExpressions",
      ],
      errorRecovery: true,
    });

    process.stdout.write(JSON.stringify(ast, null, 2));
  } catch (error) {
    process.stderr.write(
      JSON.stringify(
        {
          error: "BabelParserException",
          message: error.message,
          loc: error.loc,
          description: error.description,
          stack: error.stack,
        },
        null,
        2
      )
    );
    process.exit(1);
  }
});

process.on("uncaughtException", (err, origin) => {
  const errorOutput = {
    error: "NodeScriptUncaughtException",
    message: err.message,
    name: err.name,
    origin: origin,
    stack: err.stack,
  };
  try {
    process.stderr.write(JSON.stringify(errorOutput, null, 2));
  } catch (e) {
    process.stderr.write(
      `Uncaught Node Exception (could not stringify): ${err.message}`
    );
  }
  process.exit(1);
});
