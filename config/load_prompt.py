"""Load AI system prompt from file"""
from pathlib import Path

def load_system_prompt() -> str:
    """Load the AI system prompt from the configuration file"""
    prompt_file = Path(__file__).parent / "ai_system_prompt.txt"
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # Fallback to basic prompt if file not found
        return """You are an expert FreeCAD architect. Generate clean, professional FreeCAD Python code.
        
- Create integrated building structures, not separate boxes
- Use realistic proportions and dimensions
- Follow architectural standards
- Include proper imports and document setup
- Add materials and colors appropriately
- End with doc.recompute() and ViewFit"""
