# Naming Conventions for Generated Scripts

Standardized naming makes it easier to use and maintain generated code across models.

---

## Script Names

### Pattern: `generate_{model_name}.py`

Use the model name in lowercase with underscores, no version numbers.

**Examples:**
```
✓ generate_shelfbracket.py      (Model: ShelfBracket)
✓ generate_toolholder.py         (Model: ToolHolder)
✓ generate_pegboardtile.py       (Model: PegboardTile)
✓ generate_handlegrip.py         (Model: HandleGrip)
```

**Wrong patterns:**
```
✗ generate_shelfbracketv1.py    (Remove version number)
✗ generate_shelf_bracket.py      (Use underscore once)
✗ ShelfBracket.py               (Keep lowercase)
✗ shelf_bracket_generator.py    (Keep it short)
```

---

## Function Names

### Feature Implementation: `add_{FeatureName}`

Each feature from model.json gets a function. Use the feature name in CamelCase.

**From model.json feature timeline:**
```
Feature: "Base Extrude"
Function: def add_base_extrude(model, ...)

Feature: "Mounting Boss"
Function: def add_mounting_boss(model, ...)

Feature: "Mounting Holes"
Function: def add_mounting_holes(model, ...)

Feature: "Reinforcement Ribs"
Function: def add_reinforcement_ribs(model, ...)

Feature: "Corner Fillet External"
Function: def add_corner_fillet_external(model, ...)
```

### Sketch Creation: `create_{SketchName}_sketch` or `get_{SketchName}_positions`

Sketches are created (not added to model), so use `create_`.
For computed positions/arrays, use `get_`.

**Examples:**
```python
def create_base_profile_sketch(width, depth):
    """Create rectangular profile sketch"""
    
def create_mounting_holes_sketch(width, hole_diameter):
    """Create 4 corner hole positions"""
    
def get_mounting_hole_positions(width, depth):
    """Calculate hole positions"""
    
def get_rib_positions(width, depth):
    """Calculate rib pattern positions"""
```

### Validation: `validate_parameters` and `validate_model`

```python
def validate_parameters(BaseWidth, BaseThickness, ...):
    """Validate input parameters before generation"""
    
def validate_model(model, BaseWidth, ...):
    """Validate output model meets specs"""
```

### Main Functions

```python
def generate_shelfbracket(BaseWidth=200, ...):
    """Main generation function (user-facing)"""
    
def main():
    """CLI entry point"""
```

---

## Parameter Names (Python)

Use exact names from parameters.json in your Python code.

**Convention: PascalCase (CapitalizedWords)**

Why? Parameters are configuration data, not regular variables.

**Examples:**
```python
# From parameters.json
BaseWidth        → Use as: BaseWidth (not base_width, WIDTH, w)
CornerRadius     → Use as: CornerRadius (not corner_radius, radius)
MountingHoleDiameter → Use as: MountingHoleDiameter
MinWallThickness → Use as: MinWallThickness
RibHeight        → Use as: RibHeight
```

**In function signatures:**
```python
def generate_model(
    BaseWidth=200,              # Not width=200
    BaseThickness=10,           # Not thickness=10
    CornerRadius=1.5,           # Not radius=1.5
    MountingHoleDiameter=3.2,   # Not hole_diameter=3.2
    MinWallThickness=2,         # Not min_wall=2
    RibHeight=5,                # Not rib_h=5
    **kwargs
):
```

**In code:**
```python
# GOOD: Parameter names match everywhere
if not (100 <= BaseWidth <= 300):
    raise ValueError(f"BaseWidth {BaseWidth}mm out of range")

model = create_base_profile(BaseWidth, BaseThickness, CornerRadius)
```

```python
# BAD: Converting names makes it confusing
base_width = BaseWidth  # Don't rename - causes bugs
if not (100 <= base_width <= 300):
    raise ValueError(...)  # Now reference is wrong
```

### Fixed Parameters

Use UPPERCASE_WITH_UNDERSCORES for constants that never change.

**Examples:**
```python
# Design rules (from constraints.json)
BASE_DEPTH = 150          # Must match aluminum post standard
MOUNTING_HOLE_INSET = 10  # Design rule - holes always 10mm from corners
RIB_EXTENSION_RATIO = 0.8 # Ribs extend to 80% of width
INTERNAL_FILLET_RADIUS = 1.0  # Minimum 1mm for FDM
TAPER_FACTOR = 0.85       # Wall taper scaling
```

### Derived Parameters

Use PascalCase (like user parameters) with descriptive names.

**Examples:**
```python
# Calculated from user parameters
BossHeight = BaseWidth * 0.15  # Derived: scales with width
RibSpacing = BaseWidth * 0.25  # Derived: rib array spacing
```

---

## CLI Argument Names (kebab-case)

Command-line arguments use lowercase with hyphens.

**Convention:** Convert PascalCase parameter to kebab-case

```python
# From parameters.json:     Python name:          CLI argument:
BaseWidth                → BaseWidth        → --width
BaseThickness            → BaseThickness    → --thickness
CornerRadius             → CornerRadius     → --corner-radius
MountingHoleDiameter     → MountingHoleDiameter → --hole-diameter
MinWallThickness         → MinWallThickness → --wall-thickness
RibHeight                → RibHeight        → --rib-height
```

**In argparse:**
```python
parser.add_argument("--width", type=float, default=200,
                   help="Bracket width (100-300mm)")

parser.add_argument("--corner-radius", type=float, default=1.5,
                   help="Corner radius (1.5-3mm minimum)")

parser.add_argument("--wall-thickness", type=float, default=2,
                   help="Wall thickness (1.5-3mm, CRITICAL below 1.5mm)")
```

**Usage:**
```bash
python generate_shelfbracket.py --width 200 --corner-radius 2 --wall-thickness 2.5
```

---

## Output File Names

Pattern: `{ModelName}_{Variant}.{ext}`

**Variant** describes what's special about this output.

**Examples:**
```
shelfbracket_small.step          # width=100mm variant
shelfbracket_medium.step         # width=200mm (default)
shelfbracket_large.step          # width=300mm variant
shelfbracket_custom.step         # user-specified parameters
shelfbracket_2mm_walls.step      # wall-thickness=2mm variant
shelfbracket_minimal.step        # all minimums (testing)
shelfbracket_maximal.step        # all maximums (testing)
```

**Without variant:** Defaults to model name
```
shelfbracket.step               # Generates with default parameters
```

---

## Local Variable Names (regular variables)

Use lowercase with underscores for temporary/local variables.

**Examples:**
```python
# Local variables (lowercase)
profile_points = [(10, 10), (20, 10), ...]
hole_positions = get_mounting_hole_positions(width, depth)
rib_spacing = BaseWidth * 0.25  # Even though derived from parameter
model_volume = model.val().volume()
bounding_box = model.val().boundingBox()
```

**Key distinction:**
- `BaseWidth` - User parameter (PascalCase)
- `base_width_mm` - Local variable (lowercase_underscore)
- `BASE_DEPTH` - Constant/design rule (UPPERCASE_UNDERSCORE)

**Example function:**
```python
def add_reinforcement_ribs(model, BaseWidth, BaseDepth, RibHeight, MinWallThickness):
    """Add ribs (parameters are PascalCase)"""
    
    # Derived parameter
    rib_spacing = BaseWidth * 0.25
    
    # Calculate positions
    rib_positions = get_rib_positions(BaseWidth, BaseDepth)
    
    # Apply each rib
    for x_pos in rib_positions:
        model = (model
                 .faces("<Z")
                 .workplane()
                 .center(x_pos, 0)
                 .rect(3, BaseDepth * 0.8)
                 .pocket(RibHeight))
    
    return model
```

---

## Comments & Documentation

### Docstrings: Use triple quotes, describe parameters

```python
def generate_shelfbracket(
    BaseWidth=200,
    BaseThickness=10,
    CornerRadius=1.5,
    MountingHoleDiameter=3.2,
    MinWallThickness=2,
    RibHeight=5
):
    """
    Generate ShelfBracket model with given parameters.
    
    Args:
        BaseWidth (int): Bracket width in mm (100-300, step 10)
        BaseThickness (int): Bracket height in mm (8-12)
        CornerRadius (float): External corner radius in mm (1.5-3)
        MountingHoleDiameter (float): Bolt hole diameter in mm (3.0-3.5)
        MinWallThickness (float): Structural wall thickness in mm (1.5-3)
        RibHeight (int): Rib depth in mm (3-8)
    
    Returns:
        CadQuery.Workplane: 3D model object
    
    Raises:
        ValueError: If parameters violate constraints
    """
```

### Feature Comments: Reference model.json

```python
def add_base_extrude(model, thickness):
    """
    Feature 1: Base Extrude
    
    Creates main body by extruding the base profile.
    This is the foundational feature - all others build on it.
    """
    return model.extrude(thickness)


def add_mounting_holes(model, width, depth, hole_diameter):
    """
    Feature 3: Mounting Holes
    
    Creates 4 corner mounting holes (through-all).
    Positions: 10mm inset from all corners (design rule from model.json)
    
    Note: Hole positions are fixed by design, not parametric.
    """
```

### Inline Comments: Explain non-obvious CadQuery operations

```python
def add_reinforcement_ribs(model, width, depth, rib_height):
    """Add ribs spaced at width/4"""
    
    # Calculate dynamic rib spacing (ribs scale with width)
    rib_spacing = width * 0.25  # BaseWidth * 0.25 from parameters.json
    
    # Get rib positions
    rib_positions = get_rib_positions(width, depth)
    
    # Add each rib as pocket (negative feature on bottom face)
    for x_pos in rib_positions:
        model = (model
                 .faces("<Z")           # Select bottom face
                 .workplane()           # Create workplane on that face
                 .center(x_pos, 0)      # Center at this X position
                 .rect(3, depth * 0.8)  # Draw 3mm × 80% of depth rectangle
                 .pocket(rib_height))   # Cut pocket with specified depth
    
    return model
```

---

## Summary Table

| Type | Convention | Example | Notes |
|------|-----------|---------|-------|
| Script | lowercase_underscores | `generate_shelfbracket.py` | Model name, no version |
| Function (feature) | add_{FeatureName} | `add_base_extrude()` | Each feature gets one |
| Function (sketch) | create_{Sketch} | `create_base_profile_sketch()` | For sketch creation |
| Function (calc) | get_{Thing} | `get_mounting_hole_positions()` | For calculated data |
| Parameter (Python) | PascalCase | `BaseWidth` | Match parameters.json |
| Parameter (CLI) | kebab-case | `--width` | Convert from Python |
| Constant | UPPERCASE_UNDERSCORE | `BASE_DEPTH` | Design rules, fixed values |
| Local var | lowercase_underscore | `hole_positions` | Temporary/computed values |
| Output file | {Name}_{Variant} | `shelfbracket_large.step` | Variant describes config |

---

## Consistency Check

Before finalizing your generated script, verify:

- [ ] All parameters use PascalCase (BaseWidth not base_width)
- [ ] All CLI args use kebab-case (--corner-radius not --cornerRadius)
- [ ] All feature functions start with `add_` or `create_`
- [ ] All constants are UPPERCASE_UNDERSCORE
- [ ] Script named `generate_{model_name}.py` in lowercase
- [ ] Docstrings reference parameters.json parameter names
- [ ] Feature functions referenced in docstring match model.json timeline
- [ ] No hardcoded values that should be parameters
