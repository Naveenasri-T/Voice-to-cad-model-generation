#!/usr/bin/env python3
"""
Advanced Code Cleaner - Remove all non-code content
"""
import re
import ast

def ultra_clean_code(raw_code):
    """Ultra aggressive code cleaning to remove ALL explanatory content"""
    
    if not raw_code:
        return ""
    
    # First pass: Remove code blocks and obvious non-code
    cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = cleaned.replace("```", "")
    
    # Split into lines
    lines = cleaned.split('\n')
    pure_code_lines = []
    
    # Track if we're inside a valid Python block
    in_code_block = False
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Skip completely empty lines in between
        if not stripped:
            if in_code_block:
                pure_code_lines.append('')
            continue
        
        # Aggressive filtering of explanatory sentences
        is_explanation = (
            # Starts with explanatory words
            any(stripped.lower().startswith(word) for word in [
                'you can', 'this is', 'this will', 'this creates', 'the model',
                'here', 'note that', 'also', 'additionally', 'furthermore',
                'to make', 'for example', 'we use', 'we create', 'let\'s',
                'first', 'next', 'then', 'finally', 'however', 'therefore'
            ]) or
            # Contains explanatory phrases
            any(phrase in stripped.lower() for phrase in [
                'you can also', 'you can use', 'to create custom', 'module to create',
                'customize the code', 'add more features', 'make the model more',
                'realistic and detailed', 'custom gui elements'
            ]) or
            # Looks like documentation
            (stripped.startswith('"') and stripped.endswith('"') and len(stripped) > 20) or
            # Contains backticks (markdown)
            '`' in stripped or
            # Long sentences without code syntax
            (len(stripped) > 50 and '=' not in stripped and 'FreeCAD' not in stripped and 
             'Part.' not in stripped and 'doc.' not in stripped and not stripped.startswith('#'))
        )
        
        # If it's an explanation, skip it
        if is_explanation:
            continue
            
        # Check if it's valid Python-like syntax
        is_valid_python = (
            stripped.startswith('#') or                    # Comment
            'import ' in stripped or                       # Import
            'FreeCAD' in stripped or                      # FreeCAD API
            'Part.' in stripped or                        # Part module
            'Draft.' in stripped or                       # Draft module  
            'doc.' in stripped or                         # Document calls
            '=' in stripped or                            # Assignment
            stripped in ['pass', 'True', 'False', 'None'] or
            stripped.startswith(('try:', 'except', 'if ', 'for ', 'while ', 'def ', 'class ')) or
            stripped.endswith(':') or                     # Block start
            (line.startswith('    ') and len(stripped) > 0) or  # Indented code
            stripped.endswith(')') or                     # Function call end
            any(char in stripped for char in ['(', ')', '[', ']', '{', '}'])  # Contains brackets
        )
        
        if is_valid_python:
            pure_code_lines.append(line)
            in_code_block = True
        
    # Final result
    result = '\n'.join(pure_code_lines)
    
    # Remove any remaining problematic patterns with regex
    result = re.sub(r'\n\s*You .*?\n', '\n', result, flags=re.IGNORECASE | re.DOTALL)
    result = re.sub(r'\n.*?customize.*?\n', '\n', result, flags=re.IGNORECASE)
    result = re.sub(r'\n.*?realistic.*?detailed.*?\n', '\n', result, flags=re.IGNORECASE)
    result = re.sub(r'\n.*?`.*?`.*?\n', '\n', result)  # Remove lines with backticks
    
    # Fix incomplete variable names (like "bath2_wall_")
    lines = result.split('\n')
    fixed_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Check for incomplete variable names ending with underscore
        if stripped and not any(op in stripped for op in ['=', '(', ')', '.', 'import']):
            # If it's just a variable name ending with underscore, skip it
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*_$', stripped):
                print(f"🔧 Removing incomplete variable name: {stripped}")
                continue
        fixed_lines.append(line)
    
    result = '\n'.join(fixed_lines)
    
    # Validate the result by trying to parse it
    try:
        ast.parse(result)
        print("✅ Generated code is syntactically valid")
    except SyntaxError as e:
        print(f"❌ Syntax error still present: {e}")
        # Try to remove the problematic line
        lines = result.split('\n')
        if e.lineno and e.lineno <= len(lines):
            print(f"🔧 Removing problematic line {e.lineno}: {lines[e.lineno-1][:100]}")
            lines.pop(e.lineno-1)
            result = '\n'.join(lines)
    
    return result.strip()

# Test the cleaner
if __name__ == "__main__":
    # Test with sample problematic code
    test_code = '''import FreeCAD, Part, Draft, FreeCADGui

# Create document
doc = FreeCAD.newDocument("Test")

# Create a box
box = doc.addObject("Part::Feature", "Box")
box.Shape = Part.makeBox(1000, 1000, 1000)

You can also use the `Part` module to create custom shapes and the `Draft` module to create custom 2D drawings.

You can customize the code to add more features.
'''
    
    print("🧹 Testing Ultra Code Cleaner...")
    print("Input:")
    print(test_code)
    print("\n" + "="*50)
    print("Cleaned Output:")
    cleaned = ultra_clean_code(test_code)
    print(cleaned)