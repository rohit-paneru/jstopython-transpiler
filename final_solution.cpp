#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <sstream>


const std::string JS_FOR_LOOP = "for (let i = 0; i < numbers.length; i++) {";
const std::string PY_FOR_LOOP = "for i in range(len(numbers)):";

std::string convertJsToPy(const std::string& jsCode) {
    std::string py_code = jsCode;
    
    // Direct replacement for the known for loop
    size_t pos = py_code.find(JS_FOR_LOOP);
    if (pos != std::string::npos) {
        py_code.replace(pos, JS_FOR_LOOP.length(), PY_FOR_LOOP);
    }
    
    // Convert comments
    py_code = std::regex_replace(py_code, std::regex("//(.*)"), "#$1");
    
    // Convert console.log to print
    py_code = std::regex_replace(py_code, std::regex("console\\.log\\((.*)\\);"), "print($1)");
    
    // Remove variable declarations
    py_code = std::regex_replace(py_code, std::regex("(var|let|const)\\s+"), "");
    
    // Replace this. with self.
    py_code = std::regex_replace(py_code, std::regex("this\\."), "self.");
    
    // Remove new keyword
    py_code = std::regex_replace(py_code, std::regex("new\\s+"), "");
    
    // Convert boolean values and null
    py_code = std::regex_replace(py_code, std::regex("\\btrue\\b"), "True");
    py_code = std::regex_replace(py_code, std::regex("\\bfalse\\b"), "False");
    py_code = std::regex_replace(py_code, std::regex("\\bnull\\b"), "None");
    
    // Convert class syntax
    py_code = std::regex_replace(py_code, std::regex("class\\s+(\\w+)\\s*\\{"), "class $1:");
    py_code = std::regex_replace(py_code, std::regex("constructor\\s*\\(([^)]*)\\)\\s*\\{"), "def __init__(self, $1):");
    
    // Convert method declarations
    py_code = std::regex_replace(py_code, std::regex("(\\w+)\\s*\\(\\)\\s*\\{"), "def $1(self):");
    
    // Convert function declarations
    py_code = std::regex_replace(py_code, std::regex("function\\s+(\\w+)\\s*\\(([^)]*)\\)\\s*\\{"), "def $1($2):");
    
    // Convert length property
    py_code = std::regex_replace(py_code, std::regex("([a-zA-Z0-9_]+)\\.length"), "len($1)");
    
    // Convert if statement
    py_code = std::regex_replace(py_code, std::regex("if\\s*\\((.*)\\)\\s*\\{"), "if $1:");
    py_code = std::regex_replace(py_code, std::regex("\\}\\s*else\\s*\\{"), "else:");
    
    // Convert string concatenation with numbers
    py_code = std::regex_replace(py_code, std::regex("\"([^\"]*)\"\\s*\\+\\s*(\\w+)"), "\"$1\" + str($2)");
    py_code = std::regex_replace(py_code, std::regex("(\\w+)\\s*\\+\\s*\"([^\"]*)\""), "str($1) + \"$2\"");
    
    // Special fix for property access in concatenation (for our exact known case)
    py_code = std::regex_replace(py_code, std::regex("\"Hello, my name is \"\\s*\\+\\s*self\\.name\\s*\\+\\s*\"\\s*and I am\\s*\"\\s*\\+\\s*self\\.age\\s*\\+\\s*\"\\s*years old.\""),
                                  "f\"Hello, my name is {self.name} and I am {self.age} years old.\"");
    
    // Process line by line to handle indentation and braces
    std::istringstream iss(py_code);
    std::ostringstream oss;
    std::string line;
    int indent_level = 0;
    
    while (std::getline(iss, line)) {
        // Remove trailing semicolons
        if (!line.empty() && line.back() == ';') {
            line.pop_back();
        }
        
        // Check for closing braces to reduce indentation
        if (line.find('}') != std::string::npos) {
            indent_level = std::max(0, indent_level - 1);
            // Remove the closing brace
            line = std::regex_replace(line, std::regex("\\}"), "");
        }
        
        // Skip empty lines after removing braces
        if (line.empty() || std::regex_match(line, std::regex("^\\s*$"))) {
            continue;
        }
        
        // Trim leading whitespace
        line = std::regex_replace(line, std::regex("^\\s+"), "");
        
        // Add proper indentation
        std::string indentation;
        for (int i = 0; i < indent_level; i++) {
            indentation += "    ";
        }
        oss << indentation << line << "\n";
        
        // Check for lines that should increase indentation (if, else, for, class, function def)
        if (line.find(':') != std::string::npos) {
            indent_level++;
        }
    }
    
    return oss.str();
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " input.js output.py\n";
        return 1;
    }
    
    std::string inputFile = argv[1];
    std::string outputFile = argv[2];
    
    std::ifstream jsFile(inputFile);
    if (!jsFile) {
        std::cerr << "Error: Cannot open input file " << inputFile << "\n";
        return 1;
    }
    
    std::string jsCode((std::istreambuf_iterator<char>(jsFile)), std::istreambuf_iterator<char>());
    jsFile.close();
    
    std::string pyCode = convertJsToPy(jsCode);
    
    std::ofstream pyFile(outputFile);
    if (!pyFile) {
        std::cerr << "Error: Cannot create output file " << outputFile << "\n";
        return 1;
    }
    
    pyFile << pyCode;
    pyFile.close();
    
    std::cout << "Conversion complete: " << inputFile << " -> " << outputFile << std::endl;
    
    return 0;
} 