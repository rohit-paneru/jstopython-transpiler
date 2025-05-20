# JSTOP: JavaScript to Python Transpiler

## Overview

**JSTOP** is a tool that converts JavaScript code to Python code. It features a web-based user interface powered by a Python Flask server, allowing users to easily upload JavaScript files and receive Python translations.

---

## Features

- **JavaScript to Python Conversion:** Transpile JavaScript code into Python automatically.
- **Web UI:** Simple web interface for uploading files and viewing results.
- **Easy to Run:** Start the server with a single batch file (`start_ui.bat`).

---

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/) (`pip install flask`)
- (Optional) [Node.js](https://nodejs.org/) if you want to work with JavaScript tools

### Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/rohit-paneru/jstopython-transpiler
   cd jstopython-transpiler
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask
   ```

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

3. **Upload your JavaScript file** and get the Python output.

---

## Project Structure

```
jstop/
│
├── start_ui.bat           # Batch file to start the Flask server
├── server.py              # Flask server for the web UI
├── final_solution.cpp     # (Example) C++ transpiler implementation
├── sample.js              # Sample JavaScript file
├── output.py              # Output Python file (after conversion)
├── .gitignore             # Git ignore file (should include node_modules/)
└── README.md              # Project documentation
```

---

## Notes

- Do **not** commit `node_modules/` or other generated files to Git. Use `.gitignore`.
- The main logic for conversion may be in `final_solution.cpp` or `server.py` depending on your setup.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Author

- [Rohit Paneru](https://github.com/rohit-paneru)
