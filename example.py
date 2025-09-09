#!/usr/bin/env python3
"""
Example usage of fiasto-py
Demonstrates how to use the parse_formula and lex_formula functions.
"""

import json
import fiasto_py

def print_json_pretty(data, title):
    """Print JSON data in a pretty format"""
    print(f"\n{'='*50}")
    print(f"📊 {title}")
    print('='*50)
    print(json.dumps(data, indent=2))

def main():
    """Main example function"""
    print("🥭 fiasto-py Example Usage")
    print("=" * 50)
    
    # Example formulas to test
    formulas = [
        "y ~ x1 + x2",
        "y ~ x1 * x2 + s(z)",
        "y ~ x1 + x2 + (1|group)",
        "y ~ x1 * x2 + s(z) + (1+x1|group)",
        "mvbind(y1, y2) ~ x * z + (1|g)",
        "y ~ a1 - a2^x, a1 ~ 1, a2 ~ x + (x|g), nl = TRUE"
    ]
    
    for i, formula in enumerate(formulas, 1):
        print(f"\n🔍 Example {i}: {formula}")
        print("-" * 60)
        
        try:
            # Parse the formula
            parsed_result = fiasto_py.parse_formula(formula)
            print_json_pretty(parsed_result, f"Parsed Result for: {formula}")
            
            # Lex the formula
            lexed_result = fiasto_py.lex_formula(formula)
            print_json_pretty(lexed_result, f"Lexed Tokens for: {formula}")
            
        except Exception as e:
            print(f"❌ Error processing formula '{formula}': {e}")
    
    print(f"\n{'='*50}")
    print("🎉 Example completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
