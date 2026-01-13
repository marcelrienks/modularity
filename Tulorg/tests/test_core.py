"""Test suite for MyToolGrid generator"""

import pytest
from core.parameters import Parameters
from core.layout_calculator import LayoutCalculator
from core.builder import ModelBuilder


def test_parameters_default():
    """Test default parameters"""
    params = Parameters()
    assert params.plate_length == 100.0
    assert params.plate_width == 100.0
    assert params.plate_thickness == 6.0
    assert params.grid_rows == 10
    assert params.grid_cols == 10


def test_parameters_validation():
    """Test parameter validation"""
    params = Parameters()
    is_valid, msg = params.validate()
    assert is_valid == True
    
    # Test invalid: cylinder smaller than hole
    params.cylinder_diameter = 3.0
    is_valid, msg = params.validate()
    assert is_valid == False
    assert "Cylinder" in msg


def test_parameters_dimension_change():
    """Test changing dimensions"""
    params = Parameters()
    params.set_dimensions(width=50, length=50)
    assert params.plate_width == 50
    assert params.plate_length == 50
    assert params.grid_rows == 5
    assert params.grid_cols == 5


def test_layout_calculator_standard():
    """Test layout calculator with exact multiples"""
    calc = LayoutCalculator(total_width=200, total_length=200)
    tiles = calc.get_unique_tiles()
    
    # Should be only standard tiles
    assert len(tiles) == 1
    assert tiles[0]['dimensions'] == (100.0, 100.0)
    assert tiles[0]['quantity'] == 4


def test_layout_calculator_with_edges():
    """Test layout calculator with remainders"""
    calc = LayoutCalculator(total_width=180, total_length=250)
    tiles = calc.get_unique_tiles()
    
    # Should have standard, right edge, top edge, and corner
    assert len(tiles) == 4
    assert calc.get_total_tile_count() == 9  # 4 + 2 + 2 + 1


def test_layout_calculator_small():
    """Test layout calculator with dimensions smaller than standard"""
    calc = LayoutCalculator(total_width=75, total_length=50)
    tiles = calc.get_unique_tiles()
    
    # Should be single custom tile
    assert len(tiles) == 1
    assert tiles[0]['dimensions'] == (50, 75)
    assert tiles[0]['quantity'] == 1


def test_edge_feature_calculation():
    """Test tab/slot position calculation"""
    params = Parameters()
    features = params.calculate_edge_features()
    
    # Standard 100mm tile should have 9 positions
    assert len(features['width_positions']) == 9
    assert len(features['length_positions']) == 9
    assert features['width_positions'][0] == 10
    assert features['length_positions'][-1] == 90


def test_edge_feature_calculation_small_tile():
    """Test edge features on small tile"""
    params = Parameters()
    params.set_dimensions(width=45, length=100)
    features = params.calculate_edge_features()
    
    # 45mm width should have fewer positions
    assert len(features['width_positions']) < 9
    assert len(features['length_positions']) == 9


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
