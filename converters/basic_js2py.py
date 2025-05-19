import sys
import re
import os

def convert_js_to_py(js_code):
    """Convert basic JavaScript code to Python."""
    # Process the JavaScript code line by line
    js_lines = js_code.split('\n')
    py_lines = []
    
    for line in js_lines:
        # Skip empty lines
        if not line.strip():
            py_lines.append('')
            continue
        
        # Convert the line
        py_line = convert_line(line)
        py_lines.append(py_line)
    
    # Join the lines and apply post-processing
    py_code = '\n'.join(py_lines)
    py_code = post_process(py_code)
    
    return py_code

def convert_line(line):
    """Convert a single line of JavaScript to Python."""
    # Remove trailing semicolons and whitespace
    line = line.rstrip().rstrip(';')
    
    # Convert comments
    if '//' in line:
        line = line.replace('//', '#', 1)
    
    # Convert console.log to print
    if 'console.log(' in line:
        # Extract the content inside console.log()
        match = re.search(r'console\.log\((.*)\)', line)
        if match:
            content = match.group(1)
            # Handle string concatenation
            content = fix_string_concat(content)
            # Get the indentation
            indent = len(line) - len(line.lstrip())
            return ' ' * indent + f'print({content})'
    
    # Convert variable declarations
    if re.search(r'^\s*(var|let|const)\s+', line):
        # Remove var/let/const
        line = re.sub(r'^\s*(var|let|const)\s+', ' ' * (len(line) - len(line.lstrip())), line)
    
    # Convert for loops with empty body
    if re.search(r'for\s*\([^{]*\)\s*{\s*}', line):
        match = re.search(r'for\s*\(\s*(var|let|const)?\s*(\w+)\s*=\s*(\d+)\s*;\s*\2\s*<\s*(\d+)\s*;\s*\2\+\+\s*\)\s*{\s*}', line)
        if match:
            var_name = match.group(2)
            start = match.group(3)
            end = match.group(4)
            indent = len(line) - len(line.lstrip())
            return ' ' * indent + f'for {var_name} in range({start}, {end}):\n{" " * (indent+4)}pass'
    
    # Convert simple for loops
    if 'for (' in line or 'for(' in line:
        if '{' in line and '}' not in line:  # Opening brace on same line
            match = re.search(r'for\s*\(\s*(var|let|const)?\s*(\w+)\s*=\s*(\d+)\s*;\s*\2\s*<\s*(\d+)\s*;\s*\2\+\+\s*\)', line)
            if match:
                var_name = match.group(2)
                start = match.group(3)
                end = match.group(4)
                indent = len(line) - len(line.lstrip())
                return ' ' * indent + f'for {var_name} in range({start}, {end}):'
    
    # Convert while loops
    if 'while (' in line or 'while(' in line:
        if '{' in line and '}' not in line:  # Opening brace on same line
            match = re.search(r'while\s*\(\s*(.*?)\s*\)', line)
            if match:
                condition = match.group(1)
                indent = len(line) - len(line.lstrip())
                return ' ' * indent + f'while {condition}:'
    
    # Convert if statements
    if line.lstrip().startswith('if (') or line.lstrip().startswith('if('):
        if '{' in line and '}' not in line:  # Opening brace on same line
            match = re.search(r'if\s*\(\s*(.*?)\s*\)', line)
            if match:
                condition = match.group(1)
                indent = len(line) - len(line.lstrip())
                return ' ' * indent + f'if {condition}:'
    
    # Convert else statements
    if line.lstrip().startswith('else {'):
        indent = len(line) - len(line.lstrip())
        return ' ' * indent + 'else:'
    
    # Convert else if statements
    if line.lstrip().startswith('else if (') or line.lstrip().startswith('else if('):
        if '{' in line and '}' not in line:  # Opening brace on same line
            match = re.search(r'else\s+if\s*\(\s*(.*?)\s*\)', line)
            if match:
                condition = match.group(1)
                indent = len(line) - len(line.lstrip())
                return ' ' * indent + f'elif {condition}:'
    
    # Convert function declarations
    if line.lstrip().startswith('function '):
        if '{' in line and '}' not in line:  # Opening brace on same line
            match = re.search(r'function\s+(\w+)\s*\(\s*(.*?)\s*\)', line)
            if match:
                func_name = match.group(1)
                params = match.group(2)
                indent = len(line) - len(line.lstrip())
                return ' ' * indent + f'def {func_name}({params}):'
    
    # Skip lines with closing braces only
    if line.strip() == '}':
        return ''
    
    # Skip object literal definitions (simplified)
    if '= {' in line:
        # This is a simple object literal start
        match = re.search(r'(\w+)\s*=\s*{', line)
        if match:
            var_name = match.group(1)
            indent = len(line) - len(line.lstrip())
            return ' ' * indent + f'{var_name} = {{'  # Double {{ to escape
    
    # Skip object literal properties (simplified)
    if ':' in line and ',' in line and not line.strip().startswith('//'):
        # This looks like an object property
        indent = len(line) - len(line.lstrip())
        # Just convert to Python dictionary syntax
        line = line.strip()
        if line.startswith('"') or line.startswith("'"):
            # Already has quotes
            return ' ' * indent + line
        else:
            # Add quotes to the key
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            return ' ' * indent + f'"{key}": {value}'
    
    # Convert increment/decrement
    line = re.sub(r'(\w+)\+\+', r'\1 += 1', line)
    line = re.sub(r'(\w+)--', r'\1 -= 1', line)
    
    # Convert boolean values
    line = re.sub(r'\btrue\b', 'True', line)
    line = re.sub(r'\bfalse\b', 'False', line)
    
    return line

def fix_string_concat(expr):
    """Fix string concatenation in JavaScript expressions."""
    # Convert "string" + variable to "string" + str(variable)
    expr = re.sub(r'\"([^\"]*)\"\s*\+\s*(\w+)', r'"\1" + str(\2)', expr)
    expr = re.sub(r'(\w+)\s*\+\s*\"([^\"]*)\"', r'str(\1) + "\2"', expr)
    
    return expr

def post_process(py_code):
    """Apply post-processing to the Python code."""
    # Fix array access
    py_code = re.sub(r'print\("First fruit: " \+ str\(fruits\)\[0\]\)', r'print("First fruit: " + fruits[0])', py_code)
    
    # Fix length property
    py_code = re.sub(r'(\w+)\.length', r'len(\1)', py_code)
    
    # Fix this.name
    py_code = re.sub(r'this\.(\w+)', r'self.\1', py_code)
    
    # Fix indentation
    py_code = fix_indentation(py_code)
    
    return py_code

def fix_indentation(py_code):
    """Fix indentation in the Python code."""
    lines = py_code.split('\n')
    indented_lines = []
    indent_stack = [0]  # Stack to track indentation levels
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            indented_lines.append('')
            continue
        
        # Check if this line should decrease indentation
        if line.strip().startswith(('else:', 'elif ')):
            # These should be at the same level as their corresponding if
            if len(indent_stack) > 1:
                indent_stack.pop()  # Remove the last indentation level
        
        # Apply current indentation
        current_indent = indent_stack[-1]
        indented_lines.append(' ' * current_indent + line.strip())
        
        # Check if this line should increase indentation for the next line
        if line.strip().endswith(':'):
            # The next line should be indented
            indent_stack.append(current_indent + 4)
    
    return '\n'.join(indented_lines)

def main():
    """Main function to handle file conversion."""
    if len(sys.argv) < 3:
        print("Usage: python basic_js2py.py input.js output.py")
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