# JavaScript to Python Converter UI

This is a web-based user interface for the JavaScript to Python converter. It allows you to easily convert JavaScript code to Python without using the command line.

## Features

- User-friendly interface
- Easy conversion of JavaScript to Python
- Copy converted code to clipboard
- Download converted code as a Python file
- Multiple converter options for best results

## How to Use

### Starting the Server

1. Make sure you have Python installed on your system
2. Double-click the `start_ui.bat` file or run it from the command prompt
3. The server will start on port 8000
4. You'll see a message confirming the server is running

### Using the Web Interface

1. Open your web browser and go to http://localhost:8000
2. Paste your JavaScript code in the left text area
3. Click the "Convert to Python" button
4. The converted Python code will appear in the right text area
5. Use the "Copy to Clipboard" or "Download as .py" buttons as needed

### Converter Options

The system uses multiple converters in the following order:

1. **Improved Python Converter** - Best for most JavaScript code
2. **Original Python Converter** - Alternative if the improved converter fails
3. **C++ Converter** - Final fallback option for complex cases

The server automatically tries these converters in sequence to provide the best conversion results.

## Technical Details

- The UI is built with HTML, CSS, and JavaScript
- The server is a simple Python HTTP server running on port 8000
- The conversion is performed by multiple Python converters with a C++ fallback
- The server handles file operations and converter selection automatically

## Limitations

- The converter has the same limitations as mentioned in the main README
- Some JavaScript features may not convert perfectly to Python
- Complex JavaScript constructs might need manual adjustments
- The server must be running for the conversion to work

## Future Improvements

- Add syntax highlighting for code areas
- Implement real-time conversion as you type
- Add options to customize the conversion process
- Create a standalone executable that includes both the UI and the converter
- Add support for converting Python back to JavaScript
- Improve handling of modern JavaScript features
