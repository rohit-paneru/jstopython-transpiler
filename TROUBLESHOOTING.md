# Troubleshooting Guide

This guide helps you resolve common issues with the JavaScript to Python Converter.

## Web Interface Issues

### Server Won't Start

If `start_ui.bat` fails to start:

1. **Check if Python is installed**:

   - Open a command prompt and type `python --version`
   - If you get "command not found" or similar, Python is not installed or not in your PATH

2. **Install Python**:

   - Download Python from [python.org/downloads](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

3. **Check port availability**:
   - Make sure port 8000 is not being used by another application
   - You can change the port in server.py if needed

### Conversion Fails

If the conversion process fails:

1. **Check the JavaScript code**:

   - Make sure your JavaScript code is valid
   - Start with simple examples and gradually add complexity

2. **Try different converters**:

   - Use the command-line converters directly:
     ```
     python converters/js2py_improved.py samples/sample.js output/output.py
     ```
     or
     ```
     python converters/js2py_converter.py samples/sample.js output/output.py
     ```
     or
     ```
     converters/final_js2py.exe samples/sample.js output/output.py
     ```

3. **Use the client-side conversion**:

   - The web interface automatically uses client-side conversion when the server is unavailable
   - Works without the server running

4. **Check for specific JavaScript features**:
   - Some advanced JavaScript features may not convert properly
   - Simplify your code if possible

## Command Line Issues

### Python Converter Issues

If the Python converters fail:

1. **Check Python installation**:

   - Make sure Python 3.6 or higher is installed
   - Check that required modules are available

2. **Check file permissions**:

   - Make sure you have read/write permissions for the current directory

3. **Try the C++ converter**:
   - Use `final_js2py.exe sample.js output.py` as an alternative

### C++ Converter Issues

If the C++ converter fails:

1. **Check if the executable exists**:

   - Make sure `final_js2py.exe` is in the current directory

2. **Rebuild the executable**:

   - If you have a C++ compiler, rebuild using:
     ```
     g++ -std=c++17 -Wall -Wextra -pedantic -o final_js2py final_solution.cpp
     ```

3. **Try the Python converters**:
   - Use the Python converters as alternatives

## Common Conversion Limitations

The converter has some known limitations:

1. **Arrow functions** may not convert correctly
2. **Promises and async/await** are not fully supported
3. **JavaScript-specific features** like prototypes have no direct Python equivalent
4. **Complex object manipulations** might need manual adjustments
5. **DOM manipulation** code won't work in Python

## Getting Help

If you continue to experience issues:

1. Check the README.md file for usage instructions
2. Examine the sample.js and output.py files for examples
3. Try the test_converters.bat script to compare different converters
4. Modify the converter code to better handle your specific use case
