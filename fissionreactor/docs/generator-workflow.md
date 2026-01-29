# Generate Code from Context Package

Detailed workflow for generating parameterized Python code from your context files.

## Input & Output

**Input:** 7 JSON files (context package)  
**Output:** `generate_yourmodel.py` (working Python script)

## 5-Phase Generation Workflow

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

def generate_model(param1=100, param2=200, ...):
    """Generate model with given parameters"""
    validate_parameters(param1, param2, ...)
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

## Feature Mapping Examples

**Base Extrude Feature:**
```python
def add_base_extrude(wp, thickness):
    """Extrude base profile"""
    return wp.extrude(thickness)
```

**Mounting Holes:**
```python
def add_mounting_holes(model, width, hole_diameter):
    """Add 4 corner holes at 10mm inset"""
    positions = [(10, 10), (width-10, 10), (10, 150-10), (width-10, 150-10)]
    return model.faces(">Z").workplane().pushPoints(positions).hole(hole_diameter)
```

**Reinforcement Ribs:**
```python
def add_ribs(model, width, depth, height):
    """Add ribs scaled with width"""
    spacing = width * 0.25
    for x in [spacing, spacing*2, spacing*3]:
        model = model.faces("<Z").workplane().center(x, 0).rect(3, depth*0.8).pocket(height)
    return model
```

## Template Structure

See `template_generator.py` for boilerplate with all sections:
- Imports and constants
- Parameter validation
- Helper functions (sketches, patterns)
- Feature functions (one per timeline feature)
- Main generation function
- CLI interface
- Error handling

## Example Reference

Study `examples/generate_shelfbracket_example.py` for:
- How to structure a complete script
- How to validate all constraints
- How to handle parameter relationships
- How to implement multiple features in order
- How to create proper CLI help text

## Success Criteria

✓ Script runs: `python generate_yourmodel.py --help`  
✓ Default parameters match original model  
✓ Model opens in CAD software (STEP/STL valid)  
✓ Dimensions correct (±0.5mm tolerance)  
✓ All features present in correct order  
✓ Parameter variations work correctly  
✓ Invalid parameters rejected with clear errors

## Naming Conventions

See `generator-guide_naming-conventions.md` for:
- Script names: `generate_{model_name}.py`
- Function names: `add_{FeatureName}()`, `create_{Sketch}()`
- Parameter names: `PascalCase` in Python, `kebab-case` for CLI
- Constants: `UPPERCASE_UNDERSCORE`

## Common Patterns

**Derived Parameters:**
```python
RibSpacing = BaseWidth * 0.25  # Calculate from user param
BossHeight = BaseWidth * 0.15
```

**Workplane Selection:**
```python
model.faces(">Z")    # Top face
model.faces("<Z")    # Bottom face
model.edges(">Z")    # Top edges
```

**Array Patterns:**
```python
wp.rarray(spacing, count)      # Rectangular array
wp.polarArray(radius, count)   # Polar array
wp.pushPoints(positions)       # Multiple points
```

## Testing Workflow

1. Verify script imports correctly
2. Test default parameters produce valid model
3. Test boundary conditions (min/max parameters)
4. Test invalid parameters (should error with helpful message)
5. Test variations (different parameter combinations)
6. Verify output files (open in CAD, check dimensions)

## Next Steps

1. Send context package to AI with generation prompt
2. Receive `generate_yourmodel.py`
3. Test thoroughly
4. Use for model generation with custom parameters
