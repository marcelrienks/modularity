# Code Naming Conventions

Standardized naming for consistency and maintainability across generated scripts.

## Script Names

**Pattern:** `generate_{model_name}.py`

Use model name in lowercase, no version numbers.

```
✓ generate_shelfbracket.py     (Model: ShelfBracket)
✓ generate_toolholder.py        (Model: ToolHolder)
✓ generate_pegboardtile.py      (Model: PegboardTile)

✗ generate_shelfbracketv1.py   (Remove version)
✗ ShelfBracket.py              (Keep lowercase)
```

## Function Names

### Feature Implementation: `add_{FeatureName}`

Each feature from model.json timeline gets a function.

```python
def add_base_extrude(model, thickness):
    """Feature 1: Base Extrude"""

def add_mounting_holes(model, width, hole_diameter):
    """Feature 3: Mounting Holes"""

def add_reinforcement_ribs(model, width, height):
    """Feature 5: Reinforcement Ribs"""
```

### Sketch Creation: `create_{SketchName}_sketch` or `get_{Thing}_positions`

```python
def create_base_profile_sketch(width, depth):
    """Create rectangular profile"""

def get_mounting_hole_positions(width, depth):
    """Calculate hole positions"""

def get_rib_positions(width, depth):
    """Calculate rib pattern positions"""
```

### Validation Functions

```python
def validate_parameters(BaseWidth, BaseThickness, ...):
    """Validate parameters before generation"""

def validate_model(model, BaseWidth, ...):
    """Validate generated model meets specs"""
```

## Parameter Names (Python)

**Convention:** PascalCase (CapitalizedWords)

Use exact names from `parameters.json`. Never rename during code.

```python
def generate_model(
    BaseWidth=200,           # Not width, base_width, WIDTH
    BaseThickness=10,        # Not thickness
    CornerRadius=1.5,        # Not corner_radius
    MountingHoleDiameter=3.2,
    MinWallThickness=2,
    RibHeight=5
):
```

## CLI Argument Names

**Convention:** kebab-case (lowercase-with-hyphens)

Convert Python parameter names:

```
BaseWidth              →  --width
BaseThickness          →  --thickness
CornerRadius           →  --corner-radius
MountingHoleDiameter   →  --hole-diameter
MinWallThickness       →  --wall-thickness
RibHeight              →  --rib-height
```

**In argparse:**
```python
parser.add_argument("--width", type=float, default=200,
                    help="Bracket width (100-300mm)")

parser.add_argument("--corner-radius", type=float, default=1.5,
                    help="Corner radius (1.5-3mm minimum)")
```

## Constants

**Convention:** UPPERCASE_WITH_UNDERSCORES

Fixed values that never change (design rules).

```python
BASE_DEPTH = 150              # Must match aluminum post standard
MOUNTING_HOLE_INSET = 10      # Holes always 10mm from corners
RIB_EXTENSION_RATIO = 0.8     # Ribs extend to 80% of width
INTERNAL_FILLET_RADIUS = 1.0  # Minimum 1mm for FDM
```

## Derived Parameters

**Convention:** PascalCase (like user parameters)

Calculated from user parameters.

```python
BossHeight = BaseWidth * 0.15   # Scales with width
RibSpacing = BaseWidth * 0.25   # Rib array spacing
```

## Local Variables

**Convention:** lowercase_with_underscores

Temporary/computed values.

```python
profile_points = [(10, 10), (20, 10), ...]
hole_positions = get_mounting_hole_positions(width, depth)
model_volume = model.val().volume()
bounding_box = model.val().boundingBox()
```

## Output Files

**Pattern:** `{ModelName}_{Variant}.{ext}`

```
shelfbracket_small.step       # width=100mm variant
shelfbracket_medium.step      # width=200mm (default)
shelfbracket_large.step       # width=300mm variant
shelfbracket_custom.step      # user-specified parameters
```

## Documentation

### Docstrings

```python
def generate_shelfbracket(
    BaseWidth=200,
    BaseThickness=10,
    CornerRadius=1.5
):
    """
    Generate ShelfBracket model with given parameters.
    
    Args:
        BaseWidth (float): Bracket width in mm (100-300, step 10)
        BaseThickness (float): Bracket height in mm (8-12)
        CornerRadius (float): External corner radius in mm (1.5-3)
    
    Returns:
        CadQuery.Workplane: 3D model object
    
    Raises:
        ValueError: If parameters violate constraints
    """
```

### Feature Comments

```python
def add_base_extrude(model, thickness):
    """
    Feature 1: Base Extrude
    
    Creates main body by extruding the base profile.
    This is foundational - all other features depend on it.
    """
    return model.extrude(thickness)
```

### Inline Comments

Explain non-obvious CadQuery operations:

```python
# Select bottom face and create workplane on it
model = (model
         .faces("<Z")              # Select bottom face
         .workplane()              # Create workplane
         .center(x_pos, 0)         # Center at this X position
         .rect(3, depth * 0.8)     # Draw rectangle
         .pocket(rib_height))      # Cut pocket
```

## Quick Reference

| Type | Convention | Example |
|------|-----------|---------|
| Script | lowercase_underscores | `generate_shelfbracket.py` |
| Feature function | `add_{FeatureName}` | `add_base_extrude()` |
| Sketch function | `create_{Sketch}` | `create_base_profile_sketch()` |
| Python parameter | PascalCase | `BaseWidth` |
| CLI argument | kebab-case | `--width` |
| Constant | UPPERCASE_UNDERSCORE | `BASE_DEPTH` |
| Local variable | lowercase_underscore | `hole_positions` |
| Output file | `{Name}_{Variant}` | `shelfbracket_large.step` |

## Consistency Checklist

Before finalizing generated code:

- [ ] Parameters use PascalCase (BaseWidth not base_width)
- [ ] CLI args use kebab-case (--corner-radius not --cornerRadius)
- [ ] Feature functions start with `add_` or `create_`
- [ ] Constants are UPPERCASE_UNDERSCORE
- [ ] Script named `generate_{model_name}.py` in lowercase
- [ ] All docstrings reference parameter names correctly
- [ ] No hardcoded values (all should be parameters or constants)
