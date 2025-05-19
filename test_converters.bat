@echo off
echo Testing JavaScript to Python Converters
echo =====================================
echo.

echo PART 1: Basic Sample Test
echo -------------------------
echo.

echo Testing Basic Python Converter...
python basic_js2py.py sample.js output_basic.py
echo.

echo Testing Improved Python Converter...
python js2py_improved.py sample.js output_improved.py
echo.

echo Testing Original Python Converter...
python js2py_converter.py sample.js output_py.py
echo.

echo Testing C++ Converter...
final_js2py.exe sample.js output_cpp.py
echo.

echo PART 2: Advanced Sample Test
echo ---------------------------
echo.

echo Testing Basic Python Converter...
python basic_js2py.py advanced_sample.js advanced_output_basic.py
echo.

echo Testing Improved Python Converter...
python js2py_improved.py advanced_sample.js advanced_output_improved.py
echo.

echo Testing Original Python Converter...
python js2py_converter.py advanced_sample.js advanced_output_py.py
echo.

echo Testing C++ Converter...
final_js2py.exe advanced_sample.js advanced_output_cpp.py
echo.

echo Conversion Results (Basic Sample):
echo ================================
echo.

echo Original JavaScript (sample.js):
echo -------------------------------
type sample.js
echo.
echo.

echo Basic Python Converter Output (output_basic.py):
echo ------------------------------------------
type output_basic.py
echo.
echo.

echo Improved Python Converter Output (output_improved.py):
echo ------------------------------------------------
type output_improved.py
echo.
echo.

echo Original Python Converter Output (output_py.py):
echo -------------------------------------------
type output_py.py
echo.
echo.

echo C++ Converter Output (output_cpp.py):
echo ----------------------------------
type output_cpp.py
echo.
echo.

echo Conversion Results (Advanced Sample):
echo ==================================
echo.

echo Original JavaScript (advanced_sample.js):
echo -------------------------------------
type advanced_sample.js
echo.
echo.

echo C++ Converter Output (advanced_output_cpp.py):
echo ------------------------------------------
type advanced_output_cpp.py
echo.
echo.

echo Python Converter Output (advanced_output_py.py):
echo -------------------------------------------
type advanced_output_py.py
echo.
echo.

echo Improved Python Converter Output (advanced_output_improved.py):
echo --------------------------------------------------------
type advanced_output_improved.py
echo.

echo.
echo Test complete. Please review the outputs to determine which converter works best.
pause