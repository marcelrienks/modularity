"""3D Model builder using CadQuery"""

import cadquery as cq
from .parameters import Parameters
import math


class ModelBuilder:
    """Builds 3D tile models using CadQuery"""
    
    def __init__(self, params: Parameters):
        self.params = params
        self.model = None
    
    def build(self) -> cq.Workplane:
        """Build complete tile model"""
        
        # Validate parameters
        is_valid, msg = self.params.validate()
        if not is_valid:
            raise ValueError(f"Invalid parameters: {msg}")
        
        # Step 1: Create perimeter frame (without cutting slots - only outer geometry)
        perimeter = self._create_perimeter_frame()
        
        # Step 2: Create cylinders
        cylinders = self._create_cylinder_grid()
        
        # Step 3: Union perimeter and cylinders
        combined = perimeter
        for cyl in cylinders:
            combined = combined.union(cyl)
        
        # Step 4: Create top layer
        top_layer = self._create_top_layer()
        combined = combined.union(top_layer)
        
        # Step 5: Create holes (through full thickness)
        combined = self._create_holes(combined)
        
        # Step 6: Create edge slots (through full thickness)
        combined = self._create_edge_slots(combined)
        
        self.model = combined
        return self.model
    
    def _create_perimeter_frame(self) -> cq.Workplane:
        """Create perimeter frame with integrated tabs (slots created separately)"""
        
        p = self.params
        edge_features = p.calculate_edge_features()
        
        # Create outer rectangle
        outer = (cq.Workplane("XY")
                 .rect(p.plate_length, p.plate_width)
                 .extrude(p.perimeter_wall_height))
        
        # Create inner rectangle to subtract
        inner_length = p.plate_length - 2 * p.perimeter_wall_thickness
        inner_width = p.plate_width - 2 * p.perimeter_wall_thickness
        
        inner = (cq.Workplane("XY")
                 .center(0, 0)
                 .rect(inner_length, inner_width)
                 .extrude(p.perimeter_wall_height))
        
        frame = outer.cut(inner)
        
        # Add tabs on top and right edges
        # Top edge tabs (Y = plate_width/2)
        for x_pos in edge_features['length_positions']:
            tab_x = x_pos - p.plate_length / 2
            tab_y = p.plate_width / 2
            tab = (cq.Workplane("XY")
                   .center(tab_x, tab_y)
                   .circle(p.tab_radius)
                   .extrude(p.plate_thickness))
            # Cut half to make semicircle
            cut_box = (cq.Workplane("XY")
                      .center(tab_x, tab_y + p.tab_radius)
                      .rect(p.tab_diameter, p.tab_diameter)
                      .extrude(p.plate_thickness))
            tab = tab.cut(cut_box)
            frame = frame.union(tab)
        
        # Right edge tabs (X = plate_length/2)
        for y_pos in edge_features['width_positions']:
            tab_x = p.plate_length / 2
            tab_y = y_pos - p.plate_width / 2
            tab = (cq.Workplane("XY")
                   .center(tab_x, tab_y)
                   .circle(p.tab_radius)
                   .extrude(p.plate_thickness))
            # Cut half to make semicircle
            cut_box = (cq.Workplane("XY")
                      .center(tab_x + p.tab_radius, tab_y)
                      .rect(p.tab_diameter, p.tab_diameter)
                      .extrude(p.plate_thickness))
            tab = tab.cut(cut_box)
            frame = frame.union(tab)
        
        return frame
    
    def _create_cylinder_grid(self) -> list:
        """Create grid of cylinders"""
        
        p = self.params
        cylinders = []
        
        # Position grid starting from offset (5mm from corner)
        # Coordinates relative to tile center (CadQuery default)
        start_x = -p.plate_length / 2 + p.offset_x
        start_y = -p.plate_width / 2 + p.offset_y
        
        for row in range(p.grid_rows):
            for col in range(p.grid_cols):
                x = start_x + col * p.grid_spacing
                y = start_y + row * p.grid_spacing
                
                # Check if cylinder fits within bounds
                if (x + p.cylinder_diameter/2 <= p.plate_length/2 and
                    y + p.cylinder_diameter/2 <= p.plate_width/2):
                    
                    cyl = (cq.Workplane("XY")
                           .center(x, y)
                           .circle(p.cylinder_diameter / 2)
                           .extrude(p.perimeter_wall_height))
                    cylinders.append(cyl)
        
        return cylinders
    
    def _create_top_layer(self) -> cq.Workplane:
        """Create top solid layer"""
        
        p = self.params
        
        top = (cq.Workplane("XY")
               .workplane(offset=p.perimeter_wall_height)
               .rect(p.plate_length, p.plate_width)
               .extrude(p.top_layer_thickness))
        
        return top
    
    def _create_holes(self, model: cq.Workplane) -> cq.Workplane:
        """Create holes through the model"""
        
        p = self.params
        
        # Position grid starting from offset (5mm from corner)
        # Coordinates relative to tile center (CadQuery default)
        start_x = -p.plate_length / 2 + p.offset_x
        start_y = -p.plate_width / 2 + p.offset_y
        
        for row in range(p.grid_rows):
            for col in range(p.grid_cols):
                x = start_x + col * p.grid_spacing
                y = start_y + row * p.grid_spacing
                
                # Check if hole fits within bounds
                if (x + p.hole_diameter/2 <= p.plate_length/2 and
                    y + p.hole_diameter/2 <= p.plate_width/2):
                    
                    hole = (cq.Workplane("XY")
                            .center(x, y)
                            .circle(p.hole_diameter / 2)
                            .extrude(p.plate_thickness))
                    model = model.cut(hole)
        
        return model
    
    def _create_edge_slots(self, model: cq.Workplane) -> cq.Workplane:
        """Create edge slots through full thickness"""
        
        p = self.params
        edge_features = p.calculate_edge_features()
        
        # Bottom edge slots (Y = -plate_width/2)
        for x_pos in edge_features['length_positions']:
            slot_x = x_pos - p.plate_length / 2
            slot_y = -p.plate_width / 2
            slot = (cq.Workplane("XY")
                    .center(slot_x, slot_y)
                    .circle(p.slot_radius)
                    .extrude(p.plate_thickness))
            # Cut half to make semicircle cutout
            cut_box = (cq.Workplane("XY")
                      .center(slot_x, slot_y - p.slot_radius)
                      .rect(p.slot_diameter, p.slot_diameter)
                      .extrude(p.plate_thickness))
            slot = slot.cut(cut_box)
            model = model.cut(slot)
        
        # Left edge slots (X = -plate_length/2)
        for y_pos in edge_features['width_positions']:
            slot_x = -p.plate_length / 2
            slot_y = y_pos - p.plate_width / 2
            slot = (cq.Workplane("XY")
                    .center(slot_x, slot_y)
                    .circle(p.slot_radius)
                    .extrude(p.plate_thickness))
            # Cut half to make semicircle cutout
            cut_box = (cq.Workplane("XY")
                      .center(slot_x - p.slot_radius, slot_y)
                      .rect(p.slot_diameter, p.slot_diameter)
                      .extrude(p.plate_thickness))
            slot = slot.cut(cut_box)
            model = model.cut(slot)
        
        return model
    
    def export_stl(self, filepath: str, tolerance: float = 0.01):
        """Export model to STL"""
        if self.model is None:
            raise ValueError("Model not built yet. Call build() first.")
        
        cq.exporters.export(self.model, filepath, tolerance=tolerance)
    
    def export_step(self, filepath: str):
        """Export model to STEP"""
        if self.model is None:
            raise ValueError("Model not built yet. Call build() first.")
        
        cq.exporters.export(self.model, filepath)
    
    def get_model(self) -> cq.Workplane:
        """Get the built model"""
        return self.model
