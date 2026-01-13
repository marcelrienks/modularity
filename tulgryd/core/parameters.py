"""Parameter management for tulgryd generator"""

import json
from typing import Optional, Dict, Any
from pathlib import Path


class Parameters:
    """Manages all parameters for tile generation"""
    
    def __init__(self):
        # Base geometry (standard 100x100mm tile defaults)
        self.plate_length = 100.0
        self.plate_width = 100.0
        self.plate_thickness = 6.0
        self.perimeter_wall_thickness = 2.0
        self.perimeter_wall_height = 3.5
        self.top_layer_thickness = 2.5
        
        # Interior grid
        self.grid_spacing = 10.0
        self.offset_x = 5.0
        self.offset_y = 5.0
        self.hole_diameter = 4.0
        self.cylinder_diameter = 7.0
        
        # Edge features
        self.tab_diameter = 3.8
        self.tab_radius = 1.9
        self.slot_diameter = 4.0
        self.slot_radius = 2.0
        self.edge_feature_spacing = 10.0
        self.edge_feature_start = 10.0
        
        # Derived values
        self.grid_rows = 0
        self.grid_cols = 0
        self._recalculate_grid()
    
    def _recalculate_grid(self):
        """Calculate grid size based on tile dimensions"""
        # Calculate how many holes fit with spacing
        available_width = self.plate_width - (2 * self.offset_y)
        available_length = self.plate_length - (2 * self.offset_x)
        
        self.grid_cols = int(available_length / self.grid_spacing) + 1
        self.grid_rows = int(available_width / self.grid_spacing) + 1
    
    def set_dimensions(self, width: float, length: float):
        """Set tile dimensions and recalculate derived values"""
        self.plate_width = width
        self.plate_length = length
        self._recalculate_grid()
    
    def calculate_edge_features(self) -> Dict[str, list]:
        """Calculate tab and slot positions for current dimensions"""
        positions = {
            'width_positions': [],
            'length_positions': []
        }
        
        # Width positions (for left/right edges)
        pos = self.edge_feature_start
        while pos <= self.plate_width - self.edge_feature_start:
            positions['width_positions'].append(pos)
            pos += self.edge_feature_spacing
        
        # Length positions (for top/bottom edges)
        pos = self.edge_feature_start
        while pos <= self.plate_length - self.edge_feature_start:
            positions['length_positions'].append(pos)
            pos += self.edge_feature_spacing
        
        return positions
    
    @classmethod
    def from_json(cls, filepath: str) -> 'Parameters':
        """Load parameters from JSON file"""
        params = cls()
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load base geometry
        if 'base_geometry' in data:
            bg = data['base_geometry']
            params.plate_length = bg.get('plate_length', params.plate_length)
            params.plate_width = bg.get('plate_width', params.plate_width)
            params.plate_thickness = bg.get('plate_thickness', params.plate_thickness)
            params.perimeter_wall_thickness = bg.get('perimeter_wall_thickness', params.perimeter_wall_thickness)
            params.perimeter_wall_height = bg.get('perimeter_wall_height', params.perimeter_wall_height)
            params.top_layer_thickness = bg.get('top_layer_thickness', params.top_layer_thickness)
        
        # Load interior grid
        if 'interior_grid' in data:
            ig = data['interior_grid']
            params.grid_spacing = ig.get('grid_spacing', params.grid_spacing)
            params.offset_x = ig.get('offset_from_left_edge', params.offset_x)
            params.offset_y = ig.get('offset_from_bottom_edge', params.offset_y)
            params.hole_diameter = ig.get('hole_diameter', params.hole_diameter)
            params.cylinder_diameter = ig.get('cylinder_diameter', params.cylinder_diameter)
        
        # Load edge features
        if 'edge_features' in data:
            ef = data['edge_features']
            if 'tabs' in ef:
                params.tab_diameter = ef['tabs'].get('diameter', params.tab_diameter)
                params.tab_radius = ef['tabs'].get('radius', params.tab_radius)
                params.edge_feature_spacing = ef['tabs'].get('spacing', params.edge_feature_spacing)
                params.edge_feature_start = ef['tabs'].get('start_offset', params.edge_feature_start)
            if 'slots' in ef:
                params.slot_diameter = ef['slots'].get('diameter', params.slot_diameter)
                params.slot_radius = ef['slots'].get('radius', params.slot_radius)
        
        params._recalculate_grid()
        return params
    
    def validate(self) -> tuple[bool, str]:
        """Validate parameters meet constraints"""
        
        # Basic dimension checks
        if self.plate_length <= 0 or self.plate_width <= 0:
            return False, "Plate dimensions must be positive"
        
        if self.plate_thickness <= 0:
            return False, "Plate thickness must be positive"
        
        # Relationship checks
        if self.cylinder_diameter <= self.hole_diameter:
            return False, "Cylinder diameter must be larger than hole diameter"
        
        if self.slot_diameter <= self.tab_diameter:
            return False, "Slot diameter must be larger than tab diameter"
        
        if self.grid_spacing <= self.cylinder_diameter:
            return False, "Grid spacing must exceed cylinder diameter"
        
        # Layer height check
        total_height = self.perimeter_wall_height + self.top_layer_thickness
        if abs(total_height - self.plate_thickness) > 0.001:
            return False, f"Layer heights ({total_height}mm) must sum to plate thickness ({self.plate_thickness}mm)"
        
        # Boundary checks
        max_x = self.offset_x + (self.grid_cols - 1) * self.grid_spacing
        max_y = self.offset_y + (self.grid_rows - 1) * self.grid_spacing
        
        if max_x > self.plate_length - self.offset_x:
            return False, "Grid exceeds plate length boundaries"
        
        if max_y > self.plate_width - self.offset_y:
            return False, "Grid exceeds plate width boundaries"
        
        return True, "Valid"
    
    def to_dict(self) -> Dict[str, Any]:
        """Export parameters as dictionary"""
        return {
            'plate_length': self.plate_length,
            'plate_width': self.plate_width,
            'plate_thickness': self.plate_thickness,
            'grid_rows': self.grid_rows,
            'grid_cols': self.grid_cols,
            'total_holes': self.grid_rows * self.grid_cols
        }
