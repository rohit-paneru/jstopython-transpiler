# JavaScript to Python Converter

A tool that converts JavaScript code to Python code, with both C++ and Python implementations.

## Project Structure

### Directories

- **converters/** - Contains all the converter implementations
- **samples/** - Contains sample JavaScript files for testing
- **output/** - Where converted Python files are stored
- **docs/** - Documentation and source code for reference

### Core Files

- **converters/basic_js2py.py** - Simple Python converter for basic JavaScript code
- **converters/js2py_improved.py** - Enhanced Python converter with better indentation handling
- **converters/js2py_converter.py** - Original Python implementation of the converter
- **converters/final_js2py.exe** - The compiled C++ converter executable (fallback option)

### Web Interface

- **index.html** - Web interface for the converter
- **script.js** - JavaScript code for the web interface
- **styles.css** - Styling for the web interface
- **server.py** - Python HTTP server that handles conversion requests
- **start_ui.bat** - Batch file to start the Python server

### Utility Scripts

- **test_converters.bat** - Script to test and compare all converters
- **check_environment.bat** - Script to verify your environment setup

## How to Use

### Web Interface (Recommended)

1. Start the Python server by running `start_ui.bat`
2. Open your web browser and navigate to `http://localhost:8000`
3. Enter your JavaScript code in the left text area
4. Click the "Convert" button
5. The converted Python code will appear in the right text area

The web interface supports two conversion modes:

- **Server-side:** Uses Python converters (when server is running)
- **Client-side:** Uses JavaScript converter (automatic fallback)

### Command Line Options

You can also use the converters directly from the command line:

#### Basic Python Converter (Best for Simple Code)

```bash
python converters/basic_js2py.py input.js output.py
```

#### Improved Python Converter (For More Complex Code)

```bash
python converters/js2py_improved.py input.js output.py
```

#### Original Python Converter

```bash
python converters/js2py_converter.py input.js output.py
```

#### C++ Converter (Fallback Option)

```bash
converters/final_js2py.exe input.js output.py
```

You can also use the test batch file to compare all converters:

```bash
test_converters.bat
```

## Features

This JavaScript to Python converter handles:

- Variable declarations
- Function definitions
- Class definitions
- Loops (for, while)
- Conditionals (if/else)
- Console.log statements
- String operations and concatenation
- Arrays and basic operations
- Object-oriented programming constructs

## Conversion Examples

### JavaScript:

```javascript
// Sample JavaScript code
console.log("JavaScript to Python Converter Demo");

// Variable declaration and reassignment
let name = "Rohit";
let greeting = "Hello, " + name + "!";
console.log(greeting);

// For loop
console.log("Counting from 0 to 4:");
for (let i = 0; i < 5; i++) {
  console.log("Count: " + i);
}
```

### Python:

```python
# Sample JavaScript code
print("JavaScript to Python Converter Demo")

# Variable declaration and reassignment
name = "Rohit"
greeting = "Hello, " + str(name) + "!"
print(greeting)

# For loop
print("Counting from 0 to 4:")
for i in range(0, 5, 1):
    print("Count: " + str(i))
```

## Limitations

The converter has some limitations:

- Complex JavaScript constructs might not convert perfectly
- Arrow functions are not fully supported
- Some JavaScript-specific features have no direct Python equivalent
- Manual adjustments might be needed for certain code patterns

## Future Improvements

Potential enhancements include:

- Better handling of modern JavaScript features
- Support for JavaScript frameworks and libraries
- AST-based parsing for more accurate conversion
- Interactive mode for handling ambiguous conversions
- Enhanced web interface with more options

## Troubleshooting

### Common Issues

1. **"Failed to run converter. Server might not be running."**

   - Make sure you've started the Python server using `start_ui.bat`
   - Check that port 8000 is not being used by another application
   - Ensure Python is installed and in your PATH

2. **Conversion produces unexpected results**

   - Try a different converter (basic, improved, or original)
   - Check if your JavaScript code uses unsupported features
   - Manually adjust the Python code as needed

3. **Server won't start**
   - Ensure Python is installed correctly
   - Check for any error messages in the command window
   - Try running the converter directly from the command line

You can run `check_environment.bat` to verify that your system has all the required components installed and configured correctly.

## License

This project is open source and available for educational purposes.
