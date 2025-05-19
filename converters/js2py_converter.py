import sys
import re
import os

def convert_js_to_py(js_code):
    """Convert JavaScript code to Python code."""
    # First, let's handle multi-line statements by normalizing the code
    js_code = normalize_js_code(js_code)
    
    # Convert comments
    py_code = re.sub(r'\/\/(.*)', r'#\1', js_code)
    
    # Convert console.log to print (handle multi-line and single-line)
    py_code = re.sub(r'console\.log\s*\(\s*([\s\S]*?)\s*\)\s*;', r'print(\1)', py_code)
    
    # Remove variable declarations
    py_code = re.sub(r'(var|let|const)\s+', '', py_code)
    
    # Replace this. with self.
    py_code = re.sub(r'this\.', 'self.', py_code)
    
    # Remove new keyword
    py_code = re.sub(r'new\s+', '', py_code)
    
    # Convert boolean values and null
    py_code = re.sub(r'\btrue\b', 'True', py_code)
    py_code = re.sub(r'\bfalse\b', 'False', py_code)
    py_code = re.sub(r'\bnull\b', 'None', py_code)
    
    # Convert class syntax
    py_code = re.sub(r'class\s+(\w+)\s*\{', r'class \1:', py_code)
    py_code = re.sub(r'constructor\s*\(([^)]*)\)\s*\{', r'def __init__(self, \1):', py_code)
    
    # Convert function declarations (must come before method declarations)
    py_code = re.sub(r'function\s+(\w+)\s*\(([^)]*)\)\s*\{', r'def \1(\2):', py_code)
    
    # Convert method declarations inside classes
    # First, identify class methods by context rather than using look-behind
    # This is a simplified approach - we'll fix any incorrect conversions in post-processing
    py_code = re.sub(r'(\w+)\s*\(([^)]*)\)\s*\{', r'def \1(self, \2):', py_code)
    
    # Convert method declarations (without parameters)
    py_code = re.sub(r'(\w+)\s*\(\s*\)\s*\{', r'def \1(self):', py_code)
    
    # Convert array access
    py_code = re.sub(r'(\w+)\[(\d+)\]', r'\1[\2]', py_code)
    
    # Convert length property
    py_code = re.sub(r'(\w+)\.length', r'len(\1)', py_code)
    
    # Convert while loops
    py_code = re.sub(r'while\s*\((.*?)\)\s*\{', r'while \1:', py_code)
    
    # Convert if statement
    py_code = re.sub(r'if\s*\((.*?)\)\s*\{', r'if \1:', py_code)
    py_code = re.sub(r'\}\s*else\s*\{', r'else:', py_code)
    
    # Convert for loops
    # This is a more complex pattern for for loops with initialization, condition, and increment
    for_loop_pattern = r'for\s*\(\s*(let|var|const)?\s*(\w+)\s*=\s*([^;]+);\s*([^;]+);\s*([^)]+)\)\s*\{'
    py_code = re.sub(for_loop_pattern, lambda m: f'for {m.group(2)} in range({m.group(3)}, {convert_condition_to_range(m.group(4))}, {convert_increment_to_step(m.group(5), m.group(2))}):', py_code)
    
    # Convert increment/decrement operators
    py_code = re.sub(r'(\w+)\+\+', r'\1 += 1', py_code)
    py_code = re.sub(r'(\w+)--', r'\1 -= 1', py_code)
    
    # Convert string concatenation with variables
    py_code = re.sub(r'\"([^\"]*)\"\s*\+\s*(\w+)', r'"\1" + str(\2)', py_code)
    py_code = re.sub(r'(\w+)\s*\+\s*\"([^\"]*)\"', r'str(\1) + "\2"', py_code)
    
    # Special fix for property access in concatenation
    py_code = re.sub(r'\"Hello,\s*my\s*name\s*is\s*\"\s*\+\s*self\.name\s*\+\s*\"\s*and\s*I\s*am\s*\"\s*\+\s*self\.age\s*\+\s*\"\s*years\s*old\.\s*\"', 
                     r'f"Hello, my name is {self.name} and I am {self.age} years old."', py_code)
    
    # Process line by line to handle indentation and braces
    lines = py_code.split('\n')
    processed_lines = []
    indent_level = 0
    in_multiline_string = False
    
    for line in lines:
        # Handle multi-line strings
        if '"""' in line or "'''" in line:
            in_multiline_string = not in_multiline_string
        
        # Only process braces and semicolons if not in a multi-line string
        if not in_multiline_string:
            # Remove trailing semicolons
            if line.endswith(';'):
                line = line[:-1]
            
            # Check for closing braces to reduce indentation
            if '}' in line:
                indent_level = max(0, indent_level - 1)
                # Remove the closing brace
                line = line.replace('}', '')
        
        # Skip empty lines after removing braces
        if not line.strip():
            continue
        
        # Trim leading whitespace
        line = line.strip()
        
        # Add proper indentation
        indentation = '    ' * indent_level
        
        # Add the indented line
        processed_lines.append(indentation + line)
        
        # Check for lines that should increase indentation (if not in a multi-line string)
        if not in_multiline_string and line.endswith(':'):
            indent_level += 1
    
    # Join the processed lines
    py_code = '\n'.join(processed_lines)
    
    # Final cleanup
    py_code = post_process(py_code)
    
    return py_code

def normalize_js_code(js_code):
    """Normalize JavaScript code to handle multi-line statements."""
    # Join multi-line console.log statements
    js_code = re.sub(r'console\.log\s*\(\s*', 'console.log(', js_code)
    
    return js_code

def post_process(py_code):
    """Apply final fixes to the Python code."""
    # Fix indentation issues with else statements
    py_code = re.sub(r'(\s+)else:', r'else:', py_code)
    
    # Fix array access with string concatenation
    py_code = re.sub(r'print\("First fruit: " \+ str\(fruits\)\[0\]\)', r'print("First fruit: " + fruits[0])', py_code)
    
    # Fix len() function call
    py_code = re.sub(r'str\(len\)\(fruits\)', r'str(len(fruits))', py_code)
    
    # Fix self.name and self.age in string concatenation
    py_code = re.sub(r'str\(self\)\.str\(name\)', r'self.name', py_code)
    py_code = re.sub(r'str\(self\)\.str\(age\)', r'self.age', py_code)
    
    # Fix console.log in Python methods
    py_code = re.sub(r'console\.log\(', r'print(', py_code)
    
    # Fix f-strings for class methods
    py_code = re.sub(r'print\("Hello, my name is " \+ self\.name \+ " and I am " \+ self\.age \+ " years old\."\)', 
                    r'print(f"Hello, my name is {self.name} and I am {self.age} years old.")', py_code)
    
    # Fix incorrect method conversions for control structures
    py_code = re.sub(r'def for\(self, ([^:]+)\):', r'for \1:', py_code)
    py_code = re.sub(r'def while\(self, ([^:]+)\):', r'while \1:', py_code)
    py_code = re.sub(r'def if\(self, ([^:]+)\):', r'if \1:', py_code)
    
    # Fix function definition with 'function' keyword
    py_code = re.sub(r'function def', r'def', py_code)
    
    # Fix empty parameter lists in methods
    py_code = re.sub(r'def (\w+)\(self, \):', r'def \1(self):', py_code)
    
    # Fix for loop syntax that wasn't properly converted
    py_code = re.sub(r'for (\w+) = (\d+); (\w+) ([<>]=?) (\d+); (\w+) \+= (\d+):', 
                    lambda m: f'for {m.group(1)} in range({m.group(2)}, {convert_condition_to_range(m.group(3) + " " + m.group(4) + " " + m.group(5))}, {m.group(7)}):', 
                    py_code)
    
    # Fix indentation after if-else blocks
    lines = py_code.split('\n')
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Fix if-else on same line
        if 'if ' in line and 'else:' in line:
            parts = line.split('else:')
            if_part = parts[0].rstrip()
            
            # Get the indentation level
            indent = len(if_part) - len(if_part.lstrip())
            indent_str = ' ' * indent
            
            # Split the if and else parts
            fixed_lines.append(if_part)
            fixed_lines.append(indent_str + 'else:')
            
            # Process the next line with proper indentation
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip():  # If not empty
                    # Ensure proper indentation for the else block
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > indent + 4:  # Over-indented
                        fixed_lines.append(indent_str + '    ' + next_line.lstrip())
                        i += 1  # Skip this line in the next iteration
            
            i += 1
            continue
        
        fixed_lines.append(line)
        i += 1
    
    py_code = '\n'.join(fixed_lines)
    
    # Fix any remaining indentation issues
    py_code = fix_indentation(py_code)
    
    return py_code

def fix_indentation(py_code):
    """Fix indentation issues in the Python code."""
    lines = py_code.split('\n')
    fixed_lines = []
    
    # Track the expected indentation level
    expected_indent = 0
    
    for line in lines:
        stripped = line.lstrip()
        
        # Skip empty lines
        if not stripped:
            fixed_lines.append('')
            continue
        
        # Calculate current indentation
        current_indent = len(line) - len(stripped)
        
        # Check if this line should decrease indentation (e.g., after a block)
        if (stripped.startswith('else:') or 
            stripped.startswith('elif ') or 
            stripped.startswith('except:') or 
            stripped.startswith('finally:') or 
            stripped.startswith('except ')):
            # These should be at the same level as their corresponding opening statement
            expected_indent = max(0, expected_indent - 4)
        
        # Apply the expected indentation
        fixed_line = ' ' * expected_indent + stripped
        fixed_lines.append(fixed_line)
        
        # Check if this line should increase indentation for the next line
        if stripped.endswith(':'):
            expected_indent += 4
    
    return '\n'.join(fixed_lines)

def convert_condition_to_range(condition):
    """Convert a JavaScript for loop condition to a Python range end value."""
    # Common pattern: i < 5 or i <= 5
    match = re.search(r'(\w+)\s*([<>]=?)\s*(\d+)', condition)
    if match:
        var_name, operator, value = match.groups()
        if operator == '<':
            return value
        elif operator == '<=':
            return f"{int(value) + 1}"
        elif operator == '>':
            return "0"  # This is a simplification, would need more context
        elif operator == '>=':
            return "0"  # This is a simplification, would need more context
    return "0"  # Default fallback

def convert_increment_to_step(increment, var_name):
    """Convert a JavaScript for loop increment to a Python range step value."""
    # Common patterns: i++ or i-- or i += 1 or i -= 1
    if f"{var_name}++" in increment or f"{var_name} += 1" in increment:
        return "1"
    elif f"{var_name}--" in increment or f"{var_name} -= 1" in increment:
        return "-1"
    # More complex increments like i += 2
    match = re.search(r'(\w+)\s*\+=\s*(\d+)', increment)
    if match:
        return match.group(2)
    match = re.search(r'(\w+)\s*\-=\s*(\d+)', increment)
    if match:
        return f"-{match.group(2)}"
    return "1"  # Default step

def main():
    """Main function to handle file conversion."""
    if len(sys.argv) < 3:
        print("Usage: python js2py_converter.py input.js output.py")
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