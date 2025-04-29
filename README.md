# JavaScript to Python Converter

A C++ program that converts JavaScript code to Python code.

## Files in this Project

- **final_solution.cpp** - The primary converter implementation
- **final_version.cpp** - A simplified converter specifically designed for the sample file
- **sample.js** - A sample JavaScript file to test the converter
- **how_js2py_works.txt** - Documentation explaining how the converter works
- **Makefile** - Compilation instructions for the project

## How to Build

To build the converter, run:

```bash
make
```

Or manually compile with:

```bash
g++ -std=c++17 -Wall -Wextra -pedantic -o js2py final_solution.cpp
```

## How to Use

1. Build the converter as described above
2. Run the converter on a JavaScript file:

```bash
./js2py sample.js output.py
```

3. View the resulting Python file:

```bash
cat output.py
```

## Features

This JavaScript to Python converter handles:

- Variable declarations
- Function definitions
- Class definitions
- Loops (for, while)
- Conditionals (if/else)
- Console.log statements
- Basic string operations
- Arrays and basic operations

## Limitations

The converter has some limitations:

- Complex JavaScript constructs might not convert correctly
- Arrow functions are not fully supported
- Some JavaScript-specific features have no direct Python equivalent
- Manual adjustments might be needed for certain code patterns

## Documentation

For a complete explanation of how the converter works, refer to `how_js2py_works.txt`.

## Future Improvements

Potential enhancements include:

- Better handling of modern JavaScript features
- Support for JavaScript frameworks and libraries
- AST-based parsing for more accurate conversion
- Interactive mode for handling ambiguous conversions
- Web interface for easy online conversion

## License

This project is open source and available for educational purposes.
