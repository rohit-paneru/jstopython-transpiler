import subprocess
import json
import re
import os
import traceback

CONVERTER_SCRIPT_PATH = os.path.abspath(__file__)
CONVERTER_DIR = os.path.dirname(CONVERTER_SCRIPT_PATH)
PROJECT_ROOT = os.path.dirname(CONVERTER_DIR)
PARSER_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "parser.js")

print(f"--- [CONVERTER_INIT] Module 'js2py_converter.py' loaded. ---")
print(f"--- [CONVERTER_INIT]   PROJECT_ROOT determined as: {PROJECT_ROOT} ---")
print(f"--- [CONVERTER_INIT]   PARSER_SCRIPT_PATH determined as: {PARSER_SCRIPT_PATH} ---")

class ASTNodeTransformer:
    def __init__(self):
        self.imports = set()

    def _transform_identifier_name(self, name_str):
        if not name_str: return ""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _indent_block(self, block_code_str, indent_level=1):
        indent = "    " * indent_level
        if not block_code_str or not block_code_str.strip():
            return indent + "pass"
        return "\n".join([indent + line for line in block_code_str.splitlines()])

    def transform_node(self, node):
        if not node:
            return ""
        
        node_type = node.get("type")

        if node_type == "Program":
            self.imports.clear()
            transformed_body_parts = []
            for sub_node in node.get("body", []):
                transformed_part = self.transform_node(sub_node)
                if transformed_part:
                    transformed_body_parts.append(transformed_part)
            
            final_python_code = ""
            if self.imports:
                final_python_code += "\n".join(sorted(list(self.imports))) + "\n\n"
            final_python_code += "\n".join(transformed_body_parts)
            return final_python_code

        elif node_type == "ExpressionStatement":
            return self.transform_node(node.get("expression"))

        elif node_type == "Identifier":
            return self._transform_identifier_name(node.get("name", ""))
        elif node_type == "StringLiteral":
            return f'"{node.get("value", "")}"'
        elif node_type == "NumericLiteral":
            return str(node.get("value"))
        elif node_type == "BooleanLiteral":
            return "True" if node.get("value") else "False"
        elif node_type == "NullLiteral":
            return "None"
        elif node_type == "TemplateLiteral":
            py_fstring_parts = []
            quasis = node.get("quasis", [])
            expressions = node.get("expressions", [])
            for i, quasi in enumerate(quasis):
                py_fstring_parts.append(quasi.get("value",{}).get("raw",""))
                if i < len(expressions):
                    expr_node_to_transform = expressions[i]
                    transformed_expr_for_fstring = self.transform_node(expr_node_to_transform)
                    py_fstring_parts.append(f"{{{transformed_expr_for_fstring}}}")
            return f'f"""{"".join(py_fstring_parts)}"""'

        elif node_type == "ObjectExpression":
            py_dict_items = []
            for prop_node in node.get("properties", []):
                if prop_node.get("type") == "ObjectProperty":
                    key_node = prop_node.get("key")
                    value_node = prop_node.get("value")
                    computed = prop_node.get("computed", False)

                    if key_node.get("type") == "Identifier" and not computed:
                        py_key_str = f'"{key_node.get("name")}"'
                    elif key_node.get("type") == "StringLiteral" and not computed:
                        py_key_str = f'"{key_node.get("value", "")}"'
                    else:
                        py_key_str = self.transform_node(key_node)

                    py_value_str = self.transform_node(value_node)
                    py_dict_items.append(f"{py_key_str}: {py_value_str}")

            return f"{{{', '.join(py_dict_items)}}}"

        elif node_type == "ArrayExpression":
            py_list_elements = []
            for element_node in node.get("elements", []):
                 if element_node is None:
                     py_list_elements.append("None")
                 elif element_node.get("type") == "SpreadElement":
                      argument_node = element_node.get("argument")
                      transformed_argument = self.transform_node(argument_node)
                      py_list_elements.append(f"*{transformed_argument}")
                 else:
                    py_list_elements.append(self.transform_node(element_node))
            return f"[{', '.join(py_list_elements)}]"

        elif node_type == "VariableDeclaration":
            py_declarations = []
            js_kind = node.get("kind")
            comment_for_const = f" # JS: {js_kind}" if js_kind == 'const' else ""
            for declaration in node.get("declarations", []):
                js_var_name = declaration.get("id", {}).get("name")
                py_var_name = self._transform_identifier_name(js_var_name)
                init_node = declaration.get("init")
                if init_node:
                    py_init_value = self.transform_node(init_node)
                    py_declarations.append(f"{py_var_name} = {py_init_value}{comment_for_const}")
                else:
                    py_declarations.append(f"{py_var_name} = None # JS: {js_kind} {js_var_name} (uninitialized){comment_for_const}")
            return "\n".join(py_declarations)

        elif node_type == "CallExpression":
            callee_node = node.get("callee")
            if callee_node.get("type") == "MemberExpression" and \
               callee_node.get("object", {}).get("name") == "console" and \
               callee_node.get("property", {}).get("name") == "log":
                py_args = [self.transform_node(arg) for arg in node.get("arguments", [])]
                return f"print({', '.join(py_args)})"
            elif callee_node.get("type") == "MemberExpression" and \
                 callee_node.get("object", {}).get("name") == "Math":
                self.imports.add("import math")
                js_math_method = callee_node.get("property", {}).get("name")
                py_math_method = js_math_method.lower()
                if py_math_method == "random":
                    self.imports.add("import random")
                    return f"random.random()"
                py_args = [self.transform_node(arg) for arg in node.get("arguments", [])]
                return f"math.{py_math_method}({', '.join(py_args)})"
            else:
                py_func_name = self.transform_node(callee_node)
                py_args = [self.transform_node(arg) for arg in node.get("arguments", [])]
                return f"{py_func_name}({', '.join(py_args)})"

        elif node_type == "MemberExpression":
            py_object_expr = self.transform_node(node.get("object"))
            property_node = node.get("property")
            if node.get("computed"):
                py_property_expr = self.transform_node(property_node)
                return f"{py_object_expr}[{py_property_expr}]"
            else:
                js_property_name = property_node.get("name")
                py_property_name = js_property_name 
                return f"{py_object_expr}.{py_property_name}"

        elif node_type == "IfStatement":
            py_test_expr = self.transform_node(node.get("test"))
            py_consequent_block = self._indent_block(self.transform_node(node.get("consequent")))
            py_code = f"if {py_test_expr}:\n{py_consequent_block}"
            alternate_node = node.get("alternate")
            if alternate_node:
                if alternate_node.get("type") == "IfStatement":
                    py_else_if_block = self.transform_node(alternate_node)
                    py_code += f"\nel{py_else_if_block}"
                else:
                    py_alternate_block = self._indent_block(self.transform_node(alternate_node))
                    py_code += f"\nelse:\n{py_alternate_block}"
            return py_code

        elif node_type == "WhileStatement":
            test_code_py = self.transform_node(node.get("test"))
            body_node = node.get("body")
            transformed_body_content_py = self.transform_node(body_node)
            py_loop_lines = []
            py_loop_lines.append(f"while {test_code_py}:")
            indented_while_body_py = self._indent_block(transformed_body_content_py)
            py_loop_lines.append(indented_while_body_py)
            return "\n".join(py_loop_lines)
        
        elif node_type == "ForStatement":
            init_code_py = ""
            if node.get("init"): init_code_py = self.transform_node(node.get("init")) 
            test_code_py = "True"
            if node.get("test"): test_code_py = self.transform_node(node.get("test"))
            update_code_py = ""
            if node.get("update"): update_code_py = self.transform_node(node.get("update"))
            body_node = node.get("body")
            transformed_body_content_py = self.transform_node(body_node)
            py_loop_lines = []
            if init_code_py: py_loop_lines.append(init_code_py)
            while_body_statements = []
            if transformed_body_content_py and transformed_body_content_py.strip() != "pass":
                while_body_statements.extend(transformed_body_content_py.splitlines())
            if update_code_py:
                while_body_statements.append(update_code_py)
            if not while_body_statements: indented_while_body_py = self._indent_block("pass")
            else: indented_while_body_py = self._indent_block("\n".join(while_body_statements))
            py_loop_lines.append(f"while {test_code_py}:")
            py_loop_lines.append(indented_while_body_py)
            return "\n".join(py_loop_lines)
            
        elif node_type == "ForOfStatement":
            # Handle for...of loops (JavaScript's iteration over iterable objects)
            left_node = node.get("left")
            right_node = node.get("right")
            body_node = node.get("body")
            
            # Get the variable name or pattern
            var_name = ""
            if left_node.get("type") == "VariableDeclaration":
                # Extract variable name from declaration
                declarations = left_node.get("declarations", [])
                if declarations and len(declarations) > 0:
                    id_node = declarations[0].get("id")
                    if id_node and id_node.get("type") == "Identifier":
                        var_name = self._transform_identifier_name(id_node.get("name", "item"))
                    else:
                        var_name = "item"  # Default if we can't extract the name
                else:
                    var_name = "item"  # Default if no declarations
            elif left_node.get("type") == "Identifier":
                var_name = self._transform_identifier_name(left_node.get("name", "item"))
            else:
                var_name = "item"  # Default fallback
            
            # Transform the iterable expression
            iterable_py = self.transform_node(right_node)
            
            # Transform the loop body
            body_py = self.transform_node(body_node)
            indented_body_py = self._indent_block(body_py)
            
            # Create Python for loop
            return f"for {var_name} in {iterable_py}:\n{indented_body_py}"

        elif node_type == "BlockStatement":
            py_block_statements = [self.transform_node(stmt) for stmt in node.get("body", [])]
            py_block_statements_filtered = [s for s in py_block_statements if s and s.strip()]
            if not py_block_statements_filtered:
                return "pass"
            return "\n".join(py_block_statements_filtered)

        elif node_type == "FunctionDeclaration":
            js_func_name = node.get("id", {}).get("name", "_anonymous_function")
            py_func_name = self._transform_identifier_name(js_func_name)
            js_params = node.get("params", [])
            py_params = [self._transform_identifier_name(p.get("name")) for p in js_params]
            py_body_content = self.transform_node(node.get("body"))
            py_indented_body = self._indent_block(py_body_content)
            return f"def {py_func_name}({', '.join(py_params)}):\n{py_indented_body}"

        elif node_type == "ArrowFunctionExpression":
            js_params_nodes = node.get("params", [])
            py_params = [self._transform_identifier_name(p.get("name")) for p in js_params_nodes]
            body_node = node.get("body")
            if body_node.get("type") != "BlockStatement":
                py_expression_body = self.transform_node(body_node)
                return f"lambda {', '.join(py_params)}: {py_expression_body}"
            else:
                py_block_statements_content = self.transform_node(body_node)
                py_indented_body = self._indent_block(py_block_statements_content)
                original_js_params_str = ', '.join([p.get('name', '_param') for p in js_params_nodes])
                return (f"# JS Arrow Function with a block body: ({original_js_params_str}) => {{...}}\n"
                        f"# Python's lambdas are single-expression only; manual refactoring is needed.\n"
                        f"# Approximate 'def' structure:\n"
                        f"# def _generated_arrow_func({', '.join(py_params)}):\n"
                        f"{py_indented_body}")

        elif node_type == "ReturnStatement":
            argument_node = node.get("argument")
            if argument_node:
                py_return_value = self.transform_node(argument_node)
                return f"return {py_return_value}"
            else:
                return "return None"

        elif node_type == "BinaryExpression":
            py_left = self.transform_node(node.get("left"))
            js_operator = node.get("operator")
            py_right = self.transform_node(node.get("right"))
            operator_map = {
                "===": "==", "!==": "!=", "==": "==", "!=": "!=",
                "&&": "and", "||": "or",
                "+": "+", "-": "-", "*": "*", "/": "/", "%": "%", "**": "**",
                "&": "&", "|": "|", "^": "^", "<<": "<<", ">>": ">>",
                "<": "<", "<=": "<=", ">": ">", ">=": ">="
            }
            py_operator = operator_map.get(js_operator, f" # JS_OPERATOR: {js_operator} # ")
            return f"{py_left} {py_operator} {py_right}"

        elif node_type == "UnaryExpression":
            js_operator = node.get("operator")
            py_argument = self.transform_node(node.get("argument"))
            if js_operator == "!": return f"not {py_argument}"
            if js_operator == "typeof": return f"type({py_argument}).__name__"
            if js_operator == "delete": return f"del {py_argument}"
            if js_operator in ["+", "-"]: return f"{js_operator}{py_argument}"
            if js_operator == "~": return f"~{py_argument}"
            if js_operator == "void": return f"({py_argument}, None)[1]"
            else: return f"{js_operator}{py_argument}"

        elif node_type == "UpdateExpression":
             argument_node = node.get("argument")
             py_arg_name = self.transform_node(argument_node)
             js_operator = node.get("operator")
             if js_operator == "++":
                 return f"{py_arg_name} += 1"
             elif js_operator == "--":
                 return f"{py_arg_name} -= 1"
             else:
                 return f"# UNHANDLED_JS_UPDATE_OPERATOR: {js_operator}"

        elif node_type == "AssignmentExpression":
            left_node = node.get("left")
            py_left_operand = self.transform_node(left_node)
            js_operator = node.get("operator")
            right_node = node.get("right")
            py_right_operand = self.transform_node(right_node)
            if js_operator == ">>>=":
                self.imports.add("import ctypes")
                return f"{py_left_operand} = ({py_left_operand} >> {py_right_operand}) if {py_left_operand} >= 0 else ((({py_left_operand} & 0xFFFFFFFF) >> {py_right_operand}))"
            py_operator = js_operator 
            return f"{py_left_operand} {py_operator} {py_right_operand}"
            
        elif node_type == "LogicalExpression":
            py_left = self.transform_node(node.get("left"))
            js_operator = node.get("operator")
            py_right = self.transform_node(node.get("right"))
            
            # Map JavaScript logical operators to Python
            if js_operator == "&&":
                return f"{py_left} and {py_right}"
            elif js_operator == "||":
                return f"{py_left} or {py_right}"
            elif js_operator == "??":
                # Nullish coalescing operator - use Python's or with None check
                # We need to use a variable name that won't conflict with user code
                var_name = "_tmp_nullish_check"
                return f"(lambda {var_name}={py_left}: {var_name} if {var_name} is not None else {py_right})()"
            else:
                return f"# UNKNOWN_LOGICAL_OPERATOR: {js_operator} # ({py_left}, {py_right})"

        else:
            return f"# ASTNODE_TRANSFORMER_UNSUPPORTED_TYPE: {node_type}"

def transpile_js_to_python(js_code_str: str):
    if not os.path.exists(PARSER_SCRIPT_PATH):
        err_msg = f"Node.js parser script not found at '{PARSER_SCRIPT_PATH}'."
        return None, err_msg
    node_executable = 'node'
    try:
        process = subprocess.Popen(
            [node_executable, PARSER_SCRIPT_PATH],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', cwd=PROJECT_ROOT
        )
        stdout_data, stderr_data = process.communicate(input=js_code_str, timeout=15)
        if process.returncode != 0:
            error_details_from_node = stderr_data.strip()
            try:
                babel_error_json = json.loads(stderr_data)
                error_details_from_node = babel_error_json.get('message', error_details_from_node) 
                loc_line = babel_error_json.get('loc', {}).get('line', 'N/A')
                error_details_from_node = f"{error_details_from_node} (JS Line: {loc_line})"
                if babel_error_json.get('error') == "NodeScriptUncaughtException":
                     error_details_from_node = f"Uncaught Exception in Node.js parser script: {babel_error_json.get('message', error_details_from_node)}"
            except json.JSONDecodeError: pass
            err_msg = f"JS Parsing Error (Node failed code {process.returncode}): {error_details_from_node}"
            return None, err_msg
        try:
            js_ast = json.loads(stdout_data)
        except json.JSONDecodeError as e_json_ast:
            err_msg = f"Could not decode JSON AST. Stdout: '{stdout_data[:500]}...'. JSON Error: {e_json_ast}"
            return None, err_msg
        if "errors" in js_ast and js_ast["errors"]:
            babel_errors_list = [f"'{e.get('reasonCode')}' Line {e.get('loc',{}).get('line','?')}: {e.get('message')}" for e in js_ast["errors"]]
            err_msg = "JS Parsing Issues (Babel recovered):\n" + "\n".join(babel_errors_list)
            return None, err_msg
        transformer = ASTNodeTransformer()
        python_code = transformer.transform_node(js_ast.get("program"))
        return python_code, None
    except FileNotFoundError:
        err_msg = f"'{node_executable}' not found. Is Node.js in PATH?"
        return None, err_msg
    except subprocess.TimeoutExpired:
        err_msg = "Node.js parser timed out (15s)."
        return None, err_msg
    except Exception as e_unexpected_python:
        err_msg = f"Unexpected Python error: {type(e_unexpected_python).__name__} - {e_unexpected_python}"
        traceback.print_exc()
        return None, err_msg

if __name__ == '__main__':
    test_cases = {
        "All Features Test": """
            let message = "Test";
            message += "ing assignments!";
            console.log(message);

            const config = {
                setting: true,
                value: (10 + 5) * 2,
                "complex-key": "works",
                user: { name: "Dev", level: null }
            };
            console.log(config.user.name);

            let numbers = [10, 20, config.value, config["complex-key"]];
            console.log(numbers[0]);
            console.log(numbers[numbers.length -1]); // Note: .length is not yet handled by transformer

            function power(base, exp) {
                let result = 1;
                for (let i = 0; i < exp; i++) {
                    result *= base;
                }
                return result;
            }
            console.log(power(2, 3));

            let counter = 3;
            while (counter > 0) {
                console.log(counter);
                counter--;
            }
            
            const isBig = (val) => val > 100;
            let check = isBig(power(5,2)); // 25 > 100 = false
            console.log(check);

            if (config.setting && !check || numbers[0] === 10) {
                console.log("Condition met!");
            } else {
                console.log("Condition not met.");
            }
        """
    }
    for test_name, js_code_input in test_cases.items():
        print(f"\n{'='*5} TESTING CASE: {test_name} {'='*5}")
        print(f"--- Input JS: ---\n{js_code_input}\n--------------------")
        py_code_output, error_output = transpile_js_to_python(js_code_input)
        if error_output:
            print(f"--- RESULT (Error): ---\n{error_output}")
        else:
            print(f"--- RESULT (Python Code): ---\n{py_code_output}")
        print(f"--- END OF TEST CASE: {test_name} ---\n")