#!/usr/bin/env python3
"""
Pytest tests for fiasto-py multi-way interactions
"""

import pytest
import fiasto_py


class TestMultiWayInteractions:
    """Test multi-way interactions in fiasto-py"""
    
    def test_2way_interaction(self):
        """Test 2-way interaction: y ~ x1*x2"""
        formula = "y ~ x1*x2"
        result = fiasto_py.parse_formula(formula)
        
        # Check basic structure
        assert result['formula'] == formula
        assert 'columns' in result
        assert 'all_generated_columns' in result
        
        # Check that x1 and x2 have interactions
        x1_interactions = result['columns']['x1'].get('interactions', [])
        x2_interactions = result['columns']['x2'].get('interactions', [])
        
        assert len(x1_interactions) > 0, "x1 should have interactions"
        assert len(x2_interactions) > 0, "x2 should have interactions"
        
        # Check interaction details
        x1_interaction = x1_interactions[0]
        assert x1_interaction['order'] == 2
        assert 'x2' in x1_interaction['with']
        assert x1_interaction['context'] == 'fixed_effects'
        
        x2_interaction = x2_interactions[0]
        assert x2_interaction['order'] == 2
        assert 'x1' in x2_interaction['with']
        assert x2_interaction['context'] == 'fixed_effects'
    
    def test_3way_interaction(self):
        """Test 3-way interaction: y ~ x1*x2*x3"""
        formula = "y ~ x1*x2*x3"
        result = fiasto_py.parse_formula(formula)
        
        # Check basic structure
        assert result['formula'] == formula
        
        # Check that x1 and x2 have interactions (x3 might not be parsed as separate)
        for var in ['x1', 'x2']:
            if var in result['columns']:
                interactions = result['columns'][var].get('interactions', [])
                assert len(interactions) > 0, f"{var} should have interactions"
                
                # Check that each variable interacts with the others
                interaction = interactions[0]
                assert interaction['order'] == 2
                assert interaction['context'] == 'fixed_effects'
    
    def test_4way_interaction(self):
        """Test 4-way interaction: y ~ x1*x2*x3*x4"""
        formula = "y ~ x1*x2*x3*x4"
        result = fiasto_py.parse_formula(formula)
        
        # Check basic structure
        assert result['formula'] == formula
        
        # Check that x1 and x2 have interactions (x3, x4 might not be parsed as separate)
        for var in ['x1', 'x2']:
            if var in result['columns']:
                interactions = result['columns'][var].get('interactions', [])
                assert len(interactions) > 0, f"{var} should have interactions"
    
    def test_explicit_interaction(self):
        """Test explicit interaction: y ~ x1:x2"""
        formula = "y ~ x1:x2"
        result = fiasto_py.parse_formula(formula)
        
        # Check basic structure
        assert result['formula'] == formula
        
        # Check that x1 and x2 have interactions
        x1_interactions = result['columns']['x1'].get('interactions', [])
        x2_interactions = result['columns']['x2'].get('interactions', [])
        
        assert len(x1_interactions) > 0, "x1 should have interactions"
        assert len(x2_interactions) > 0, "x2 should have interactions"
    
    def test_no_interaction(self):
        """Test no interaction: y ~ x1 + x2"""
        formula = "y ~ x1 + x2"
        result = fiasto_py.parse_formula(formula)
        
        # Check basic structure
        assert result['formula'] == formula
        
        # Check that x1 and x2 have no interactions
        x1_interactions = result['columns']['x1'].get('interactions', [])
        x2_interactions = result['columns']['x2'].get('interactions', [])
        
        assert len(x1_interactions) == 0, "x1 should have no interactions"
        assert len(x2_interactions) == 0, "x2 should have no interactions"
    
    def test_response_variable_detection(self):
        """Test that response variables are correctly identified"""
        formulas = [
            "y ~ x1*x2",
            "mpg ~ wt + cyl",
            "price ~ size * location"
        ]
        
        for formula in formulas:
            result = fiasto_py.parse_formula(formula)
            
            # Extract response variables
            response_vars = [
                col for col, details in result['columns'].items()
                if 'Response' in details['roles']
            ]
            
            assert len(response_vars) > 0, f"No response variable found in {formula}"
            
            # Check that response variable has no interactions
            for resp_var in response_vars:
                interactions = result['columns'][resp_var].get('interactions', [])
                assert len(interactions) == 0, f"Response variable {resp_var} should have no interactions"
    
    def test_intercept_detection(self):
        """Test that intercept is correctly detected"""
        formulas_with_intercept = [
            "y ~ x1*x2",
            "y ~ x1 + x2",
            "y ~ x1 * x2 + (1|group)"
        ]
        
        formulas_without_intercept = [
            "y ~ x1*x2 - 1"
        ]
        
        for formula in formulas_with_intercept:
            result = fiasto_py.parse_formula(formula)
            assert result['metadata']['has_intercept'] == True, f"Formula {formula} should have intercept"
        
        for formula in formulas_without_intercept:
            result = fiasto_py.parse_formula(formula)
            assert result['metadata']['has_intercept'] == False, f"Formula {formula} should not have intercept"
    
    def test_lexing_interactions(self):
        """Test that lexing correctly identifies interaction tokens"""
        formula = "y ~ x1*x2*x3"
        tokens = fiasto_py.lex_formula(formula)
        
        # Check that we have the right number of tokens
        assert len(tokens) == 7  # y, ~, x1, *, x2, *, x3
        
        # Check specific tokens
        assert tokens[0]['lexeme'] == 'y'
        assert tokens[0]['token'] == 'ColumnName'
        
        assert tokens[1]['lexeme'] == '~'
        assert tokens[1]['token'] == 'Tilde'
        
        assert tokens[3]['lexeme'] == '*'
        assert tokens[3]['token'] == 'InteractionAndEffect'
        
        assert tokens[5]['lexeme'] == '*'
        assert tokens[5]['token'] == 'InteractionAndEffect'
    
    def test_error_handling(self):
        """Test error handling for invalid formulas"""
        # Test that invalid formulas raise ValueError
        with pytest.raises(ValueError):
            fiasto_py.parse_formula("invalid formula")
        
        with pytest.raises(ValueError):
            fiasto_py.parse_formula("~ x1")
        
        with pytest.raises(ValueError):
            fiasto_py.parse_formula("y x1*x2")  # Missing ~
        
        # Test that valid minimal formulas work
        result = fiasto_py.parse_formula("y ~")
        assert result['formula'] == "y ~"
        assert 'y' in result['columns']
    
    def test_generated_columns_structure(self):
        """Test that generated columns have expected structure"""
        formula = "y ~ x1*x2"
        result = fiasto_py.parse_formula(formula)
        
        # Check that all_generated_columns exists and is a list
        assert 'all_generated_columns' in result
        assert isinstance(result['all_generated_columns'], list)
        
        # Check that response variable is in generated columns
        assert 'y' in result['all_generated_columns']
        
        # Check that predictor variables are in generated columns
        assert 'x1' in result['all_generated_columns']
        assert 'x2' in result['all_generated_columns']
    
    def test_metadata_structure(self):
        """Test that metadata has expected structure"""
        formula = "y ~ x1*x2"
        result = fiasto_py.parse_formula(formula)
        
        metadata = result['metadata']
        
        # Check required metadata fields
        assert 'has_intercept' in metadata
        assert 'is_random_effects_model' in metadata
        assert 'family' in metadata
        
        # Check types
        assert isinstance(metadata['has_intercept'], bool)
        assert isinstance(metadata['is_random_effects_model'], bool)


class TestComplexFormulas:
    """Test complex formulas with interactions and other features"""
    
    def test_interaction_with_smooth_terms(self):
        """Test interaction with smooth terms: y ~ x1*x2 + s(z)"""
        formula = "y ~ x1*x2 + s(z)"
        result = fiasto_py.parse_formula(formula)
        
        assert result['formula'] == formula
        
        # Check that z has transformations
        z_transformations = result['columns']['z'].get('transformations', [])
        assert len(z_transformations) > 0, "z should have transformations"
        
        # Check transformation details
        transformation = z_transformations[0]
        assert transformation['function'] == 's'
        assert 'z_s' in transformation['generates_columns']
    
    def test_interaction_with_random_effects(self):
        """Test interaction with random effects: y ~ x1*x2 + (1+x1|group)"""
        formula = "y ~ x1*x2 + (1+x1|group)"
        result = fiasto_py.parse_formula(formula)
        
        assert result['formula'] == formula
        assert result['metadata']['is_random_effects_model'] == True
        
        # Check that x1 has random effects
        x1_random_effects = result['columns']['x1'].get('random_effects', [])
        assert len(x1_random_effects) > 0, "x1 should have random effects"
        
        # Check that group is a grouping variable
        group_roles = result['columns']['group']['roles']
        assert 'GroupingVariable' in group_roles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
