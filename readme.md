# jstopython-transpiler: JavaScript to Python Transpiler

## Overview

_\*\*jstopython-transpiler_\*\* is a tool that converts JavaScript code to Python code. It features a web-based user interface powered by a Python Flask server, allowing users to easily input JavaScript code and receive Python translations in real-time.

---

## Features

- **JavaScript to Python Conversion:** Transpile JavaScript code into Python automatically 
- **Web UI:** Clean, responsive interface for entering code and viewing results
- **Real-time Conversion:** Instantly see Python output as you write JavaScript
- **AST-based Transformation:** Uses Babel parser to create accurate Abstract Syntax Tree transformations
- **Easy to Run:** Start the server with a single batch file (`start_ui.bat`)
- **Keyboard Shortcuts:** Use Ctrl+Enter to quickly transpile code

---

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (Required for JavaScript parsing)
- [Flask](https://flask.palletsprojects.com/) (`pip install flask`)

### Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/rohit-paneru/jstopython-transpiler
   cd jstopython-transpilerython-transpiler
   ```

2. **Install Python dependencies:**

   ```bash
   pip install flask
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   This will install the required `@babel/parser` package.

---

## Usage

1. **Start the Web UI:**

   - Double-click `start_ui.bat`  
     _or_
   - Run in terminal:
     ```bash
     start_ui.bat
     ```

2. **Open your browser and go to:**  
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

3. **Enter JavaScript code** in the left panel and click "Transpile" (or press Ctrl+Enter)

4. **View the Python output** in the right panel

5. **Copy the Python code** using the "Copy Python" button

---

## How It Works

1. The Flask server (`server.py`) provides the web interface
2. JavaScript code is sent to the server via API
3. The server uses `parser.js` (with Babel) to generate an AST of the JavaScript code
4. The Python converter (`js2py_converter.py`) transforms the AST into equivalent Python code
5. The converted Python code is returned to the web UI

---

## Project Structure

```
jstopython-transpiler/
│
├── server.py                    # Flask server for the web UI
├── start_ui.bat                 # Batch file to start the Flask server
├── parser.js                    # Node.js script for JavaScript parsing
├── package.json                 # Node.js dependencies
├── converters/                  # Python conversion modules
│   └── js2py_converter.py       # JavaScript to Python transformer
├── templates/                   # HTML templates
│   └── index.html               # Main web interface
├── static/                      # Static assets
│   ├── styles.css               # CSS styles
│   └── scripts.js               # Client-side JavaScript
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

---

## Supported JavaScript Features

The transpiler currently supports:

- Variables and constants
- Basic data types (strings, numbers, booleans, null)
- Arrays and objects
- Functions and arrow functions
- Control structures (if/else, loops)
- Console.log statements
- Math operations
- Template literals
- And more!

---

## Notes

- The transpiler is a demonstration tool and may not handle all JavaScript features or edge cases.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Author

- [Rohit Paneru](https://github.com/rohit-paneru)
- karan andola
- 
