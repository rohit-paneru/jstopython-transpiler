# server.py
from flask import Flask, request, jsonify, render_template
import os
import sys

# --- Print CWD and script path information at the very start ---
CWD = os.getcwd()
print(f"--- Python script 'server.py' is starting. ---")
print(f"--- Current Working Directory (os.getcwd()): {CWD} ---")
# __file__ is the path to this server.py script
ABS_SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(ABS_SCRIPT_PATH)
print(f"--- Absolute path of this script (__file__): {ABS_SCRIPT_PATH} ---")
print(f"--- Directory of server.py (SCRIPT_DIR): {SCRIPT_DIR} ---")

# --- Robust way to handle imports when 'converters' is a subdirectory ---
# SCRIPT_DIR should be your project root 'JSPY' if you run `python server.py` from JSPY.
# Adding SCRIPT_DIR to sys.path ensures Python can find the 'converters' package.
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR) # Add to the beginning of the search path
    print(f"--- Added '{SCRIPT_DIR}' to sys.path for module resolution. ---")

print(f"--- Current sys.path: {sys.path} ---")

# --- Attempt to import the critical transpiler function ---
try:
    from converters.js2py_converter import transpile_js_to_python
    print("--- Successfully imported 'transpile_js_to_python' from 'converters.js2py_converter'. ---")
except ImportError as e:
    print(f"--- !!! FATAL ERROR: Could not import 'transpile_js_to_python'. !!! ---")
    print(f"--- ImportError details: {e} ---")
    print(f"--- Please ensure 'JSPY/converters/js2py_converter.py' exists and there are no syntax errors in it. ---")
    print(f"--- Also check that 'JSPY/parser.js' and 'node_modules' (with @babel/parser) are present in '{SCRIPT_DIR}'. ---")
    sys.exit("Essential transpiler module import failed. Application cannot start.")
except Exception as e_generic: # Catch other potential errors during import
    print(f"--- !!! FATAL ERROR: An unexpected error occurred while importing 'transpile_js_to_python'. !!! ---")
    print(f"--- Error details: {type(e_generic).__name__}: {e_generic} ---")
    import traceback
    traceback.print_exc()
    sys.exit("Unexpected error during critical transpiler module import.")


# --- Initialize Flask App ONCE ---
# static_folder='.' means Flask will look for static files (CSS, client-side JS)
# in the Current Working Directory (CWD) from where server.py is run.
# If you run `python server.py` from JSPY, CWD will be JSPY.
# template_folder='.' means Flask looks for 'index.html' in the CWD.
# CWD should be your project root (e.g., C:\Users\Rohit\Desktop\jspy)
# SCRIPT_DIR is also the project root if server.py is there.
# Using SCRIPT_DIR (absolute path to where server.py is) for static and templates is more robust.
app = Flask(__name__, template_folder='templates', static_folder='static')
 # <<< MODIFIED LINE
print(f"--- Flask app initialized. template_folder='templates', static_folder='static' ---")


@app.route('/')
def index():
    print(f"--- [{request.method}] Request for route / (index.html) from {request.remote_addr} ---")
    return render_template('index.html')

@app.route('/transpile', methods=['POST'])
def handle_transpile():
    print(f"--- [{request.method}] Request for route /transpile from {request.remote_addr} ---")
    try:
        # Ensure the request has JSON data
        if not request.is_json:
            print("--- ERROR in /transpile: Request Content-Type is not 'application/json'. ---")
            return jsonify({'error': 'Invalid request: Content-Type must be application/json.'}), 415 # Unsupported Media Type
        
        data = request.get_json()
        if data is None: # Should be caught by request.is_json check but good to have
            print("--- ERROR in /transpile: No JSON data received even with correct Content-Type. ---")
            return jsonify({'error': 'Invalid request: No JSON data body received.'}), 400

    except Exception as e: # Catch errors during request.get_json() itself (e.g., malformed JSON)
        print(f"--- ERROR in /transpile: Could not parse request JSON. Error: {type(e).__name__}: {e} ---")
        return jsonify({'error': f'Could not parse request JSON: {e}'}), 400


    js_code = data.get('js_code', '') # Safely get js_code, defaults to empty string if key is missing
    # Optional: Truncate long js_code for logging to keep logs manageable
    log_js_code = js_code[:100] + '...' if len(js_code) > 100 else js_code
    print(f"--- /transpile: Received js_code (up to 100 chars): '{log_js_code}' ---")

    if not js_code.strip():
        print("--- /transpile: No JavaScript code provided by client (empty or whitespace only). ---")
        return jsonify({'error': 'No JavaScript code provided.'}), 400 # Client error

    print("--- /transpile: Calling 'transpile_js_to_python' from 'converters' module... ---")
    # This is the critical call to your backend logic
    python_code, error_message = transpile_js_to_python(js_code)

    if error_message:
        print(f"--- /transpile: 'transpile_js_to_python' returned an error: {error_message} ---")
        # Return 200 OK so the client-side JS can always parse the JSON body for the error message.
        return jsonify({'error': error_message, 'python_code': None}), 200
    else:
        # Truncate long python_code for logging
        log_python_code = python_code[:100] + '...' if len(python_code) > 100 else python_code
        print(f"--- /transpile: 'transpile_js_to_python' successful. Python (up to 100 chars): '{log_python_code}' ---")
        return jsonify({'python_code': python_code, 'error': None})


if __name__ == '__main__':
    print("--- Starting Flask development server... ---")
    print("--- This server will serve the UI and handle transpilation requests. ---")
    print(f"--- Web UI should be accessible at http://127.0.0.1:5000/ (or a similar address if port is in use) ---")
    print("--- Ensure 'JSPY/parser.js' and 'JSPY/node_modules' (with @babel/parser) are present. ---")
    print("--- Press CTRL+C in this terminal to stop the server. ---")
    # debug=True enables the reloader and debugger.
    # host='0.0.0.0' makes the server accessible from other devices on your local network.
    app.run(debug=True, host='0.0.0.0', port=5000)