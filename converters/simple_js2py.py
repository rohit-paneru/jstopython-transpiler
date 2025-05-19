import sys
import re
import os

def convert_js_to_py(js_code):
    """Convert JavaScript code to Python code."""
    # Replace comments
    py_code = re.sub(r'\/\/(.*)', r'#\1', js_code)
    
    # Replace console.log with print
    py_code = re.sub(r'console\.log\((.*?)\);', r'print(\1)', py_code)
    
    # Replace variable declarations
    py_code = re.sub(r'(var|let|const)\s+(\w+)\s*=\s*', r'\2 = ', py_code)
    
    # Replace semicolons
    py_code = re.sub(r';', '', py_code)
    
    # Replace for loops
    py_code = re.sub(r'for\s*\(\s*(var|let|const)?\s*(\w+)\s*=\s*(\d+)\s*;\s*\2\s*<\s*(\d+)\s*;\s*\2\+\+\s*\)\s*{(.*?)}', 
                    lambda m: f'for {m.group(2)} in range({m.group(3)}, {m.group(4)}):{m.group(5)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace empty for loops
    py_code = re.sub(r'for\s*\(\s*(var|let|const)?\s*(\w+)\s*=\s*(\d+)\s*;\s*\2\s*<\s*(\d+)\s*;\s*\2\+\+\s*\)\s*{}', 
                    lambda m: f'for {m.group(2)} in range({m.group(3)}, {m.group(4)}):\n    pass', 
                    py_code)
    
    # Replace while loops
    py_code = re.sub(r'while\s*\((.*?)\)\s*{(.*?)}', 
                    lambda m: f'while {m.group(1)}:{m.group(2)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace if statements
    py_code = re.sub(r'if\s*\((.*?)\)\s*{(.*?)}', 
                    lambda m: f'if {m.group(1)}:{m.group(2)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace else if statements
    py_code = re.sub(r'}\s*else\s+if\s*\((.*?)\)\s*{(.*?)}', 
                    lambda m: f'elif {m.group(1)}:{m.group(2)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace else statements
    py_code = re.sub(r'}\s*else\s*{(.*?)}', 
                    lambda m: f'else:{m.group(1)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace function declarations
    py_code = re.sub(r'function\s+(\w+)\s*\((.*?)\)\s*{(.*?)}', 
                    lambda m: f'def {m.group(1)}({m.group(2)}):{m.group(3)}', 
                    py_code, flags=re.DOTALL)
    
    # Replace this. with self.
    py_code = re.sub(r'this\.', 'self.', py_code)
    
    # Replace array.length with len(array)
    py_code = re.sub(r'(\w+)\.length', r'len(\1)', py_code)
    
    # Replace boolean values
    py_code = re.sub(r'\btrue\b', 'True', py_code)
    py_code = re.sub(r'\bfalse\b', 'False', py_code)
    
    # Replace string concatenation
    py_code = re.sub(r'"([^"]*)"\s*\+\s*(\w+)', r'"\1" + str(\2)', py_code)
    py_code = re.sub(r'(\w+)\s*\+\s*"([^"]*)"', r'str(\1) + "\2"', py_code)
    
    # Replace increment/decrement
    py_code = re.sub(r'(\w+)\+\+', r'\1 += 1', py_code)
    py_code = re.sub(r'(\w+)--', r'\1 -= 1', py_code)
    
    # Fix indentation
    py_code = fix_indentation(py_code)
    
    return py_code

def fix_indentation(py_code):
    """Fix indentation in the Python code."""
    lines = py_code.split('\n')
    indented_lines = []
    indent_level = 0
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            indented_lines.append('')
            continue
        
        # Check if this line ends a block
        if line.strip().startswith(('elif', 'else')):
            # These should be at the same level as their corresponding if
            indented_lines.append(' ' * (4 * (indent_level - 1)) + line.strip())
            if line.strip().endswith(':'):
                # The next line should be indented
                continue
        else:
            # Apply current indentation
            indented_lines.append(' ' * (4 * indent_level) + line.strip())
        
        # Check if this line starts a new block
        if line.strip().endswith(':'):
            indent_level += 1
    
    return '\n'.join(indented_lines)

def main():
    """Main function to handle file conversion."""
    if len(sys.argv) < 3:
        print("Usage: python simple_js2py.py input.js output.py")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    try:
        with open(input_file, 'r') as f:
            js_code = f.read()
        
        py_code = convert_js_to_py(js_code)
        
        with open(output_file, 'w') as f:
            f.write(py_code)
        
        print(f"Conversion complete: {input_file} -> {output_file}")
    
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()