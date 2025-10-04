"""
Enhanced code cleaning utilities for Voice-to-CAD application
"""
import re
import py_compile
import tempfile
import os
from utils.logging_config import get_logger

def validate_python_syntax(code_content):
    """Validate that code has proper Python syntax"""
    logger = get_logger("ai")
    
    try:
        # Create temporary file to test compilation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_content)
            temp_filename = f.name
        
        try:
            # Try to compile the code
            py_compile.compile(temp_filename, doraise=True)
            logger.info("Code syntax validation passed")
            return True, "Valid Python syntax"
        except py_compile.PyCompileError as e:
            logger.error(f"Code syntax validation failed: {e}")
            return False, str(e)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    except Exception as e:
        logger.error(f"Error during syntax validation: {e}")
        return False, f"Validation error: {e}"

def super_clean_ai_code(raw_code: str) -> str:
    """Super enhanced AI code cleaning with validation"""
    
    if not raw_code:
        return ""
    
    logger = get_logger("ai")
    logger.info("Starting super code cleaning process")
    
    try:
        # Step 1: Remove code block markers
        cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE | re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
        cleaned = cleaned.replace("```", "")
        
        # Step 2: Split into lines and identify code vs text
        lines = cleaned.split('\n')
        code_lines = []
        in_code_section = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Start of code section detection
            if (stripped.startswith('import ') or 
                stripped.startswith('# Import') or 
                stripped.startswith('# Create') or
                stripped.startswith('from ') or
                'FreeCAD' in stripped):
                in_code_section = True
            
            # Skip explanatory text patterns
            if any(phrase in stripped.lower() for phrase in [
                "here's", "this is", "the following", "note that", "however",
                "instead", "you should", "as shown", "this script will",
                "the model includes", "according to", "requirements"
            ]):
                # This is explanatory text, skip it
                continue
            
            # Include line if we're in code section or it looks like code
            if in_code_section or any(keyword in line for keyword in [
                'import', 'def', 'class', 'doc.', 'Part.', 'FreeCAD', '=', 'Placement'
            ]):
                code_lines.append(line)
        
        # Step 3: Rejoin and clean up
        cleaned = '\n'.join(code_lines)
        
        # Step 4: Remove common artifacts
        artifacts_to_remove = [
            r'^python\s*$',
            r'^Here\'s.*?:\s*$',
            r'^This .*?creates.*?$',
            r'^The .*?includes.*?$',
            r'^Note that.*?$',
            r'^However.*?$'
        ]
        
        for pattern in artifacts_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # Step 5: Clean up empty lines but preserve structure
        lines = cleaned.split('\n')
        final_lines = []
        
        for line in lines:
            if line.strip() or (len(final_lines) > 0 and final_lines[-1].strip()):
                final_lines.append(line)
        
        result = '\n'.join(final_lines).strip()
        
        # Step 6: Validate syntax
        is_valid, validation_message = validate_python_syntax(result)
        
        if is_valid:
            logger.info(f"Super code cleaning successful: {len(result)} characters, syntax valid")
            return result
        else:
            logger.error(f"Cleaned code has invalid syntax: {validation_message}")
            # Return original cleaned version but log the issue
            return result
    
    except Exception as e:
        logger.error(f"Super code cleaning failed: {e}")
        return raw_code  # Return original if cleaning fails

def clean_and_save_generated_code(raw_code: str, filename: str = None) -> tuple:
    """Clean code and save to generated directory with validation"""
    
    from config.settings import get_config
    config = get_config()
    logger = get_logger("ai")
    
    # Clean the code
    clean_code = super_clean_ai_code(raw_code)
    
    # Generate filename if not provided
    if not filename:
        filename = config.get_generated_filename("cleaned_model")
    elif not filename.endswith('.py'):
        filename += '.py'
    
    # Ensure it's in the generated directory
    if not filename.startswith(config.paths.generated_dir):
        filename = os.path.join(config.paths.generated_dir, os.path.basename(filename))
    
    try:
        # Save the cleaned code
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(clean_code)
        
        # Validate the saved file
        is_valid, validation_message = validate_python_syntax(clean_code)
        
        logger.info(f"Code saved to {filename}, syntax valid: {is_valid}")
        
        return filename, is_valid, validation_message
    
    except Exception as e:
        logger.error(f"Failed to save cleaned code: {e}")
        return None, False, str(e)

# Example usage in voice_to_cad.py:
"""
def enhanced_generate_script_with_ai(command_text: str) -> str:
    # Enhanced script generation with super cleaning
    
    # 1. Generate raw code with AI
    response = client.chat.completions.create(...)
    raw_code = response.choices[0].message.content
    
    # 2. Super clean the code with validation
    clean_code = super_clean_ai_code(raw_code)
    
    # 3. Save and validate
    saved_file, is_valid, message = clean_and_save_generated_code(clean_code)
    
    if not is_valid:
        logger = get_logger("ai")
        logger.warning(f"Generated code may have syntax issues: {message}")
    
    return clean_code
"""