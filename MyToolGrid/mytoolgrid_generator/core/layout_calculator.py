"""Layout calculator for multi-tile assemblies"""

from typing import List, Dict, Tuple


class LayoutCalculator:
    """Calculate optimal tile layout for given total dimensions"""
    
    STANDARD_TILE_SIZE = 100.0  # mm
    
    def __init__(self, total_width: float, total_length: float):
        self.total_width = total_width
        self.total_length = total_length
        self.layout = self._calculate_layout()
    
    def _calculate_layout(self) -> List[Dict]:
        """Calculate tile layout breakdown"""
        
        # Calculate how many full 100mm tiles fit
        full_tiles_x = int(self.total_length // self.STANDARD_TILE_SIZE)
        full_tiles_y = int(self.total_width // self.STANDARD_TILE_SIZE)
        
        # Calculate remaining edge dimensions
        remainder_x = self.total_length % self.STANDARD_TILE_SIZE
        remainder_y = self.total_width % self.STANDARD_TILE_SIZE
        
        tiles = []
        
        # Standard 100×100mm tiles
        if full_tiles_x > 0 and full_tiles_y > 0:
            tiles.append({
                'type': 'standard',
                'dimensions': (self.STANDARD_TILE_SIZE, self.STANDARD_TILE_SIZE),
                'quantity': full_tiles_x * full_tiles_y,
                'positions': self._get_standard_positions(full_tiles_x, full_tiles_y),
                'description': 'Standard tile'
            })
        
        # Right edge tiles (remainder_x × 100)
        if remainder_x > 0 and full_tiles_y > 0:
            tiles.append({
                'type': 'edge_right',
                'dimensions': (remainder_x, self.STANDARD_TILE_SIZE),
                'quantity': full_tiles_y,
                'positions': self._get_right_edge_positions(full_tiles_x, full_tiles_y),
                'description': 'Right edge tile'
            })
        
        # Top edge tiles (100 × remainder_y)
        if remainder_y > 0 and full_tiles_x > 0:
            tiles.append({
                'type': 'edge_top',
                'dimensions': (self.STANDARD_TILE_SIZE, remainder_y),
                'quantity': full_tiles_x,
                'positions': self._get_top_edge_positions(full_tiles_x, full_tiles_y),
                'description': 'Top edge tile'
            })
        
        # Corner tile (remainder_x × remainder_y)
        if remainder_x > 0 and remainder_y > 0:
            tiles.append({
                'type': 'corner',
                'dimensions': (remainder_x, remainder_y),
                'quantity': 1,
                'positions': [(full_tiles_x, full_tiles_y)],
                'description': 'Corner tile'
            })
        
        # Special case: dimensions smaller than standard tile
        if full_tiles_x == 0 and full_tiles_y == 0:
            tiles.append({
                'type': 'custom',
                'dimensions': (self.total_length, self.total_width),
                'quantity': 1,
                'positions': [(0, 0)],
                'description': 'Custom single tile'
            })
        
        return tiles
    
    def _get_standard_positions(self, cols: int, rows: int) -> List[Tuple[int, int]]:
        """Get grid positions for standard tiles"""
        return [(x, y) for y in range(rows) for x in range(cols)]
    
    def _get_right_edge_positions(self, full_cols: int, full_rows: int) -> List[Tuple[int, int]]:
        """Get positions for right edge tiles"""
        return [(full_cols, y) for y in range(full_rows)]
    
    def _get_top_edge_positions(self, full_cols: int, full_rows: int) -> List[Tuple[int, int]]:
        """Get positions for top edge tiles"""
        return [(x, full_rows) for x in range(full_cols)]
    
    def get_unique_tiles(self) -> List[Dict]:
        """Return list of unique tile geometries to generate"""
        return [
            {
                'dimensions': tile['dimensions'],
                'quantity': tile['quantity'],
                'type': tile['type'],
                'description': tile['description']
            }
            for tile in self.layout
        ]
    
    def get_total_tile_count(self) -> int:
        """Get total number of physical tiles needed"""
        return sum(tile['quantity'] for tile in self.layout)
    
    def get_unique_count(self) -> int:
        """Get number of unique tile geometries"""
        return len(self.layout)
    
    def generate_layout_diagram(self) -> str:
        """Generate ASCII art layout diagram"""
        
        lines = []
        lines.append("\nLayout Diagram:")
        lines.append("=" * 60)
        lines.append(f"Total dimensions: {self.total_length}mm × {self.total_width}mm")
        lines.append(f"Total tiles: {self.get_total_tile_count()}")
        lines.append(f"Unique geometries: {self.get_unique_count()}\n")
        
        # List tiles
        for i, tile in enumerate(self.layout, 1):
            dims = tile['dimensions']
            lines.append(f"  {i}. {tile['description']}: {dims[0]:.0f}×{dims[1]:.0f}mm (qty: {tile['quantity']})")
        
        return "\n".join(lines)
    
    def get_summary(self) -> Dict:
        """Get layout summary information"""
        return {
            'total_dimensions': (self.total_length, self.total_width),
            'total_tiles': self.get_total_tile_count(),
            'unique_geometries': self.get_unique_count(),
            'tiles': self.get_unique_tiles()
        }
