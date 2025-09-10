#!/usr/bin/env python3
"""
Testing Multi-way Interactions in fiasto-py
Similar to the Rust test but checking Python object output
"""

import fiasto_py
from pprint import pprint

def test_multiway_interactions():
    """Test multi-way interactions in fiasto-py"""
    print("Testing Multi-way Interactions in fiasto-py")
    print("===========================================")
    print()

    # Test 2-way interaction
    print("=== Testing 2-way interaction ===")
    formula2 = "y ~ x1*x2"
    print(f"Formula: {formula2}")
    print("Expected: [x1, x2, x1_x2]")
    
    try:
        result = fiasto_py.parse_formula(formula2)
        print("✓ Parsed successfully!")
        
        # Extract generated columns
        generated_cols = result.get('all_generated_columns', [])
        print(f"Generated columns: {generated_cols}")
        
        # Check for expected interactions
        expected_cols = ['y', 'intercept', 'x1', 'x2', 'x1_x2']
        missing_cols = [col for col in expected_cols if col not in generated_cols]
        if missing_cols:
            print(f"⚠️  Missing expected columns: {missing_cols}")
        else:
            print("✓ All expected columns present!")
            
        # Show interaction details
        x1_interactions = result['columns']['x1'].get('interactions', [])
        print(f"x1 interactions: {len(x1_interactions)}")
        for interaction in x1_interactions:
            print(f"  - Order {interaction['order']}: {interaction['with']}")
            
    except Exception as e:
        print(f"✗ Error parsing formula: {e}")
    
    print()

    # Test 3-way interaction
    print("=== Testing 3-way interaction ===")
    formula3 = "y ~ x1*x2*x3"
    print(f"Formula: {formula3}")
    print("Expected: [x1, x2, x3, x1_x2, x1_x3, x2_x3, x1_x2_x3]")
    
    try:
        result = fiasto_py.parse_formula(formula3)
        print("✓ Parsed successfully!")
        
        # Extract generated columns
        generated_cols = result.get('all_generated_columns', [])
        print(f"Generated columns: {generated_cols}")
        
        # Check for expected interactions
        expected_cols = ['y', 'intercept', 'x1', 'x2', 'x3', 'x1_x2', 'x1_x3', 'x2_x3', 'x1_x2_x3']
        missing_cols = [col for col in expected_cols if col not in generated_cols]
        if missing_cols:
            print(f"⚠️  Missing expected columns: {missing_cols}")
        else:
            print("✓ All expected columns present!")
            
        # Show interaction details for x1
        x1_interactions = result['columns']['x1'].get('interactions', [])
        print(f"x1 interactions: {len(x1_interactions)}")
        for interaction in x1_interactions:
            print(f"  - Order {interaction['order']}: {interaction['with']}")
            
    except Exception as e:
        print(f"✗ Error parsing formula: {e}")
    
    print()

    # Test 4-way interaction
    print("=== Testing 4-way interaction ===")
    formula4 = "y ~ x1*x2*x3*x4"
    print(f"Formula: {formula4}")
    print("Expected: [x1, x2, x3, x4, x1_x2, x1_x3, x1_x4, x2_x3, x2_x4, x3_x4, x1_x2_x3, x1_x2_x4, x1_x3_x4, x2_x3_x4, x1_x2_x3_x4]")
    
    try:
        result = fiasto_py.parse_formula(formula4)
        print("✓ Parsed successfully!")
        
        # Extract generated columns
        generated_cols = result.get('all_generated_columns', [])
        print(f"Generated columns ({len(generated_cols)}): {generated_cols}")
        
        # Check for expected interactions
        expected_cols = [
            'y', 'intercept', 'x1', 'x2', 'x3', 'x4',
            'x1_x2', 'x1_x3', 'x1_x4', 'x2_x3', 'x2_x4', 'x3_x4',
            'x1_x2_x3', 'x1_x2_x4', 'x1_x3_x4', 'x2_x3_x4',
            'x1_x2_x3_x4'
        ]
        missing_cols = [col for col in expected_cols if col not in generated_cols]
        if missing_cols:
            print(f"⚠️  Missing expected columns: {missing_cols}")
        else:
            print("✓ All expected columns present!")
            
        # Show interaction details for x1
        x1_interactions = result['columns']['x1'].get('interactions', [])
        print(f"x1 interactions: {len(x1_interactions)}")
        for interaction in x1_interactions:
            print(f"  - Order {interaction['order']}: {interaction['with']}")
            
        # Count total interactions
        total_interactions = sum(
            len(col_data.get('interactions', []))
            for col_data in result['columns'].values()
        )
        print(f"Total interactions across all variables: {total_interactions}")
            
    except Exception as e:
        print(f"✗ Error parsing formula: {e}")

def test_interaction_details():
    """Test detailed interaction information"""
    print("\n" + "="*50)
    print("Testing Interaction Details")
    print("="*50)
    
    formula = "y ~ x1*x2*x3"
    print(f"Formula: {formula}")
    
    try:
        result = fiasto_py.parse_formula(formula)
        
        # Show detailed interaction information for each variable
        for var_name, var_data in result['columns'].items():
            if var_name == 'y':  # Skip response variable
                continue
                
            interactions = var_data.get('interactions', [])
            if interactions:
                print(f"\n{var_name} interactions:")
                for i, interaction in enumerate(interactions, 1):
                    print(f"  {i}. Order {interaction['order']}: {interaction['with']}")
                    print(f"     Context: {interaction['context']}")
                    print(f"     Grouping: {interaction.get('grouping_variable', 'None')}")
            else:
                print(f"\n{var_name}: No interactions")
                
    except Exception as e:
        print(f"✗ Error: {e}")

def test_lexing():
    """Test lexing of multi-way interactions"""
    print("\n" + "="*50)
    print("Testing Lexing of Multi-way Interactions")
    print("="*50)
    
    formulas = [
        "y ~ x1*x2",
        "y ~ x1*x2*x3", 
        "y ~ x1*x2*x3*x4"
    ]
    
    for formula in formulas:
        print(f"\nFormula: {formula}")
        try:
            tokens = fiasto_py.lex_formula(formula)
            print("✓ Lexed successfully!")
            print(f"Tokens ({len(tokens)}):")
            for i, token in enumerate(tokens, 1):
                print(f"  {i}. {token['lexeme']} -> {token['token']}")
        except Exception as e:
            print(f"✗ Error lexing: {e}")

if __name__ == "__main__":
    test_multiway_interactions()
    test_interaction_details()
    test_lexing()
    print("\n🎉 Multi-way interaction tests completed!")
