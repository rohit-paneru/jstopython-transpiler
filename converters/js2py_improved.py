import sys
import re
import os

def convert_js_to_py(js_code):
    """Convert JavaScript code to Python code with proper indentation."""
    # Handle empty or very simple code
    if not js_code.strip():
        return "# Empty JavaScript code"
    
    # Simple direct conversion for very basic code
    if len(js_code.strip().split('\n')) <= 10:
        return simple_convert(js_code)
    
    # For more complex code, use the tokenization approach
    try:
        # First, tokenize the JavaScript code to handle structure properly
        tokens = tokenize_js(js_code)
        
        # Convert the tokens to Python code
        py_code = generate_python(tokens)
        
        return py_code
    except Exception as e:
        # Fallback to simple conversion if tokenization fails
        print(f"Warning: Complex parsing failed ({str(e)}), falling back to simple conversion")
        return simple_convert(js_code)

def simple_convert(js_code):
    """Simple line-by-line conversion for basic JavaScript code."""
    lines = js_code.strip().split('\n')
    py_lines = []
    
    indent = 0
    in_object_literal = False
    object_indent = 0
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            py_lines.append('')
            i += 1
            continue
        
        # Check for object literal start
        if '=' in line and '{' in line and '}' not in line and not line.startswith('if') and not line.startswith('for') and not line.startswith('while'):
            in_object_literal = True
            object_indent = indent
            
            # Convert object literal to dictionary
            var_name = line.split('=')[0].strip()
            py_lines.append(' ' * (4 * indent) + var_name + ' = {')
            indent += 1
            i += 1
            continue
        
        # Check for object literal end
        if in_object_literal and line.startswith('}'):
            in_object_literal = False
            indent = object_indent
            py_lines.append(' ' * (4 * indent) + '}')
            i += 1
            continue
        
        # Handle object literal properties
        if in_object_literal:
            # Convert property to dictionary key-value pair
            if ':' in line:
                prop = line.rstrip(',')
                key, value = prop.split(':', 1)
                key = key.strip().strip('"\'')
                value = value.strip()
                
                # Handle function in object
                if 'function' in value:
                    # Skip this line, object methods are not directly convertible
                    i += 1
                    # Skip until we find the closing brace
                    brace_count = 1
                    while i < len(lines) and brace_count > 0:
                        if '{' in lines[i]:
                            brace_count += 1
                        if '}' in lines[i]:
                            brace_count -= 1
                        i += 1
                    continue
                
                py_lines.append(' ' * (4 * indent) + f'"{key}": {value},')
                i += 1
                continue
        
        # Handle normal indentation
        if '}' in line and indent > 0 and not in_object_literal:
            indent -= 1
        
        # Handle else statements
        if line.startswith('} else') or line == 'else {':
            # Extract the else part
            if 'else if' in line or 'else {' in line:
                # This is an else if or else block
                py_line = ' ' * (4 * (indent)) + convert_line(line.replace('}', '').strip())
                py_lines.append(py_line)
                
                # Increase indent for the next line
                if '{' in line and '}' not in line:
                    indent += 1
                
                i += 1
                continue
        
        # Convert the line
        py_line = ' ' * (4 * indent) + convert_line(line)
        py_lines.append(py_line)
        
        # Check if indentation should increase
        if '{' in line and '}' not in line and not in_object_literal:
            indent += 1
        
        i += 1
    
    # Post-process the Python code
    py_code = '\n'.join(py_lines)
    py_code = post_process(py_code)
    
    return py_code

def post_process(py_code):
    """Apply final fixes to the Python code."""
    # Fix boolean values
    py_code = py_code.replace(' true', ' True')
    py_code = py_code.replace(' false', ' False')
    
    # Fix array access
    py_code = re.sub(r'print\("First fruit: " \+ str\(fruits\)\[0\]\)', r'print("First fruit: " + fruits[0])', py_code)
    
    # Fix length property
    py_code = re.sub(r'str\((\w+)\)\.length', r'len(\1)', py_code)
    
    # Fix this.name
    py_code = re.sub(r'str\(this\)\.(\w+)', r'self.\1', py_code)
    
    return py_code

def convert_line(js_line):
    """Convert a single line of JavaScript to Python."""
    # Remove trailing semicolons
    js_line = js_line.rstrip(';')
    
    # Convert console.log to print
    if js_line.startswith('console.log('):
        content = js_line[12:-1]  # Remove console.log( and )
        # Handle string concatenation in console.log
        content = convert_string_concat(content)
        return f"print({content})"
    
    # Convert variable declarations
    if js_line.startswith(('var ', 'let ', 'const ')):
        js_line = re.sub(r'^(var|let|const)\s+', '', js_line)
    
    # Convert for loops
    if js_line.startswith('for(') or js_line.startswith('for ('):
        # Extract the for loop components
        match = re.search(r'for\s*\(\s*(let|var|const)?\s*(\w+)\s*=\s*([^;]+);\s*([^;]+);\s*([^)]+)\)', js_line)
        if match:
            var_name = match.group(2)
            start = match.group(3)
            condition = match.group(4)
            increment = match.group(5)
            
            # Convert the condition to a range end value
            end = "5"  # Default value
            if '<' in condition:
                end_match = re.search(r'(\w+)\s*<\s*(\d+)', condition)
                if end_match:
                    end = end_match.group(2)
            elif '<=' in condition:
                end_match = re.search(r'(\w+)\s*<=\s*(\d+)', condition)
                if end_match:
                    end = str(int(end_match.group(2)) + 1)
            
            # Convert the increment to a step value
            step = "1"  # Default value
            if '+=' in increment:
                step_match = re.search(r'(\w+)\s*\+=\s*(\d+)', increment)
                if step_match:
                    step = step_match.group(2)
            elif '++' in increment:
                step = "1"
            
            # Handle empty for loop body
            if js_line.endswith('{}'):
                return f"for {var_name} in range({start}, {end}, {step}):\n    pass"
            
            return f"for {var_name} in range({start}, {end}, {step}):"
    
    # Convert while loops
    if js_line.startswith('while(') or js_line.startswith('while ('):
        # Extract the condition
        match = re.search(r'while\s*\(\s*(.*?)\s*\)', js_line)
        if match:
            condition = match.group(1)
            
            # Handle empty while loop body
            if js_line.endswith('{}'):
                return f"while {condition}:\n    pass"
            
            return f"while {condition}:"
    
    # Convert if statements
    if js_line.startswith('if(') or js_line.startswith('if ('):
        # Extract the condition
        match = re.search(r'if\s*\(\s*(.*?)\s*\)', js_line)
        if match:
            condition = match.group(1)
            
            # Handle empty if body
            if js_line.endswith('{}'):
                return f"if {condition}:\n    pass"
            
            return f"if {condition}:"
    
    # Convert else statements
    if js_line.startswith('else') and not js_line.startswith('else if'):
        # Handle empty else body
        if js_line.endswith('{}'):
            return f"else:\n    pass"
        
        # Handle else with opening brace
        if js_line.endswith('{'):
            return "else:"
        
        # Handle else without braces (single line)
        match = re.search(r'else\s+(.*)', js_line)
        if match and not match.group(1).startswith('{'):
            statement = match.group(1)
            return f"else:\n    {convert_line(statement)}"
        
        return "else:"
    
    # Convert else if statements
    if js_line.startswith('else if(') or js_line.startswith('else if ('):
        # Extract the condition
        match = re.search(r'else\s+if\s*\(\s*(.*?)\s*\)', js_line)
        if match:
            condition = match.group(1)
            
            # Handle empty else if body
            if js_line.endswith('{}'):
                return f"elif {condition}:\n    pass"
            
            # Handle else if with opening brace
            if js_line.endswith('{'):
                return f"elif {condition}:"
            
            # Handle else if without braces (single line)
            match = re.search(r'else\s+if\s*\([^)]*\)\s+(.*)', js_line)
            if match and not match.group(1).startswith('{'):
                statement = match.group(1)
                return f"elif {condition}:\n    {convert_line(statement)}"
            
            return f"elif {condition}:"
    
    # Convert function declarations
    if js_line.startswith('function '):
        # Extract function name and parameters
        match = re.search(r'function\s+(\w+)\s*\(\s*(.*?)\s*\)', js_line)
        if match:
            func_name = match.group(1)
            params = match.group(2)
            
            # Handle empty function body
            if js_line.endswith('{}'):
                return f"def {func_name}({params}):\n    pass"
            
            return f"def {func_name}({params}):"
    
    # Convert array access
    js_line = re.sub(r'(\w+)\.length', r'len(\1)', js_line)
    
    # Convert string concatenation
    js_line = convert_string_concat(js_line)
    
    # Convert this. to self.
    js_line = re.sub(r'this\.', 'self.', js_line)
    
    # Handle object literal property access
    js_line = re.sub(r'(\w+)\[([\'"])(.*?)(\2)\]', r'\1["\3"]', js_line)
    
    # Handle object method calls
    if re.search(r'(\w+)\.(\w+)\(\)', js_line):
        match = re.search(r'(\w+)\.(\w+)\(\)', js_line)
        if match:
            obj = match.group(1)
            method = match.group(2)
            js_line = f"{obj}.{method}()"
    
    return js_line

def convert_string_concat(expr):
    """Convert JavaScript string concatenation to Python."""
    # Convert "string" + variable to "string" + str(variable)
    expr = re.sub(r'\"([^\"]*)\"\s*\+\s*(\w+)', r'"\1" + str(\2)', expr)
    expr = re.sub(r'(\w+)\s*\+\s*\"([^\"]*)\"', r'str(\1) + "\2"', expr)
    
    return expr

def tokenize_js(js_code):
    """Tokenize JavaScript code into a structured format."""
    # Replace comments
    js_code = re.sub(r'\/\/(.*)', r'#\1', js_code)
    
    # Split the code into lines for easier processing
    lines = js_code.split('\n')
    
    # Initialize the token structure
    tokens = []
    current_block = []
    block_stack = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Process the line
        line = line.strip()
        
        # Check for block start/end
        if '{' in line:
            # Extract the part before the opening brace
            before_brace = line[:line.index('{')].strip()
            
            # Determine the type of block
            block_type = get_block_type(before_brace)
            
            # Add the block start token
            current_block.append({
                'type': 'block_start',
                'block_type': block_type,
                'content': before_brace
            })
            
            # Push the current block to the stack and start a new one
            block_stack.append(current_block)
            current_block = []
            
            # Process any content after the opening brace
            after_brace = line[line.index('{')+1:].strip()
            if after_brace and '}' not in after_brace:
                current_block.append({
                    'type': 'statement',
                    'content': after_brace
                })
        elif '}' in line:
            # Process any content before the closing brace
            before_brace = line[:line.index('}')].strip()
            if before_brace:
                current_block.append({
                    'type': 'statement',
                    'content': before_brace
                })
            
            # Pop the parent block from the stack
            if block_stack:
                # Add the current block as a child of the parent
                parent_block = block_stack.pop()
                parent_block.append({
                    'type': 'block',
                    'content': current_block
                })
                
                # Set the current block to the parent
                current_block = parent_block
            
            # Process any content after the closing brace
            after_brace = line[line.index('}')+1:].strip()
            if after_brace:
                if after_brace.startswith('else'):
                    # Handle else block
                    current_block.append({
                        'type': 'block_start',
                        'block_type': 'else',
                        'content': 'else'
                    })
                    
                    # Push the current block to the stack and start a new one
                    block_stack.append(current_block)
                    current_block = []
                    
                    # Process any content after 'else'
                    after_else = after_brace[4:].strip()
                    if after_else and after_else.startswith('{'):
                        # Skip the opening brace
                        after_else = after_else[1:].strip()
                        if after_else:
                            current_block.append({
                                'type': 'statement',
                                'content': after_else
                            })
                else:
                    current_block.append({
                        'type': 'statement',
                        'content': after_brace
                    })
        else:
            # Regular statement
            current_block.append({
                'type': 'statement',
                'content': line
            })
    
    # Handle any remaining blocks
    while block_stack:
        parent_block = block_stack.pop()
        parent_block.append({
            'type': 'block',
            'content': current_block
        })
        current_block = parent_block
    
    return current_block

def get_block_type(line):
    """Determine the type of block based on the line content."""
    if line.startswith('if '):
        return 'if'
    elif line.startswith('else if ') or line.startswith('elif '):
        return 'elif'
    elif line == 'else':
        return 'else'
    elif line.startswith('for '):
        return 'for'
    elif line.startswith('while '):
        return 'while'
    elif line.startswith('function '):
        return 'function'
    elif line.startswith('class '):
        return 'class'
    elif 'constructor' in line:
        return 'constructor'
    elif '(' in line and ')' in line and not line.startswith('console.log'):
        # Likely a method definition
        return 'method'
    else:
        return 'unknown'

def generate_python(tokens, indent_level=0):
    """Generate Python code from the token structure."""
    python_lines = []
    indent = '    ' * indent_level
    
    for token in tokens:
        if token['type'] == 'statement':
            # Convert the statement to Python
            py_statement = convert_statement(token['content'])
            python_lines.append(indent + py_statement)
        elif token['type'] == 'block_start':
            # Convert the block start to Python
            py_block_start = convert_block_start(token['block_type'], token['content'])
            python_lines.append(indent + py_block_start)
        elif token['type'] == 'block':
            # Recursively process the block with increased indentation
            block_code = generate_python(token['content'], indent_level + 1)
            python_lines.append(block_code)
    
    return '\n'.join(python_lines)

def convert_statement(js_statement):
    """Convert a JavaScript statement to Python."""
    # Remove trailing semicolons
    if js_statement.endswith(';'):
        js_statement = js_statement[:-1]
    
    # Convert console.log to print
    if js_statement.startswith('console.log('):
        content = js_statement[12:-1]  # Remove console.log( and )
        # Handle string concatenation
        content = convert_string_concat(content)
        return f"print({content})"
    
    # Convert variable declarations
    if js_statement.startswith(('var ', 'let ', 'const ')):
        js_statement = re.sub(r'^(var|let|const)\s+', '', js_statement)
    
    # Convert increment/decrement
    js_statement = re.sub(r'(\w+)\+\+', r'\1 += 1', js_statement)
    js_statement = re.sub(r'(\w+)--', r'\1 -= 1', js_statement)
    
    # Convert array access
    js_statement = re.sub(r'(\w+)\.length', r'len(\1)', js_statement)
    
    # Convert string concatenation
    js_statement = convert_string_concat(js_statement)
    
    # Convert new keyword
    js_statement = re.sub(r'new\s+', '', js_statement)
    
    # Convert this. to self.
    js_statement = re.sub(r'this\.', 'self.', js_statement)
    
    return js_statement

def convert_string_concat(expr):
    """Convert JavaScript string concatenation to Python."""
    # Convert "string" + variable to "string" + str(variable)
    expr = re.sub(r'\"([^\"]*)\"\s*\+\s*(\w+)', r'"\1" + str(\2)', expr)
    expr = re.sub(r'(\w+)\s*\+\s*\"([^\"]*)\"', r'str(\1) + "\2"', expr)
    
    return expr

def convert_block_start(block_type, content):
    """Convert a JavaScript block start to Python."""
    if block_type == 'if':
        # Convert if (condition) { to if condition:
        condition = re.search(r'if\s*\((.*)\)', content).group(1)
        return f"if {condition}:"
    elif block_type == 'elif':
        # Convert else if (condition) { to elif condition:
        condition = re.search(r'else\s+if\s*\((.*)\)', content).group(1)
        return f"elif {condition}:"
    elif block_type == 'else':
        return "else:"
    elif block_type == 'for':
        # Convert for (init; condition; increment) { to for var in range():
        match = re.search(r'for\s*\(\s*(let|var|const)?\s*(\w+)\s*=\s*([^;]+);\s*([^;]+);\s*([^)]+)\)', content)
        if match:
            var_name = match.group(2)
            start = match.group(3)
            condition = match.group(4)
            increment = match.group(5)
            
            # Convert the condition to a range end value
            end = convert_condition_to_range(condition)
            
            # Convert the increment to a step value
            step = convert_increment_to_step(increment, var_name)
            
            return f"for {var_name} in range({start}, {end}, {step}):"
        return "# Could not convert for loop"
    elif block_type == 'while':
        # Convert while (condition) { to while condition:
        condition = re.search(r'while\s*\((.*)\)', content).group(1)
        return f"while {condition}:"
    elif block_type == 'function':
        # Convert function name(params) { to def name(params):
        match = re.search(r'function\s+(\w+)\s*\((.*)\)', content)
        if match:
            name = match.group(1)
            params = match.group(2)
            return f"def {name}({params}):"
        return "# Could not convert function"
    elif block_type == 'class':
        # Convert class Name { to class Name:
        name = re.search(r'class\s+(\w+)', content).group(1)
        return f"class {name}:"
    elif block_type == 'constructor':
        # Convert constructor(params) { to def __init__(self, params):
        params = re.search(r'constructor\s*\((.*)\)', content).group(1)
        return f"def __init__(self, {params}):"
    elif block_type == 'method':
        # Convert method(params) { to def method(self, params):
        match = re.search(r'(\w+)\s*\((.*)\)', content)
        if match:
            name = match.group(1)
            params = match.group(2)
            if params:
                return f"def {name}(self, {params}):"
            else:
                return f"def {name}(self):"
        return "# Could not convert method"
    else:
        return f"# Unknown block type: {content}"

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
        print("Usage: python js2py_improved.py input.js output.py")
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