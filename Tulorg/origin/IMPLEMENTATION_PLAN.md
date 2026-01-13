# Tulorg - Parametric Script Implementation Plan

## Executive Summary
This document outlines a comprehensive plan for implementing a parameterized script to auto-generate the Tulorg 3D model assembly system. The script accepts **total width and length parameters** and intelligently generates a modular tile layout using standard 100×100mm tiles plus custom edge pieces to exactly fill the specified dimensions. Each unique tile geometry is exported once as an STL file with quantity information in the filename, and a comprehensive assembly guide is auto-generated.

---

## 1. Project Overview

### 1.1 Objectives
- Accept **total width and length** as input parameters
- Calculate optimal tile layout using 100×100mm standard tiles
- Generate custom edge/filler tiles for partial dimensions (<100mm)
- Create unique STL files with quantity-coded filenames (e.g., `tile_100x100_qty4.stl`)
- Auto-generate assembly README with layout diagram and instructions
- Support multiple output formats (STEP, STL, 3MF, OBJ)
- Ensure geometric accuracy and interlocking compatibility
- Provide validation and error checking

### 1.2 Reference Files Analyzed
- ✅ **Tulorg.md** - Detailed technical specifications and measurements
- ✅ **Tulorg.png** - Technical drawing with orthographic views and dimensions
- ✅ **Tulorg.step** - 3D CAD model in STEP AP214 format
- ✅ **parameters.json** - Extracted parameter definitions (NEW)
- ✅ **validation_rules.json** - Geometric constraints and rules (NEW)
- ✅ **geometry_formulas.json** - Mathematical definitions (NEW)

### 1.3 Cross-Verification Results
All three source documents are **consistent**:
- Dimensions match: 100×100×6mm base geometry
- Feature counts confirmed: 100 holes, 18 tabs, 18 slots
- Spacing verified: 10mm grid, 10mm edge feature spacing
- Diameters confirmed: Ø4mm holes, Ø7mm cylinders, Ø3.8mm tabs, Ø4mm slots
- Layer structure validated: 3.5mm + 2.5mm = 6mm total height

---

## 2. Implementation Strategies

### 2.1 Platform Options

#### Option A: Python + CadQuery (RECOMMENDED)
**Advantages:**
- Open-source and free
- Excellent Python integration
- Parametric by nature
- Exports to STEP, STL, 3MF
- Cross-platform (Windows, Linux, Mac)
- Active community support

**Implementation Complexity:** Medium
**Development Time:** 2-3 days

#### Option B: Python + OpenSCAD
**Advantages:**
- Simple syntax
- Fast rendering
- Easy parameter files
- Good for geometric primitives

**Disadvantages:**
- Limited STEP export
- Less precise for complex curves
- No native boolean optimization

**Implementation Complexity:** Low
**Development Time:** 1-2 days

#### Option C: FreeCAD Python Scripting
**Advantages:**
- Full CAD capabilities
- Native STEP support
- GUI for validation
- Parametric modeling

**Disadvantages:**
- Requires FreeCAD installation
- More complex API
- Platform-dependent

**Implementation Complexity:** High
**Development Time:** 3-5 days

#### Option D: Fusion 360 API (JavaScript/Python)
**Advantages:**
- Professional CAD environment
- Excellent parametric features
- Cloud collaboration

**Disadvantages:**
- Requires Fusion 360 license
- Proprietary platform
- Internet connection needed

**Implementation Complexity:** Medium-High
**Development Time:** 3-4 days

### 2.2 Recommended Approach
**Primary:** Python + CadQuery
**Fallback:** Python + OpenSCAD (for STL-only workflows)

---

## 3. Detailed Implementation Plan

### 3.1 Script Architecture

```
tulorg_generator/
├── core/
│   ├── __init__.py
│   ├── parameters.py          # Parameter loading and validation
│   ├── geometry.py            # Geometric calculation functions
│   ├── builder.py             # Main CAD construction logic
│   ├── validator.py           # Constraint checking
│   ├── layout_calculator.py   # NEW: Tile layout optimization
│   └── assembly_guide.py      # NEW: README generation
├── config/
│   ├── default_parameters.json
│   ├── validation_rules.json
│   └── presets/               # Pre-configured variants
│       ├── standard_100x100.json
│       ├── drawer_small_250x180.json
│       └── drawer_large_600x400.json
├── output/
│   └── [timestamp]/           # NEW: Each run creates timestamped directory
│       ├── tile_100x100_qty12.stl
│       ├── tile_edge_100x45_qty2.stl
│       ├── tile_corner_45x45_qty1.stl
│       ├── layout_diagram.txt
│       └── ASSEMBLY_README.md
├── tests/
│   ├── test_parameters.py
│   ├── test_geometry.py
│   ├── test_validation.py
│   ├── test_layout_calculator.py  # NEW
│   └── test_assembly_guide.py     # NEW
├── generate_model.py          # Main CLI script
├── requirements.txt
└── README.md
```

### 3.2 Development Phases

#### Phase 0: Layout Calculator (NEW - Day 1)
**Tasks:**
1. Implement tile layout algorithm for arbitrary dimensions
2. Calculate standard 100×100mm tile count
3. Calculate custom edge piece dimensions
4. Determine unique tile types needed
5. Create assembly layout mapping

**Deliverables:**
- `LayoutCalculator` class
- Tile dimension optimizer
- Layout visualization (ASCII/text diagram)
- Unit tests for various input dimensions

**Validation:**
- 250×180mm → 4 standard + 2 edge pieces correctly calculated
- 315×215mm → proper breakdown verified
- Edge cases handled (exact multiples, very small dimensions)

#### Phase 1: Foundation (Day 1-2)
**Tasks:**
1. Set up project structure
2. Implement parameter loading from JSON
3. Create validation framework
4. Implement geometric calculation functions
5. Write unit tests for calculations

**Deliverables:**
- Parameter class with validation
- Coordinate calculation functions
- Test suite with 90%+ coverage

**Validation:**
- All geometric formulas produce expected coordinates
- Parameter validation catches invalid inputs
- Unit tests pass

#### Phase 2: Core Geometry Builder (Day 2-3)
**Tasks:**
1. Implement perimeter frame sketch with tabs/slots
2. Create cylinder pattern generation with variable grid size
3. Implement two-layer extrusion strategy
4. Add interior hole pattern (variable grid)
5. Boolean union operations
6. Support custom tile dimensions (<100×100mm)

**Deliverables:**
- Working CAD model builder for any tile dimension
- STEP file export
- STL export with proper mesh resolution

**Validation:**
- Generated 100×100mm tile matches reference geometry
- Custom 100×45mm edge tile generates correctly
- Tab/slot alignment verified
- Dimensions within 0.01mm tolerance

#### Phase 3: Multi-Tile Generation & Assembly Guide (Day 4)
**Tasks:**
1. Implement batch tile generation from layout
2. Create unique tile deduplication logic
3. Generate quantity-coded filenames
4. Create assembly guide generator
5. Generate layout diagram (text/ASCII art)

**Deliverables:**
- Batch generation system
- Assembly README auto-generator
- Layout visualization
- Timestamped output directories

**Validation:**
- Example: 250×180mm produces correct file set
- README accurately describes assembly
- Filenames match quantities needed
- All tiles are unique geometries

#### Phase 4: CLI & Multi-Format Export (Day 5)
**Tasks:**
1. Implement multi-format export (STEP, STL, 3MF, OBJ)
2. Add preset configurations
3. Create CLI interface with total dimension arguments
4. Implement batch generation
5. Add progress reporting

**Deliverables:**
- Multi-format export capability
- CLI tool with help system
- Preset library for common drawer sizes

**Validation:**
- All export formats functional
- CLI: `--total-width 250 --total-length 180` works
- Presets generate correct layouts

#### Phase 5: Quality & Documentation (Day 6)
**Tasks:**
1. Comprehensive testing
2. Performance optimization
3. Documentation writing
4. Example gallery generation
5. Error handling improvements

**Deliverables:**
- Complete documentation
- Test coverage report
- Example assemblies for common sizes
- User guide

**Validation:**
- All tests pass
- Documentation complete
- Example models verified

---

## 4. Technical Specifications

### 4.1 Core Algorithms

#### Algorithm 1: Perimeter Frame with Tabs/Slots
```python
def create_perimeter_sketch(params):
    """
    Create 2D profile with integrated tabs and slots
    """
    # Outer rectangle
    outer = rectangle(params.length, params.width)
    
    # Inner rectangle (offset by wall thickness)
    inner = rectangle(
        params.length - 2*params.wall_thickness,
        params.width - 2*params.wall_thickness
    ).translate(params.wall_thickness, params.wall_thickness)
    
    # Subtract inner from outer
    frame = outer - inner
    
    # Add tabs (top and right edges)
    for pos in calculate_tab_positions(params):
        tab = create_semicircle(pos, params.tab_radius, orientation)
        frame = frame + tab
    
    # Subtract slots (bottom and left edges)
    for pos in calculate_slot_positions(params):
        slot = create_semicircle(pos, params.slot_radius, orientation)
        frame = frame - slot
    
    return frame
```

#### Algorithm 2: Layout Calculator (NEW)
```python
class LayoutCalculator:
    """
    Calculate optimal tile layout for given total dimensions
    """
    STANDARD_TILE_SIZE = 100.0  # mm
    
    def __init__(self, total_width, total_length):
        self.total_width = total_width
        self.total_length = total_length
        self.layout = self._calculate_layout()
    
    def _calculate_layout(self):
        """
        Calculate tile layout breakdown
        """
        # Calculate how many full 100mm tiles fit
        full_tiles_x = int(self.total_width // self.STANDARD_TILE_SIZE)
        full_tiles_y = int(self.total_length // self.STANDARD_TILE_SIZE)
        
        # Calculate remaining edge dimensions
        remainder_x = self.total_width % self.STANDARD_TILE_SIZE
        remainder_y = self.total_length % self.STANDARD_TILE_SIZE
        
        tiles = []
        
        # Standard 100×100mm tiles
        if full_tiles_x > 0 and full_tiles_y > 0:
            tiles.append({
                'type': 'standard',
                'dimensions': (100.0, 100.0),
                'quantity': full_tiles_x * full_tiles_y,
                'positions': self._get_standard_positions(full_tiles_x, full_tiles_y)
            })
        
        # Right edge tiles (100×remainder_x)
        if remainder_x > 0 and full_tiles_y > 0:
            tiles.append({
                'type': 'edge_right',
                'dimensions': (remainder_x, 100.0),
                'quantity': full_tiles_y,
                'positions': self._get_right_edge_positions(full_tiles_x, full_tiles_y)
            })
        
        # Top edge tiles (100×remainder_y)
        if remainder_y > 0 and full_tiles_x > 0:
            tiles.append({
                'type': 'edge_top',
                'dimensions': (100.0, remainder_y),
                'quantity': full_tiles_x,
                'positions': self._get_top_edge_positions(full_tiles_x, full_tiles_y)
            })
        
        # Corner tile (remainder_x × remainder_y)
        if remainder_x > 0 and remainder_y > 0:
            tiles.append({
                'type': 'corner',
                'dimensions': (remainder_x, remainder_y),
                'quantity': 1,
                'positions': [(full_tiles_x, full_tiles_y)]
            })
        
        return tiles
    
    def get_unique_tiles(self):
        """
        Return list of unique tile geometries to generate
        """
        return [
            {
                'dimensions': tile['dimensions'],
                'quantity': tile['quantity'],
                'type': tile['type']
            }
            for tile in self.layout
        ]
    
    def generate_layout_diagram(self):
        """
        Generate ASCII art layout diagram
        """
        # Implementation returns visual grid representation
        pass

# Example usage:
# calculator = LayoutCalculator(total_width=250, total_length=180)
# Result: 
#   - 4 tiles of 100×100mm (2×1 grid)
#   - 2 tiles of 50×100mm (right edge)
#   - 2 tiles of 100×80mm (top edge)
#   - 1 tile of 50×80mm (corner)
```

#### Algorithm 3: Interior Grid Generation (Updated for Variable Dimensions)
```python
def create_cylinder_grid(params):
    """
    Generate variable grid of cylinders based on tile dimensions
    """
    # Calculate grid size based on tile dimensions
    grid_cols = int((params.length - 2*params.offset_x) / params.spacing) + 1
    grid_rows = int((params.width - 2*params.offset_y) / params.spacing) + 1
    
    cylinders = []
    
    for row in range(grid_rows):
        for col in range(grid_cols):
            x = params.offset_x + col * params.spacing
            y = params.offset_y + row * params.spacing
            
            # Only add cylinder if it fits within tile bounds
            if (x + params.cylinder_diameter/2 <= params.length - params.offset_x and
                y + params.cylinder_diameter/2 <= params.width - params.offset_y):
                
                cyl = cylinder(
                    radius=params.cylinder_diameter/2,
                    height=params.cylinder_height,
                    center=(x, y, 0)
                )
                cylinders.append(cyl)
    
    return cylinders
```

#### Algorithm 4: Tab/Slot Position Calculator (Updated for Variable Dimensions)
```python
def calculate_edge_feature_positions(tile_width, tile_length):
    """
    Calculate tab and slot positions based on tile dimensions
    Only place features at 10mm intervals that fit within the tile
    """
    FEATURE_SPACING = 10.0
    FEATURE_START = 10.0
    
    # Calculate positions for width (left/right edges)
    width_positions = []
    pos = FEATURE_START
    while pos <= tile_width - FEATURE_START:
        width_positions.append(pos)
        pos += FEATURE_SPACING
    
    # Calculate positions for length (top/bottom edges)
    length_positions = []
    pos = FEATURE_START
    while pos <= tile_length - FEATURE_START:
        length_positions.append(pos)
        pos += FEATURE_SPACING
    
    return {
        'width_positions': width_positions,   # For left/right edges
        'length_positions': length_positions  # For top/bottom edges
    }
```

#### Algorithm 5: Assembly Strategy
```python
def build_complete_model(params):
    """
    Main assembly function using two-layer approach
    """
    # Step 1: Create base layer (Z=0 to Z=3.5)
    perimeter_frame = extrude(
        create_perimeter_sketch(params),
        height=params.perimeter_wall_height
    )
    
    cylinders = create_cylinder_grid(params)
    
    # Step 2: Create top layer (Z=3.5 to Z=6)
    top_layer_sketch = rectangle(params.length, params.width)
    top_layer = extrude(
        top_layer_sketch,
        height=params.top_layer_thickness
    ).translate(z=params.perimeter_wall_height)
    
    # Step 3: Unite all components
    unified = union([perimeter_frame] + cylinders + [top_layer])
    
    # Step 4: Create holes through entire model
    for row in range(params.grid_rows):
        for col in range(params.grid_cols):
            x = params.offset_x + col * params.spacing
            y = params.offset_y + row * params.spacing
            
            hole = cylinder(
                radius=params.hole_diameter/2,
                height=params.plate_thickness,
                center=(x, y, 0)
            )
            unified = unified - hole
    
    return unified
```

### 4.2 Parameter Validation Rules

```python
class ParameterValidator:
    @staticmethod
    def validate(params):
        """Comprehensive parameter validation"""
        
        # Dimension checks
        assert params.plate_length > 0, "Length must be positive"
        assert params.plate_width > 0, "Width must be positive"
        assert params.plate_thickness > 0, "Thickness must be positive"
        
        # Relationship checks
        assert params.cylinder_diameter > params.hole_diameter, \
            "Cylinder must be larger than hole"
        
        assert params.slot_diameter > params.tab_diameter, \
            "Slots must be larger than tabs"
        
        assert params.grid_spacing > params.cylinder_diameter, \
            "Grid spacing must exceed cylinder diameter"
        
        # Layer height check
        assert abs(
            params.perimeter_wall_height + params.top_layer_thickness - 
            params.plate_thickness
        ) < 0.001, "Layer heights must sum to total thickness"
        
        # Boundary checks
        max_x = params.offset_x + (params.grid_cols - 1) * params.spacing
        max_y = params.offset_y + (params.grid_rows - 1) * params.spacing
        
        assert max_x <= params.plate_length - params.offset_x, \
            "Grid exceeds plate boundaries"
        
        assert max_y <= params.plate_width - params.offset_y, \
            "Grid exceeds plate boundaries"
        
        return True
```

---

## 5. Testing Strategy

### 5.1 Unit Tests
- Parameter loading and parsing
- Geometric coordinate calculations
- Validation rule enforcement
- Export format generation
- **Layout calculator logic (NEW)**
- **Edge feature position calculator (NEW)**
- **Grid size calculation for custom dimensions (NEW)**

### 5.2 Integration Tests
- Complete model generation (standard 100×100mm)
- **Custom dimension tile generation (e.g., 45×100mm) (NEW)**
- **Multi-tile assembly generation (NEW)**
- Multi-format export
- Preset configurations
- Batch processing

### 5.3 Validation Tests
- Compare generated STEP with reference
- Measure critical dimensions
- Verify feature counts
- Check for geometric errors
- **Verify tab/slot alignment across tiles (NEW)**
- **Confirm custom tiles fit within total dimensions (NEW)**

### 5.4 Layout Tests (NEW)
- **250×180mm → 4+2+2+1 tiles verified**
- **315×215mm → proper breakdown**
- **100×100mm (exact) → 1 tile only**
- **450×450mm → 4×4 grid of standard tiles**
- **Edge cases: 105×100mm, 50×75mm**

### 5.5 Performance Tests
- Generation time benchmarks
- Memory usage profiling
- Large assemblies (e.g., 1000×500mm = 50 tiles)
- Batch generation efficiency

---

## 6. Usage Examples

### 6.1 Basic Usage - Total Dimensions (NEW)
```bash
# Generate tiles for 250mm × 180mm drawer
python generate_model.py --total-width 250 --total-length 180

# Output to specific directory
python generate_model.py --total-width 250 --total-length 180 --output-dir ./my_drawer

# Different format
python generate_model.py --total-width 315 --total-length 215 --format stl

# Use preset for common drawer size
python generate_model.py --preset drawer_small_250x180
```

### 6.2 Single Tile Generation (Original Behavior)
```bash
# Generate standard 100×100mm tile
python generate_model.py --single-tile

# Generate custom single tile
python generate_model.py --single-tile --tile-width 100 --tile-length 45

# Use custom parameters
python generate_model.py --single-tile --config custom_params.json

# Specify output format
python generate_model.py --single-tile --format step --output tulorg.step
```

### 6.3 Python API - Assembly Generation (NEW)
```python
from tulorg_generator import ModelBuilder, Parameters

# Load parameters
params = Parameters.from_json('config/default_parameters.json')

# Build model
builder = ModelBuilder(params)
model = builder.build()

# Export
builder.export_step('output/tulorg.step')
builder.export_stl('output/tulorg.stl')
```

### 6.3 Custom Variants
```python
# Create a larger 200x200mm grid
params = Parameters.from_json('config/default_parameters.json')
params.plate_length = 200
params.plate_width = 200
params.grid_rows = 20
params.grid_cols = 20

builder = ModelBuilder(params)
model = builder.build()
```

---

## 7. Assembly README Generation (NEW)

### 7.1 Auto-Generated README Structure

The script automatically generates a comprehensive `ASSEMBLY_README.md` file for each layout:

```markdown
# Tulorg Assembly Guide
**Generated:** 2026-01-13 07:08:00
**Total Dimensions:** 250mm × 180mm
**Total Tiles Required:** 9 tiles (4 unique geometries)

## Files in This Package

| Filename | Dimensions | Quantity | Type | Notes |
|----------|-----------|----------|------|-------|
| tile_100x100_qty4.stl | 100×100mm | 4 | Standard | Main grid tiles |
| tile_100x50_qty2.stl | 100×50mm | 2 | Edge (Right) | Fill right edge |
| tile_80x100_qty2.stl | 80×100mm | 2 | Edge (Top) | Fill top edge |
| tile_80x50_qty1.stl | 80×50mm | 1 | Corner | Top-right corner |

**Manufacturing Summary:**
- Print/manufacture 9 total tiles
- 4 unique STL files provided
- All tiles are 6mm thick

## Layout Diagram

```
    0mm   100mm  200mm  250mm
    ┌─────┬─────┬─────┐
0mm │  1  │  2  │  5  │
    │100×1│100×1│50×10│
    │00   │00   │0    │
    ├─────┼─────┼─────┤
100m│  3  │  4  │  6  │
m   │100×1│100×1│50×10│
    │00   │00   │0    │
    ├─────┴─────┴─────┤
180m│   7    │   8   │9│
m   │  100×80  │ 50×80│
    └─────────┴──────┴┘
```

## Assembly Instructions

### Step 1: Prepare Tiles
- Manufacture all 9 tiles according to filenames
- Verify dimensions with calipers
- Check that tabs and slots are clean and free of defects

### Step 2: Assembly Order
1. **Start with bottom-left:** Tile #1 (100×100mm)
2. **Build bottom row:** Add tiles #2, #5 moving right
3. **Build second row:** Add tiles #3, #4, #6
4. **Complete top row:** Add tiles #7, #8, #9

### Step 3: Interlocking System
- **Tabs (male):** Located on TOP and RIGHT edges
- **Slots (female):** Located on BOTTOM and LEFT edges
- **Connection:** Each tile's right tabs fit into next tile's left slots
- **Connection:** Each tile's top tabs fit into tile above's bottom slots

### Step 4: Alignment Tips
- Start from bottom-left corner (0,0 position)
- Work left-to-right, bottom-to-top
- Press firmly to seat tabs in slots
- Verify alignment by checking grid holes align across tiles

## Grid Pattern
- Each 100×100mm tile: 10×10 holes (100 mounting points)
- Each edge tile: Partial grid maintaining 10mm spacing
- Total mounting points: ~162 (actual count depends on edge dimensions)
- Hole diameter: 4mm (suitable for M3 or 1/8" pegs)

## Tile Details

### Standard Tile (100×100mm) - Quantity: 4
- Grid: 10×10 holes
- Tabs: 9 on top edge, 9 on right edge (Ø3.8mm)
- Slots: 9 on bottom edge, 9 on left edge (Ø4.0mm)
- Positions in assembly: Tiles #1, #2, #3, #4

### Edge Tile Right (100×50mm) - Quantity: 2
- Grid: 10×5 holes (approximately)
- Tabs: 9 on top edge, 4 on right edge
- Slots: 9 on bottom edge, 0 on left edge (flush connection)
- Positions in assembly: Tiles #5, #6

### Edge Tile Top (80×100mm) - Quantity: 2
- Grid: 8×10 holes (approximately)
- Tabs: 7 on top edge, 0 on right edge (flush termination)
- Slots: 0 on bottom edge (flush), 9 on left edge
- Positions in assembly: Tiles #7, #8

### Corner Tile (80×50mm) - Quantity: 1
- Grid: 8×5 holes (approximately)
- Tabs: 7 on top edge, 4 on right edge
- Slots: 0 on bottom, 0 on left (flush termination)
- Position in assembly: Tile #9

## Troubleshooting

**Tabs don't fit in slots:**
- Check for printing artifacts or supports
- Light sanding may be needed (0.2mm clearance designed in)

**Tiles don't align:**
- Verify manufacturing dimensions
- Check assembly order (bottom-to-top, left-to-right)

**Gaps between tiles:**
- Normal - slight gaps expected due to manufacturing tolerances
- Should not affect functionality

## Customization
To generate a different size layout:
```bash
python generate_model.py --total-width [WIDTH] --total-length [LENGTH]
```

---
*Auto-generated by Tulorg Generator v1.0*
```

### 7.2 Layout Diagram Generator

```python
class AssemblyGuideGenerator:
    """
    Generate assembly documentation
    """
    
    def generate_layout_diagram(self, layout):
        """
        Create ASCII art layout with tile numbers and dimensions
        """
        # Build visual grid representation
        diagram = []
        
        # Add dimension markers
        # Add tile boxes with numbers and dimensions
        # Format for readability
        
        return "\n".join(diagram)
    
    def generate_readme(self, layout, output_dir):
        """
        Create comprehensive ASSEMBLY_README.md
        """
        content = self._build_readme_content(layout)
        
        with open(f"{output_dir}/ASSEMBLY_README.md", "w") as f:
            f.write(content)
    
    def _build_readme_content(self, layout):
        """
        Build complete README content
        """
        sections = []
        sections.append(self._header_section(layout))
        sections.append(self._files_table(layout))
        sections.append(self._layout_diagram(layout))
        sections.append(self._assembly_instructions(layout))
        sections.append(self._tile_details(layout))
        sections.append(self._troubleshooting_section())
        
        return "\n\n".join(sections)
```

---

## 8. Deliverables Checklist

### Documentation
- [ ] README.md with quick start guide
- [ ] API documentation
- [ ] Parameter reference guide
- [ ] Example gallery with images
- [ ] Troubleshooting guide
- [ ] **Assembly guide auto-generation (NEW)**
- [ ] **Layout diagram generator (NEW)**

### Code
- [ ] Core geometry builder
- [ ] **Variable dimension tile builder (NEW)**
- [ ] **Layout calculator (NEW)**
- [ ] **Assembly guide generator (NEW)**
- [ ] Parameter management system
- [ ] Validation framework
- [ ] Export modules (STEP, STL, 3MF, OBJ)
- [ ] CLI interface with total dimension arguments
- [ ] **Batch tile generation (NEW)**
- [ ] **Filename quantity encoding (NEW)**
- [ ] Unit tests (>90% coverage)
- [ ] Integration tests

### Data Files
- [x] parameters.json
- [x] validation_rules.json
- [x] geometry_formulas.json
- [ ] Preset configurations for common drawer sizes
  - [ ] drawer_small_250x180.json
  - [ ] drawer_medium_450x300.json
  - [ ] drawer_large_600x400.json

### Output Examples
- [ ] Reference STEP file (100×100mm)
- [ ] **Complete 250×180mm assembly (NEW)**
  - [ ] 4 unique STL files with qty in filename
  - [ ] Assembly README.md
  - [ ] Layout diagram
- [ ] **Complete 315×215mm assembly (NEW)**
- [ ] Single custom tile (50×75mm)

---

## 8. Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| CAD library limitations | High | Medium | Test CadQuery early, have OpenSCAD fallback |
| STEP export accuracy | High | Low | Validate against reference, use established libraries |
| Performance with large grids | Medium | Medium | Optimize boolean operations, add progress reporting |
| Cross-platform compatibility | Medium | Low | Test on Windows/Linux/Mac |

### Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | Medium | Medium | Clear phase definitions, MVP first |
| Parameter complexity | Low | Low | Comprehensive validation, good documentation |
| User adoption | Low | Low | Excellent documentation, examples, presets |

---

## 9. Success Criteria

### Must Have (Updated)
- ✅ **Accept total width/length as input parameters (NEW)**
- ✅ **Calculate optimal tile layout automatically (NEW)**
- ✅ **Generate unique STL files with quantity in filename (NEW)**
- ✅ **Auto-generate assembly README with instructions (NEW)**
- ✅ Generate geometrically accurate tiles matching reference
- ✅ Export to STL format (primary)
- ✅ Parameter validation with clear error messages
- ✅ Command-line interface
- ✅ Basic documentation

### Should Have
- Export to STEP, 3MF formats (in addition to STL)
- Preset configurations for common drawer sizes
- **Layout diagram visualization (NEW)**
- **Support for edge tiles <100mm (NEW)**
- Comprehensive test suite
- Example assemblies

### Nice to Have
- GUI interface
- Real-time preview
- Web-based configurator
- **3D assembly visualization (NEW)**
- Integration with slicer software
- Export assembly instructions as PDF

---

## 10. Timeline (Updated for Assembly Features)

### Accelerated Schedule (6 days)
- **Day 1:** Foundation + layout calculator
- **Day 2:** Core geometry for variable dimensions
- **Day 3:** Batch generation + STL export
- **Day 4:** Assembly guide generator
- **Day 5:** CLI + testing
- **Day 6:** Documentation + examples

### Standard Schedule (2 weeks)
- **Days 1-2:** Foundation + layout calculator + validation
- **Days 3-5:** Core geometry + variable dimension support
- **Days 6-7:** Batch generation + assembly guide
- **Days 8-9:** CLI + multi-format export
- **Days 10-12:** Testing + optimization
- **Days 13-14:** Documentation + example assemblies

### Extended Schedule (3 weeks)
- **Week 1:** Core implementation + layout system
- **Week 2:** Assembly generation + batch processing
- **Week 3:** Testing + comprehensive documentation + GUI prototype

---

## 11. Next Steps

### Immediate Actions
1. **Choose platform:** Confirm CadQuery as primary implementation
2. **Set up environment:** Install dependencies, create project structure
3. **Validate approach:** Create minimal proof-of-concept (single tile generation)
4. **Prototype layout calculator:** Test algorithm with various total dimensions
5. **Begin Phase 0:** Implement layout calculator and validation

### Decision Points
- ✅ **Platform selection:** CadQuery recommended based on requirements
- ✅ **Primary use case:** Assembly generation with total dimensions as input
- ⏳ **Schedule choice:** Standard 2-week schedule recommended for full feature set
- ⏳ **Feature priority:** Prioritize STL export and assembly guide generation
- ⏳ **Testing rigor:** Determine acceptable test coverage level (target 85%+)

### Example Test Cases to Implement
1. **250×180mm drawer:** 4+2+2+1 tiles
2. **315×215mm drawer:** Verify proper edge tile dimensions
3. **100×100mm (exact):** Single tile only, verify no edge pieces
4. **450×450mm:** 4×4 grid, all standard tiles
5. **125×75mm:** Small assembly with all edge types

---

## 12. Example Workflow (End-to-End)

### User Perspective
```bash
# User has a toolbox drawer: 250mm wide × 180mm deep
$ python generate_model.py --total-width 250 --total-length 180

Calculating layout for 250mm × 180mm...
✓ Layout calculated: 4 standard tiles + 5 edge pieces

Generating tiles:
  [1/4] tile_100x100_qty4.stl ... ✓ (2.3 MB)
  [2/4] tile_100x50_qty2.stl ... ✓ (1.2 MB)
  [3/4] tile_80x100_qty2.stl ... ✓ (1.1 MB)
  [4/4] tile_80x50_qty1.stl ... ✓ (0.6 MB)

Generating assembly guide...
  ✓ layout_diagram.txt
  ✓ ASSEMBLY_README.md

Output saved to: ./output/2026-01-13_070800_250x180mm/

Summary:
  Total tiles to manufacture: 9
  Unique geometries: 4
  Total STL file size: 5.2 MB
  Assembly guide: ASSEMBLY_README.md

Next steps:
  1. Review layout in ASSEMBLY_README.md
  2. Send STL files to 3D printer/CNC
  3. Manufacture quantities as indicated in filenames
  4. Follow assembly instructions in README
```

### Generated File Structure
```
output/2026-01-13_070800_250x180mm/
├── tile_100x100_qty4.stl          # 2.3 MB - Standard full tiles
├── tile_100x50_qty2.stl           # 1.2 MB - Right edge
├── tile_80x100_qty2.stl           # 1.1 MB - Top edge
├── tile_80x50_qty1.stl            # 0.6 MB - Corner
├── layout_diagram.txt             # Visual ASCII layout
└── ASSEMBLY_README.md             # Complete instructions
```

---

## 13. Appendix

### A. Dependencies (CadQuery Approach)
```
cadquery>=2.4.0
numpy>=1.24.0
ezdxf>=1.1.0  # For DXF export (optional)
pytest>=7.4.0
black>=23.0.0  # Code formatting
click>=8.0.0   # CLI framework (NEW)
jinja2>=3.0.0  # README template generation (NEW)
```

### B. Coordinate Reference System
- **Origin:** (0, 0, 0) at bottom-left-front corner
- **X-axis:** Left to right (0 to 100mm)
- **Y-axis:** Bottom to top (0 to 100mm)
- **Z-axis:** Bottom to top (0 to 6mm)

### C. File Format Specifications
- **STEP:** AP214 (AUTOMOTIVE_DESIGN)
- **STL:** Binary, ASCII optional
- **3MF:** With color/material metadata
- **OBJ:** With normals

### D. Performance Targets (Updated)
- **Single tile generation:** <10 seconds for standard 100×100mm model
- **Assembly generation:** <60 seconds for 9-tile assembly (250×180mm)
- **Large assembly:** <5 minutes for 50-tile assembly (1000×500mm)
- Memory usage: <500MB for standard assembly
- STL file size per tile: ~1-3MB (depends on resolution)
- **Assembly package:** ~5-15MB total for typical drawer

### E. Filename Convention (NEW)
```
tile_{width}x{length}_qty{count}.stl

Examples:
- tile_100x100_qty4.stl    → 100mm×100mm, make 4 copies
- tile_100x50_qty2.stl     → 100mm×50mm, make 2 copies
- tile_80x100_qty2.stl     → 80mm×100mm, make 2 copies
- tile_80x50_qty1.stl      → 80mm×50mm, make 1 copy
- tile_45x65_qty1.stl      → 45mm×65mm, make 1 copy

Format: {dimension1}x{dimension2} always in mm, rounded to integers
        qty{N} indicates number of physical tiles to manufacture
```

### F. Layout Calculation Examples (NEW)

| Total Dimensions | Standard Tiles | Edge Tiles | Corner | Total Physical | Unique Files |
|-----------------|---------------|------------|--------|---------------|--------------|
| 100×100mm | 1 (100×100) | - | - | 1 | 1 |
| 250×180mm | 4 (100×100) | 2+2 edges | 1 | 9 | 4 |
| 315×215mm | 6 (100×100) | 3+2 edges | 1 | 12 | 4 |
| 450×450mm | 16 (100×100) | - | - | 16 | 1 |
| 225×125mm | 4 (100×100) | 2+2 edges | 1 | 9 | 4 |
| 105×75mm | - | 1+0 edges | 1 | 2 | 2 |

---

## Conclusion

This implementation plan provides a comprehensive roadmap for creating a **modular assembly generation system** for Tulorg. The script accepts total drawer dimensions and intelligently generates the optimal tile layout, produces unique STL files with quantity encoding, and auto-generates assembly instructions.

**Key Innovation:** Rather than generating individual tiles, the system generates complete **assembly packages** optimized for manufacturing - minimizing the number of unique parts while maximizing modularity.

The analysis confirms all reference documents are consistent and accurate. The recommended CadQuery-based approach balances capability, accessibility, and maintainability while supporting the assembly generation workflow.

**Recommended Start:** 
1. Begin with layout calculator proof-of-concept
2. Validate tile dimension calculation algorithm
3. Implement single variable-dimension tile generator
4. Proceed with batch generation and assembly guide features
