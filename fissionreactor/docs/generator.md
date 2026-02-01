# Code Generation

Complete guide to generating parameterized Python code from your context package using AI.

## Overview

Transform your 7 JSON metadata files into a working Python script that generates your CAD model with custom parameters.

### What You Have

7 JSON files (your context package):
- `model.json` — Design geometry and features
- `context.json` — Design intent and constraints
- `metadata.json`, `parameters.json`, `constraints.json`, `features.json`, `assembly.json` — AI-ready specs

### What You Get

A complete Python script (`generate_yourmodel.py`) that:
- Accepts CLI parameters: `python generate_yourmodel.py --width 200 --output model.step`
- Validates inputs against design constraints
- Generates your CAD model with custom parameters
- Exports to STEP or STL format
- Works out of the box

---

## Workflow Overview

### Phase 1: Parse Context Package

Load all JSON files and extract:
- Parameter specs (name, type, range, default, validation)
- Feature timeline (order, type, dependencies)
- Constraint rules (tolerances, min/max, validation logic)
- CLI interface spec (arguments, help text)

### Phase 2: Design Script Structure

Create Python skeleton with:
```python
from cadquery import Workplane
import argparse

def generate_model(BaseWidth=200, BaseThickness=10, ...):
    """Generate model with given parameters"""
    validate_parameters(BaseWidth, BaseThickness, ...)
    # ... build features ...
    validate_model(model)
    return model

def main():
    parser = argparse.ArgumentParser(...)
    # ... CLI arguments ...
    args = parser.parse_args()
    model = generate_model(...)
    model.save(args.output, mode="STEP")

if __name__ == "__main__":
    main()
```

### Phase 3: Implement Features

For each feature in model.json timeline:

1. Read feature definition from model.json
2. Translate to CadQuery equivalent:

| Fusion 360 | CadQuery |
|-----------|----------|
| Extrude | `.extrude(depth)` |
| Pocket | `.pocket(depth)` or `.cboreHole()` |
| Hole | `.hole(diameter)` |
| Fillet | `.edges().fillet(radius)` |
| Pattern | `.rarray(spacing, count)` |

3. Implement in feature order from timeline

### Phase 4: Implement Validation

**Pre-generation** (validate parameters before building):
```python
def validate_parameters(**params):
    # Check ranges from parameters.json
    # Check constraints from constraints.json
    # Check dependencies
```

**Post-generation** (verify generated model):
```python
def validate_model(model, **params):
    # Check body count
    # Check volume/dimensions
    # Check critical features present
```

### Phase 5: Implement CLI Interface

From parameters.json, create argparse arguments:
```python
parser.add_argument("--width", type=float, default=200,
                    help="Width (100-300mm)")
parser.add_argument("--output", type=str, default="model.step",
                    help="Output filename")
```

---

## Sending to AI

### Generation Prompt

```
Generate a complete parameterized CadQuery Python script that:

1. Accepts all parameters from parameters.json as CLI arguments
2. Validates inputs against constraints.json (pre-generation)
3. Builds model following the feature timeline from model.json
4. Validates output (post-generation)
5. Exports to STEP or STL format

Requirements:
- Use template_generator.py as reference for code structure
- Study examples/generate_shelfbracket_example.py for patterns
- Follow naming conventions from Code Generation guide
- Include helpful error messages when constraints are violated
- Support both --output filename.step and .stl formats

Return the complete, working generate_yourmodel.py script.
```

### What to Include

1. All 7 JSON files from your context package
2. The generation prompt (above)
3. Reference to `examples/generate_shelfbracket_example.py` for patterns
4. Reference to `template_generator.py` for structure

---

## Feature Mapping Examples

**Base Extrude Feature:**
```python
def add_base_extrude(model, thickness):
    """Feature 1: Base Extrude - Extrude base profile"""
    return model.extrude(thickness)
```

**Mounting Holes:**
```python
def add_mounting_holes(model, width, hole_diameter):
    """Feature 3: Mounting Holes - Add 4 corner holes at 10mm inset"""
    positions = [(10, 10), (width-10, 10), (10, 150-10), (width-10, 150-10)]
    return model.faces(">Z").workplane().pushPoints(positions).hole(hole_diameter)
```

**Reinforcement Ribs:**
```python
def add_ribs(model, width, depth, height):
    """Feature 5: Reinforcement Ribs - Add ribs scaled with width"""
    spacing = width * 0.25
    for x in [spacing, spacing*2, spacing*3]:
        model = model.faces("<Z").workplane().center(x, 0).rect(3, depth*0.8).pocket(height)
    return model
```

---

## Testing Generated Code

```bash
# Show help
python generate_yourmodel.py --help

# Generate with defaults
python generate_yourmodel.py

# Test custom parameters
python generate_yourmodel.py --width 100 --output small.step

# Test error handling (should reject invalid params)
python generate_yourmodel.py --width 50 --output test.step  # Should error if < min
```

### Validation Checklist

- ✓ Script runs: `python generate_yourmodel.py --help`
- ✓ Default parameters match original model
- ✓ Model opens in CAD software (STEP/STL valid)
- ✓ Dimensions correct (±0.5mm tolerance)
- ✓ All features present in correct order
- ✓ Parameter variations work correctly
- ✓ Invalid parameters rejected with clear errors

---

## Naming Conventions

Standardized naming for consistency and maintainability.

### Script Names

**Pattern:** `generate_{model_name}.py`

Use model name in lowercase, no version numbers.

```
✓ generate_shelfbracket.py     (Model: ShelfBracket)
✓ generate_toolholder.py        (Model: ToolHolder)
✓ generate_pegboardtile.py      (Model: PegboardTile)

✗ generate_shelfbracketv1.py   (Remove version)
✗ ShelfBracket.py              (Keep lowercase)
```

### Function Names

**Feature Implementation:** `add_{FeatureName}`

Each feature from model.json timeline gets a function.

```python
def add_base_extrude(model, thickness):
    """Feature 1: Base Extrude"""

def add_mounting_holes(model, width, hole_diameter):
    """Feature 3: Mounting Holes"""

def add_reinforcement_ribs(model, width, height):
    """Feature 5: Reinforcement Ribs"""
```

**Sketch Creation:** `create_{SketchName}_sketch` or `get_{Thing}_positions`

```python
def create_base_profile_sketch(width, depth):
    """Create rectangular profile"""

def get_mounting_hole_positions(width, depth):
    """Calculate hole positions"""

def get_rib_positions(width, depth):
    """Calculate rib pattern positions"""
```

**Validation Functions:**

```python
def validate_parameters(BaseWidth, BaseThickness, ...):
    """Validate parameters before generation"""

def validate_model(model, BaseWidth, ...):
    """Validate generated model meets specs"""
```

### Parameter Names (Python)

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

### CLI Argument Names

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

### Constants

**Convention:** UPPERCASE_WITH_UNDERSCORES

Fixed values that never change (design rules).

```python
BASE_DEPTH = 150              # Must match aluminum post standard
MOUNTING_HOLE_INSET = 10      # Holes always 10mm from corners
RIB_EXTENSION_RATIO = 0.8     # Ribs extend to 80% of width
INTERNAL_FILLET_RADIUS = 1.0  # Minimum 1mm for FDM
```

### Derived Parameters

**Convention:** PascalCase (like user parameters)

Calculated from user parameters.

```python
BossHeight = BaseWidth * 0.15   # Scales with width
RibSpacing = BaseWidth * 0.25   # Rib array spacing
```

### Local Variables

**Convention:** lowercase_with_underscores

Temporary/computed values.

```python
profile_points = [(10, 10), (20, 10), ...]
hole_positions = get_mounting_hole_positions(width, depth)
model_volume = model.val().volume()
bounding_box = model.val().boundingBox()
```

### Output Files

**Pattern:** `{ModelName}_{Variant}.{ext}`

```
shelfbracket_small.step       # width=100mm variant
shelfbracket_medium.step      # width=200mm (default)
shelfbracket_large.step       # width=300mm variant
shelfbracket_custom.step      # user-specified parameters
```

### Documentation

**Docstrings:**

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

**Feature Comments:**

```python
def add_base_extrude(model, thickness):
    """
    Feature 1: Base Extrude
    
    Creates main body by extruding the base profile.
    This is foundational - all other features depend on it.
    """
    return model.extrude(thickness)
```

**Inline Comments:**

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

### Naming Quick Reference

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

### Consistency Checklist

Before finalizing generated code:

- [ ] Parameters use PascalCase (BaseWidth not base_width)
- [ ] CLI args use kebab-case (--corner-radius not --cornerRadius)
- [ ] Feature functions start with `add_` or `create_`
- [ ] Constants are UPPERCASE_UNDERSCORE
- [ ] Script named `generate_{model_name}.py` in lowercase
- [ ] All docstrings reference parameter names correctly
- [ ] No hardcoded values (all should be parameters or constants)

---

## References

- **Template:** `template_generator.py` (boilerplate skeleton)
- **Example:** `examples/generate_shelfbracket_example.py` (working code)
- **Data Format:** `docs/data_format_specification.md` (field reference)

---

## Next Steps

1. Send context package to AI with generation prompt
2. Receive `generate_yourmodel.py`
3. Test thoroughly with validation checklist
4. Use for model generation with custom parameters
