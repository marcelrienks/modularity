# Parameterized Script Generation Guide

## Overview

This guide documents how to transform a **context package** (5 JSON files from Task 3) into a **parameterized Python generator script** that produces CAD models with variations.

**Input:** Complete context package (model.json, context.json, metadata.json, parameters.json, constraints.json)
**Output:** Working Python script (e.g., `generate_shelfbracket.py`)
**Success:** Generated script produces models identical to original, handles variations correctly, validates inputs

---

## Code Generation Workflow

### Phase 1: Parse Context Package (AI or Human)

**Input:** 5 JSON files
**Output:** In-memory data structures understanding the model

```python
import json

def load_context_package(package_path):
    """Load all 5 JSON files from context package"""
    model = json.load(open(f"{package_path}/model.json"))
    context = json.load(open(f"{package_path}/context.json"))
    metadata = json.load(open(f"{package_path}/metadata.json"))
    parameters = json.load(open(f"{package_path}/parameters.json"))
    constraints = json.load(open(f"{package_path}/constraints.json"))
    
    return {
        "model": model,
        "context": context,
        "metadata": metadata,
        "parameters": parameters,
        "constraints": constraints
    }
```

**What to extract:**
- Parameter specs (name, type, range, default, validation)
- Feature timeline (order, type, inputs)
- Sketch definitions (geometry, constraints)
- Constraint rules (tolerances, minimums, dependencies)
- CLI interface spec (arguments, defaults)

### Phase 2: Design Script Structure

**Output:** Python script skeleton with all parameters and functions

```python
from cadquery import Workplane
import argparse
import json

def generate_model(
    BaseWidth=200,
    BaseThickness=10,
    CornerRadius=1.5,
    MountingHoleDiameter=3.2,
    MinWallThickness=2,
    RibHeight=5
):
    """Generate ShelfBracket model with given parameters"""
    
    # Pre-generation validation
    validate_parameters(BaseWidth, BaseThickness, CornerRadius, 
                       MountingHoleDiameter, MinWallThickness, RibHeight)
    
    # Build model step by step
    model = create_base_profile(BaseWidth, BaseThickness, CornerRadius)
    model = add_mounting_holes(model, BaseWidth, MountingHoleDiameter)
    model = add_reinforcement_ribs(model, BaseWidth, RibHeight, MinWallThickness)
    model = apply_fillets(model, CornerRadius)
    
    # Post-generation validation
    validate_model(model)
    
    return model

def main():
    parser = argparse.ArgumentParser(description="Generate ShelfBracket models")
    parser.add_argument("--width", type=float, default=200, 
                       help="Bracket width (100-300mm)")
    parser.add_argument("--thickness", type=float, default=10,
                       help="Bracket height (8-12mm)")
    # ... more arguments
    parser.add_argument("--output", type=str, default="shelfbracket.step",
                       help="Output filename (STEP or STL)")
    
    args = parser.parse_args()
    
    # Generate model
    model = generate_model(
        BaseWidth=args.width,
        BaseThickness=args.thickness,
        # ... more parameters
    )
    
    # Export
    if args.output.endswith(".stl"):
        model.save(args.output, mode="STL")
    else:
        model.save(args.output, mode="STEP")

if __name__ == "__main__":
    main()
```

### Phase 3: Implement Features

**For each feature in model.json timeline:**

1. Read feature definition (name, type, inputs, parameters)
2. Translate to CadQuery equivalent
3. Add to model in sequence

**Feature Mapping - Fusion 360 to CadQuery:**

| Fusion 360 | CadQuery | Example |
|-----------|---------|---------|
| Extrude | `.extrude()` | `wp.extrude(BaseThickness)` |
| Pocket | `.cboreHole()` or `.pocket()` | `wp.pocket(10).through()` |
| Fillet | `.edges()` then `.fillet()` | `model.edges().fillet(1.5)` |
| Sketch + Extrude | `.sketch()` then `.extrude()` | `wp.sketch("ProfileSketch").extrude(10)` |
| Pattern | `.polarArray()` or `.rarray()` | `wp.rarray(spacing, 4)` |

### Phase 4: Implement Validation

**Pre-generation validation (parameters valid before generating):**

```python
def validate_parameters(BaseWidth, BaseThickness, CornerRadius, 
                       MountingHoleDiameter, MinWallThickness, RibHeight):
    """Validate all parameters before generation"""
    
    # Range checks
    if not (100 <= BaseWidth <= 300):
        raise ValueError(f"BaseWidth must be 100-300mm, got {BaseWidth}")
    if BaseWidth % 10 != 0:
        raise ValueError(f"BaseWidth must be multiple of 10, got {BaseWidth}")
    
    if not (1.5 <= MinWallThickness <= 3):
        raise ValueError(f"MinWallThickness must be 1.5-3mm, got {MinWallThickness}")
    if MinWallThickness < 1.5:
        raise ValueError("CRITICAL: MinWallThickness < 1.5mm causes structural failure")
    
    # Dependency checks
    if MountingHoleDiameter < 3.0:
        raise ValueError("Mounting holes < 3mm won't print")
    
    if CornerRadius < 1.5:
        raise ValueError("Corner radius < 1.5mm unreliable for FDM printing")
```

**Post-generation validation (model is correct after generating):**

```python
def validate_model(model):
    """Validate generated model meets specifications"""
    
    # Body count
    solids = model.val().solids()
    if len(solids) != 1:
        raise ValueError(f"Expected 1 body, got {len(solids)}")
    
    # Volume reasonability
    volume = model.val().volume()
    if not (50000 <= volume <= 150000):
        raise ValueError(f"Volume {volume}mm³ outside expected range (50k-150k)")
    
    # Bounding box
    bbox = model.val().boundingBox()
    if abs(bbox.xlen - BaseWidth) > 2:
        raise ValueError(f"Width mismatch: {bbox.xlen}mm vs {BaseWidth}mm")
    
    # Check mounting holes present
    holes = [f for f in model.faces() if f.geomType() == "PLANE"]
    if len(holes) < 4:
        raise ValueError("Missing mounting holes")
```

### Phase 5: Implement CLI Interface

**From parameters.json:**

```python
def main():
    parser = argparse.ArgumentParser(
        description="Generate ShelfBracket models with custom parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_shelfbracket.py --width 100 --output small.step
  python generate_shelfbracket.py --width 200 --thickness 10 --output medium.step
  python generate_shelfbracket.py --width 300 --rib-height 6 --output custom.step
        """
    )
    
    # Variable parameters (from parameters.json)
    parser.add_argument(
        "--width", type=float, default=200,
        metavar="MM", help="Bracket width (100-300mm, step 10)"
    )
    parser.add_argument(
        "--thickness", type=float, default=10,
        metavar="MM", help="Bracket height (8-12mm, step 1)"
    )
    parser.add_argument(
        "--corner-radius", type=float, default=1.5,
        metavar="MM", help="External corner radius (1.5-3mm, FDM minimum 1.5mm)"
    )
    parser.add_argument(
        "--hole-diameter", type=float, default=3.2,
        metavar="MM", help="M3 mounting hole diameter (3.0-3.5mm)"
    )
    parser.add_argument(
        "--wall-thickness", type=float, default=2,
        metavar="MM", help="Minimum wall thickness (1.5-3mm, CRITICAL below 1.5mm)"
    )
    parser.add_argument(
        "--rib-height", type=float, default=5,
        metavar="MM", help="Reinforcement rib height (3-8mm)"
    )
    
    # Output options
    parser.add_argument(
        "--output", type=str, default="shelfbracket.step",
        metavar="FILE", help="Output filename (STEP or STL format)"
    )
    parser.add_argument(
        "--format", type=str, choices=["step", "stl"], default="step",
        help="Output format (auto-detected from extension if omitted)"
    )
    
    args = parser.parse_args()
    
    # Generate
    try:
        model = generate_model(
            BaseWidth=args.width,
            BaseThickness=args.thickness,
            CornerRadius=args.corner_radius,
            MountingHoleDiameter=args.hole_diameter,
            MinWallThickness=args.wall_thickness,
            RibHeight=args.rib_height
        )
        
        # Export
        format_ext = args.output.split(".")[-1].upper()
        format = args.format.upper() if args.format else format_ext
        
        model.save(args.output, mode=format)
        print(f"✓ Generated: {args.output} ({format})")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
        return 1
    
    return 0
```

---

## Template Structure

The generated script should follow this structure:

```python
"""
Generate ShelfBracket models with parameter variations.

This script was auto-generated from a context package:
- Source: ShelfBracket_v1.f3d
- Generated: 2026-01-27
- Parameters: 8 (4 variable, 2 fixed, 2 derived)
- Features: 12 in sequence
"""

from cadquery import Workplane, selectors
import argparse
import sys

# ============================================================================
# PARAMETERS & VALIDATION
# ============================================================================

def validate_parameters(**params):
    """Validate parameters before generation"""
    # Range checks from constraints.json
    # Dependency checks
    # Severity level checks (CRITICAL, HIGH, MEDIUM)
    pass

def validate_model(model, **params):
    """Validate generated model meets specs"""
    # Geometry checks
    # Volume/dimensions checks
    # Feature presence checks
    pass

# ============================================================================
# HELPER FUNCTIONS - SKETCHES & PATTERNS
# ============================================================================

def create_base_profile(width, depth, radius):
    """Create rectangular profile with rounded corners"""
    return (Workplane("XY")
            .box(width, depth, 0.1)  # Simplified for sketch
            .edges()
            .fillet(radius))

def create_mounting_holes_sketch(width, depth, hole_diameter):
    """Create 4 corner mounting holes"""
    wp = Workplane("XY")
    # Add 4 circles at corners with 10mm inset
    positions = [(10, 10), (width-10, 10), (10, depth-10), (width-10, depth-10)]
    for x, y in positions:
        wp = wp.center(x, y).circle(hole_diameter/2).center(-x, -y)
    return wp

# ============================================================================
# FEATURE GENERATION
# ============================================================================

def add_base_extrude(wp, thickness):
    """Feature 1: Base Extrude"""
    return wp.extrude(thickness)

def add_mounting_holes(model, hole_diameter):
    """Feature 4: Mounting Holes (pocket through-all)"""
    return model.faces(">Z").workplane().pushPoints([...]).cboreHole(...)

def add_reinforcement_ribs(model, width, height, min_wall_thickness):
    """Feature 5: Reinforcement Ribs"""
    # Add ribs spaced at BaseWidth * 0.25
    pass

def apply_fillets(model, corner_radius):
    """Features 6-7: Corner and edge fillets"""
    return model.edges(">Z or <Z").fillet(corner_radius)

# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_model(
    BaseWidth=200,
    BaseThickness=10,
    CornerRadius=1.5,
    MountingHoleDiameter=3.2,
    MinWallThickness=2,
    RibHeight=5
):
    """Generate ShelfBracket model with given parameters"""
    
    # Validate inputs
    validate_parameters(
        BaseWidth=BaseWidth,
        BaseThickness=BaseThickness,
        CornerRadius=CornerRadius,
        MountingHoleDiameter=MountingHoleDiameter,
        MinWallThickness=MinWallThickness,
        RibHeight=RibHeight
    )
    
    # Derived parameters
    RibSpacing = BaseWidth * 0.25
    BossHeight = BaseWidth * 0.15
    BaseDepth = 150  # Fixed
    
    # Build in feature order from model.json
    model = create_base_profile(BaseWidth, BaseDepth, CornerRadius)
    model = add_base_extrude(model, BaseThickness)
    model = add_mounting_holes(model, MountingHoleDiameter)
    model = add_reinforcement_ribs(model, BaseWidth, RibHeight, MinWallThickness)
    model = apply_fillets(model, CornerRadius)
    
    # Validate output
    validate_model(model, BaseWidth=BaseWidth)
    
    return model

# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate ShelfBracket models",
        epilog="Examples:\n"
               "  python generate_shelfbracket.py --width 100\n"
               "  python generate_shelfbracket.py --width 300 --output custom.stl"
    )
    
    parser.add_argument("--width", type=float, default=200,
                       help="Width (100-300mm, step 10)")
    parser.add_argument("--thickness", type=float, default=10,
                       help="Height (8-12mm)")
    parser.add_argument("--corner-radius", type=float, default=1.5,
                       help="Corner radius (1.5-3mm, min 1.5 for FDM)")
    parser.add_argument("--hole-diameter", type=float, default=3.2,
                       help="Hole diameter (3.0-3.5mm for M3)")
    parser.add_argument("--wall-thickness", type=float, default=2,
                       help="Wall thickness (1.5-3mm, CRITICAL below 1.5)")
    parser.add_argument("--rib-height", type=float, default=5,
                       help="Rib height (3-8mm)")
    parser.add_argument("--output", type=str, default="shelfbracket.step",
                       help="Output file (STEP or STL)")
    
    args = parser.parse_args()
    
    try:
        model = generate_model(
            BaseWidth=args.width,
            BaseThickness=args.thickness,
            CornerRadius=args.corner_radius,
            MountingHoleDiameter=args.hole_diameter,
            MinWallThickness=args.wall_thickness,
            RibHeight=args.rib_height
        )
        
        format = "STEP" if args.output.endswith(".step") else "STL"
        model.save(args.output, mode=format)
        print(f"✓ Generated: {args.output}")
        return 0
        
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## Naming Conventions

### Script Names

Pattern: `generate_{ModelName}.py`

**Examples:**
- `generate_shelfbracket.py` - Model name: ShelfBracket
- `generate_toolholder.py` - Model name: ToolHolder
- `generate_pegboardtile.py` - Model name: PegboardTile

**Guidelines:**
- Lowercase with underscores
- Remove version numbers (ShelfBracket_v1 → shelfbracket, not shelfbracketv1)
- Use singular form (bracket not brackets)
- Keep name short but descriptive

### Function Names

**Feature implementation functions:**
- Prefix: `add_` or `create_`
- Pattern: `add_{FeatureName}` where FeatureName is CamelCase from model.json

**Examples:**
```python
def add_base_extrude():      # Feature name: "Base Extrude"
def add_mounting_holes():    # Feature name: "Mounting Holes"
def add_tapered_walls():     # Feature name: "Tapered Walls"
def add_corner_fillet():     # Feature name: "Corner Fillet"
```

**Sketch functions:**
- Prefix: `create_` (sketches are created, not added)
- Pattern: `create_{SketchName}_sketch`

**Examples:**
```python
def create_base_profile_sketch():
def create_mounting_holes_sketch():
def create_rib_pattern_sketch():
```

**Validation functions:**
- `validate_parameters(**params)` - Pre-generation validation
- `validate_model(model, **params)` - Post-generation validation

### Parameter Names

Use exact names from parameters.json:
- `BaseWidth` (not width, W, base_width)
- `CornerRadius` (not corner_radius, radius, r)
- `MinWallThickness` (not min_wall_thickness, wall_thick)

**CLI Arguments** (kebab-case):
- `--width` (from BaseWidth)
- `--corner-radius` (from CornerRadius)
- `--wall-thickness` (from MinWallThickness)
- `--hole-diameter` (from MountingHoleDiameter)

### File Naming (Output Models)

Pattern: `{ModelName}_{VariantDescription}.{ext}`

**Examples:**
- `shelfbracket_small.step` (width=100mm variant)
- `shelfbracket_medium.step` (width=200mm variant)
- `shelfbracket_large.step` (width=300mm variant)
- `shelfbracket_custom.stl` (user-specified parameters)

---

## Success Criteria for Generated Scripts

### ✅ Correctness
- [ ] Script generates valid 3D model (opens in CAD software)
- [ ] Default parameters produce model matching original Fusion 360
- [ ] Dimensions within ±0.5mm of original
- [ ] All features present in correct order
- [ ] All mounting holes/features in correct positions

### ✅ Parameterization
- [ ] All variable parameters accepted as CLI arguments
- [ ] Changing parameters produces different models
- [ ] Derived parameters calculated correctly
- [ ] Fixed parameters cannot be overridden

### ✅ Validation
- [ ] Pre-generation validation rejects invalid inputs
- [ ] Validation error messages are clear and actionable
- [ ] Post-generation validation confirms model correctness
- [ ] CRITICAL constraints enforced (parameter validation fails < 1.5mm walls)
- [ ] HIGH constraints warned (parameter validation warns overhang > 45°)

### ✅ Quality
- [ ] Code is readable and well-commented
- [ ] Docstrings on all functions
- [ ] No hardcoded values (all parameters used)
- [ ] Proper error handling
- [ ] Both STEP and STL export work

### ✅ Documentation
- [ ] Script has docstring explaining purpose
- [ ] CLI help is accurate (--help works)
- [ ] Example commands in epilog
- [ ] Comments explain non-obvious CadQuery operations

---

## Common Pitfalls

### ❌ Hard-Coded Values
```python
BAD:  model = wp.extrude(10)  # Uses fixed 10 instead of parameter
GOOD: model = wp.extrude(BaseThickness)  # Uses parameter
```

### ❌ Wrong Feature Order
```python
BAD:  Create fillets, then add holes (holes get filleted!)
GOOD: Add all features, then apply fillets last
```

### ❌ Missing Validation
```python
BAD:  def generate_model(BaseWidth): ...  # Accepts any value
GOOD: def generate_model(BaseWidth):
          validate_parameters(BaseWidth=BaseWidth)  # Validates first
```

### ❌ Vague Error Messages
```python
BAD:  raise ValueError("Invalid width")
GOOD: raise ValueError(f"BaseWidth must be 100-300mm, got {BaseWidth}. "
                       "Width also must be multiple of 10.")
```

### ❌ Missing Derived Parameters
```python
BAD:  Only implements 4 parameters, ignores RibSpacing = BaseWidth * 0.25
GOOD: Calculates derived parameters: RibSpacing = BaseWidth * 0.25
```

---

## Workflow Summary

```
Context Package (5 JSON files)
         ↓
Parse & Extract Specifications
         ↓
Design Script Structure
  (parameters, functions, CLI)
         ↓
Implement Features (timeline order)
         ↓
Implement Validation
  (pre-generation + post-generation)
         ↓
Implement CLI Interface
         ↓
Test Against Original Model
  (default parameters match)
         ↓
Test Variations
  (different parameter values work)
         ↓
Test Error Cases
  (invalid inputs rejected)
         ↓
Generate Production Script
```

---

## Next: See Example Scripts

- `template_generator.py` - Boilerplate skeleton with all sections
- `generate_shelfbracket_example.py` - Full working example for ShelfBracket_v1
- Real integration with example-context/ for verification
