# STL Tool - Comprehensive Documentation

Complete STL file analysis for SCAD debugging. Combines dimensional and geometric inspection in a single unified tool.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Full Feature Reference](#full-feature-reference)
3. [Usage Modes](#usage-modes)
4. [Understanding the Analysis](#understanding-the-analysis)
5. [Examples](#examples)
6. [SCAD Debugging Workflow](#scad-debugging-workflow)
7. [Technical Details](#technical-details)

---

## Quick Start

### Installation

No external dependencies required. Python 3.6+ only.

```bash
chmod +x stl_tool.py
```

### Basic Commands

```bash
# Analyze a single file
python3 stl_tool.py model.stl

# Compare two models
python3 stl_tool.py --compare generated.stl reference.stl

# View only dimensions
python3 stl_tool.py --dimensions model.stl

# View only geometry metrics
python3 stl_tool.py --geometry model.stl

# View only detected features
python3 stl_tool.py --features model.stl

# Analyze multiple files
python3 stl_tool.py examples/*.stl

# Verbose output (with parsing details)
python3 stl_tool.py --verbose model.stl

# Show help
python3 stl_tool.py --help
```

### Common Tasks

**Quick size check:**
```bash
python3 stl_tool.py --dimensions model.stl
```

**Validate SCAD generator output:**
```bash
openscad -o /tmp/test.stl generator.scad
python3 stl_tool.py --compare /tmp/test.stl examples/reference.stl
```

**Review all example models:**
```bash
python3 stl_tool.py examples/*.stl
```

**Detailed analysis of a model:**
```bash
python3 stl_tool.py model.stl
```

---

## Full Feature Reference

### File Information

When analyzing any STL file, the tool reports:

- **Format**: ASCII or Binary (auto-detected)
- **File Path**: Full path to the file
- **Vertices**: Total number of coordinate points (3 per triangle)
- **Triangles**: Number of mesh faces

```
File Information:
  Format: Binary
  Path: examples/toolgrid_ratchet_1-4inch.stl
  Vertices: 119,232
  Triangles: 39,744
```

### Dimensional Analysis

Complete dimensional metrics for sizing and fitting:

- **Width (X)**: Left-right dimension
  - Shows exact measurement with min/max coordinates
  - Example: `29.5000 mm (-6.5000 to 23.0000)`

- **Height (Y)**: Front-back dimension
  - Shows exact measurement with min/max coordinates
  - Example: `13.0000 mm (-6.5000 to 6.5000)`

- **Depth (Z)**: Down-up dimension
  - Shows exact measurement with min/max coordinates
  - Example: `21.1000 mm (-6.0000 to 15.1000)`
  - Negative Z indicates features extending downward

- **Center Point**: Geometric center of the model
  - Useful for rotation and placement
  - Format: `(X, Y, Z)` coordinates

```
Dimensional Analysis:
  Width (X):  29.5000 mm (-6.5000 to 23.0000)
  Height (Y): 13.0000 mm (-6.5000 to 6.5000)
  Depth (Z):  21.1000 mm (-6.0000 to 15.1000)
  Center: (8.2500, 0.0000, 4.5500)
```

### Geometric Analysis

Measures model complexity and structure:

- **Complexity Level**: Classification of geometric detail
  - **Simple** (< 10 Z levels): Boxes, flat shapes
  - **Moderate** (10-50 Z levels): Some curves
  - **Complex** (50-100 Z levels): Curved surfaces
  - **Very Complex** (> 100 Z levels): Intricate geometry

- **Unique Z Levels**: Number of distinct horizontal slices
  - KEY METRIC for geometry complexity
  - More levels = more detail/curves
  - Flat box: ~5 levels
  - Curved cylinder: ~50-100 levels

- **Unique X/Y Levels**: Coordinate distribution granularity
  - Indicates complexity in horizontal plane
  - Higher values = more detailed geometry

```
Geometric Analysis:
  Complexity Level: Complex
  Unique Z Levels: 60
  Unique X Levels: 214
  Unique Y Levels: 131
```

### Feature Detection

Automatically identifies geometric features:

#### Mounting Pegs
- **What it detects**: Cylindrical protrusions extending downward
- **Detection method**: Identifies Z coordinates below -2mm
- **Information shown**: Height of extension
- **Example**: `✓ Mounting pegs: extend 6.00mm below base`
- **Indicates**: Model can mount on pegboard

#### Curved Surfaces
- **What it detects**: Cylindrical or rounded geometry
- **Detection method**: Analyzes coordinate distribution per Z level
- **What it means**: Non-flat surface geometry
- **Example**: `✓ Curved surfaces detected: cylindrical or rounded edges`
- **Indicates**: Model has cylinders, rounded corners, or smooth curves

#### Interior Cavities
- **What it detects**: Holes, voids, pockets within the model
- **Detection method**: Finds coordinate clusters with reduced range
- **Information shown**: Count of distinct cavities
- **Example**: `✓ Interior cavities: 16 distinct voids`
- **Indicates**: Support pins, ratchet heads, storage slots, etc.

#### Symmetry Detection
- **X-axis Symmetry**: Left-right balance
  - Example: `✓ X-axis symmetry detected`
  - Indicates: Balanced design

- **Y-axis Symmetry**: Front-back balance
  - Example: `✓ Y-axis symmetry detected`
  - Indicates: Balanced parametric design

#### Wall Thickness
- **What it estimates**: Structural wall thickness
- **Detection method**: Analyzes gaps in coordinate distribution
- **Information shown**: Estimated thickness in mm
- **Example**: `✓ Estimated wall thickness: 2.8mm`
- **Indicates**: Structural strength and material usage

```
Detected Features:
  ✓ Mounting pegs: extend 6.00mm below base
  ✓ Curved surfaces detected: cylindrical or rounded edges
  ✓ Interior cavities: 16 distinct voids
  ✓ Y-axis symmetry detected
  ✓ Estimated wall thickness: 2.8mm
```

### Shape Classification

Automatic shape type identification:

The tool infers the overall shape based on detected features:

- **Rectangular/box shape**: Simple box, no special features
- **Rectangular holder with mounting pegs**: Box with downward pegs
- **Cylindrical holder with mounting pegs**: Curved back with pegs
- **Curved/cylindrical shape (no pegs)**: Curved without mounting
- **With N cavities**: Appended to indicate internal structures

```
Estimated Shape:
  Cylindrical holder with mounting pegs with 16 cavities
```

### Surface Properties

Material and physical property estimates:

- **Volume**: Bounding box approximation
  - Formula: Width × Height × Depth
  - Unit: mm³
  - Use: Material volume estimate

- **Surface Area**: Bounding box approximation
  - Use: Approximate surface coverage
  - Unit: mm²

- **Weight (PLA)**: Material weight estimation
  - Formula: Volume (cm³) × 1.24 g/cm³
  - Default: PLA density (easily adjustable in source)
  - Use: Print time and cost estimation

```
Surface Properties:
  Est. Volume: 8,091.85 mm³
  Est. Surface Area: 2,560.50 mm²
  Est. Weight (PLA): 10.0g
```

---

## Usage Modes

### Mode 1: Full Comprehensive Analysis (Default)

Shows all available information about an STL file.

```bash
python3 stl_tool.py model.stl
```

**Output includes:**
- File information
- Dimensional analysis
- Geometric analysis
- Detected features
- Surface properties
- Shape classification

**Use when:** You want complete understanding of a model

**Example:**
```bash
$ python3 stl_tool.py examples/toolgrid_ratchet_1-4inch.stl

================================================================================
STL COMPREHENSIVE ANALYSIS: toolgrid_ratchet_1-4inch.stl
================================================================================

File Information:
  Format: Binary
  Path: examples/toolgrid_ratchet_1-4inch.stl
  Vertices: 119,232
  Triangles: 39,744

[... full analysis output ...]
```

### Mode 2: Dimensions Only

Shows only dimensional metrics.

```bash
python3 stl_tool.py --dimensions model.stl
```

**Output includes:**
- Format
- Exact dimensions (W × L × H)
- Bounding box coordinates
- Vertex and triangle counts

**Use when:** You only need size verification

**Example:**
```bash
$ python3 stl_tool.py --dimensions examples/toolgrid_tile_full.stl

toolgrid_tile_full.stl
----------------------------------------------------------------------
  Format: ASCII
  Dimensions (W × L × H): 155.47 × 155.47 × 8.00 mm
  Bounding box:
    X: 0.0000 to 155.4700 mm
    Y: 0.0000 to 155.4700 mm
    Z: 0.0000 to 8.0000 mm
  Vertices: 42,120
  Triangles: 14,040
```

### Mode 3: Geometry Only

Shows only geometric complexity metrics.

```bash
python3 stl_tool.py --geometry model.stl
```

**Output includes:**
- Complexity level
- Z-level count
- Shape type

**Use when:** You only need geometry details

**Example:**
```bash
$ python3 stl_tool.py --geometry examples/toolgrid_wrench_small.stl

toolgrid_wrench_small.stl - Geometric Analysis
----------------------------------------------------------------------
  Complexity: Very Complex
  Z Levels: 100
  Mounting Pegs: True
  Curved Surfaces: True
  Cavities: 75
  Shape: Cylindrical holder with mounting pegs with 75 cavities
```

### Mode 4: Features Only

Shows only detected features.

```bash
python3 stl_tool.py --features model.stl
```

**Output includes:**
- List of detected features with details
- Shape classification

**Use when:** You only need feature information

**Example:**
```bash
$ python3 stl_tool.py --features examples/toolgrid_wrench_small.stl

toolgrid_wrench_small.stl - Feature Analysis
----------------------------------------------------------------------
  Features: pegs(9.0mm), curves, cavities(75), x-sym, wall(1.1mm)
  Shape: Cylindrical holder with mounting pegs with 75 cavities
```

### Mode 5: Comparison

Detailed side-by-side comparison of two models.

```bash
python3 stl_tool.py --compare file1.stl file2.stl
```

**Output includes:**
- Full analysis of both files
- Dimensional comparison
- Geometric complexity comparison
- Feature-by-feature comparison
- Overall match assessment

**Use when:** Validating generated models against reference

**Example:**
```bash
$ python3 stl_tool.py --compare generated.stl examples/reference.stl

================================================================================
COMPREHENSIVE STL COMPARISON
generated.stl vs examples/reference.stl
================================================================================

Model 1: generated.stl
[... full analysis ...]

Model 2: examples/reference.stl
[... full analysis ...]

================================================================================
COMPARISON RESULTS
================================================================================

Dimensional Comparison:
  Width:     29.50mm vs    29.50mm (diff:    0.00mm)
  Height:    13.00mm vs    13.00mm (diff:    0.00mm)
  Depth:     21.10mm vs    21.10mm (diff:    0.00mm)

Geometric Comparison:
  Complexity: Complex vs Complex (Z levels: 60 vs 60)

Feature Comparison:
  Mounting pegs: True vs True
  Curved surfaces: True vs True
  Cavities: 16 vs 16

================================================================================
ASSESSMENT
================================================================================
✓ Dimensions match (within 0.5mm tolerance)
✓ Key features match (pegs, curves)
✓ Geometry complexity matches

================================================================================
✓✓✓ MODELS MATCH - Geometries are compatible
================================================================================
```

### Mode 6: Batch Analysis

Analyze multiple files with summary table.

```bash
python3 stl_tool.py examples/*.stl
```

**Output includes:**
- Summary table with all files
- Dimensions, complexity, and features for each
- Quick comparison overview

**Use when:** Reviewing multiple models at once

**Example:**
```bash
$ python3 stl_tool.py examples/toolgrid_*.stl

====================================================================================================
COMPREHENSIVE STL ANALYSIS - BATCH
====================================================================================================

File                                     Format   W×H×D              Complexity   Features
----------------------------------------------------------------------------------------------------
toolgrid_ratchet_1-4inch.stl             Binary   29.5×13.0×21.1     Complex      pegs, curves, cavities(16), sym, wall(2.8mm)
toolgrid_ratchet_3-8inch.stl             Binary   31.8×17.5×24.4     Complex      pegs, curves, cavities(23), sym, wall(3.5mm)
toolgrid_wrench_small.stl                Binary   23.0×23.5×42.0     Very Complex pegs, curves, cavities(75), sym, wall(1.1mm)
```

### Mode 7: Verbose Output

Includes parsing details for debugging.

```bash
python3 stl_tool.py --verbose model.stl
```

**Output includes:**
- All normal analysis
- Parsing method used
- Vertex count during parsing

**Use when:** Debugging parse issues

---

## Understanding the Analysis

### What Each Metric Means

#### Complexity Score (Z Levels)

The number of unique Z-level values indicates model complexity:

| Z Levels | Classification | Typical Model |
|----------|----------------|---------------|
| < 10 | Simple | Flat boxes, tiles |
| 10-50 | Moderate | Boxes with some curves |
| 50-100 | Complex | Cylinders, rounded shapes |
| > 100 | Very Complex | Intricate geometry, wrench holders |

**Why this matters for SCAD debugging:**
- If your generated model has 4 Z levels but reference has 60, you're missing curved surfaces
- If Z levels don't match, your geometry is incomplete

#### Mounting Pegs

**When you see:** `✓ Mounting pegs: extend 6.00mm below base`
- The model has pegboard compatibility
- Can mount on toolgrid or similar systems
- Pegs extend 6mm downward into pegboard holes

**When you see:** `✗ No mounting pegs detected`
- Missing pegboard mounting capability
- Model sits on surface instead
- Won't attach to pegboard grid

#### Curved Surfaces

**When you see:** `✓ Curved surfaces detected`
- Model has cylindrical or rounded geometry
- Uses smooth transitions, not sharp edges
- More 3D detail than simple box

**When you see:** `✗ No curved surfaces`
- Model is rectangular/flat
- Sharp edges throughout
- Simpler geometry

#### Cavities

**When you see:** `✓ Interior cavities: 16 distinct voids`
- Model has 16 holes or internal spaces
- Could be support pins, storage slots, etc.
- More complex internal structure

**Count examples:**
- Simple tile: 1 cavity (grid holes)
- Ratchet holder: 16 cavities (1 main + support pins)
- Wrench holder: 75 cavities (many small support points)

### Comparing Models

When using `--compare` mode, the assessment tells you:

**✓ MODELS MATCH**
- Dimensions within 0.5mm tolerance
- Key features match (pegs, curves)
- Complexity similar (within 30 Z levels)
- **Meaning:** Generated model is correct

**✗ MODELS DIFFER**
- One or more metrics significantly different
- **Meaning:** Investigate differences, fix SCAD

### Red Flags in Comparison

Look for these to identify SCAD issues:

```
✗ Mounting pegs: False vs True
```
→ SCAD script missing downward peg geometry

```
✗ Curved surfaces: False vs True
```
→ SCAD script using flat shapes instead of cylinders

```
Complexity: Simple vs Complex (64 Z level difference)
```
→ SCAD script generating too-simple geometry

```
Cavities: 1 vs 23
```
→ SCAD script missing interior feature subtraction

---

## Examples

### Example 1: Analyze a Model to Understand Its Structure

```bash
$ python3 stl_tool.py examples/toolgrid_wrench_small.stl
```

**What you learn:**
- Size: 23.0 × 23.5 × 42.0 mm (good for fitting in hand)
- Complexity: Very Complex (100+ Z levels - detailed geometry)
- Features: Pegs (9mm), curves, 75 cavities (lots of support)
- Weight: ~30g in PLA (moderate print)
- Shape: Cylindrical holder (tool-friendly shape)

### Example 2: Validate SCAD Generator Output

```bash
# Generate
openscad -o /tmp/test.stl -D 'drive_size="1-4"' ratchet-holder-generator.scad

# Analyze
python3 stl_tool.py /tmp/test.stl

# Compare
python3 stl_tool.py --compare /tmp/test.stl examples/toolgrid_ratchet_1-4inch.stl
```

**What to check:**
1. Dimensions match reference
2. Complexity similar (within 30 Z levels)
3. Features present (pegs: true, curves: true)
4. Cavities count similar
5. Overall assessment: MODELS MATCH or DIFFER

### Example 3: Quick Batch Review

```bash
# See all ratchet models at once
python3 stl_tool.py examples/toolgrid_ratchet*.stl

# Output shows:
# - Both 1/4" and 3/8" sizes
# - Both have pegs, curves, cavities
# - Different dimensions (expected)
# - Different complexity (3/8" slightly more complex)
```

### Example 4: Find Size Quickly

```bash
python3 stl_tool.py --dimensions model.stl
```

**Output shows:** Exact dimensions in mm, perfect for CAD software or printing

### Example 5: Debug Complexity Issue

```bash
# Your generated model:
python3 stl_tool.py /tmp/generated.stl
# → Shows: Complexity: Simple, Z Levels: 4

# Compare with reference:
python3 stl_tool.py --compare /tmp/generated.stl examples/reference.stl
# → Shows: Complexity: Simple vs Complex (64 Z level difference)

# Diagnosis: SCAD script not creating curved surfaces
# Solution: Add cylinder() or rotate_extrude() to SCAD
```

---

## SCAD Debugging Workflow

### Step-by-Step Process

#### 1. Write/Modify SCAD Script

Edit your `.scad` file with geometry changes.

#### 2. Generate Test Model

```bash
openscad -o /tmp/test.stl \
  -D 'parameter="value"' \
  your_generator.scad
```

#### 3. Analyze Generated Model

```bash
python3 stl_tool.py /tmp/test.stl
```

Check:
- ✓ Basic dimensions look right?
- ✓ Complexity reasonable?
- ✓ Features present?

#### 4. Compare with Reference

```bash
python3 stl_tool.py --compare /tmp/test.stl examples/reference.stl
```

Check overall assessment:
- ✓ MODELS MATCH? → Success! Proceed to testing
- ✗ MODELS DIFFER? → Analyze differences

#### 5. Analyze Specific Differences

```bash
# Just see features
python3 stl_tool.py --features /tmp/test.stl examples/reference.stl

# Or get detailed comparison output
python3 stl_tool.py --compare /tmp/test.stl examples/reference.stl
```

Look for:
- Missing pegs? Add cylinder/peg code
- No curves? Replace cubes with cylinders
- Too simple? Increase $fn, add details
- Wrong cavities? Check difference() operations

#### 6. Iterate

Modify SCAD → Regenerate → Analyze → Compare
Repeat until MODELS MATCH

#### 7. Export Final Model

Once comparison shows MODELS MATCH:

```bash
cp /tmp/test.stl models/my_model.stl
```

Verify one more time with final file:

```bash
python3 stl_tool.py --compare models/my_model.stl examples/reference.stl
```

#### 8. Commit to Repository

```bash
git add models/my_model.stl
git commit -m "Add new model - validated against reference"
```

### Common SCAD Issues & Fixes

#### Issue: Missing Mounting Pegs

**Symptom:**
```
Mounting pegs: False vs True
```

**Cause:** SCAD script not creating downward extensions

**Fix:** Add peg generation code
```scad
// Add pegs extending downward
module pegs() {
    translate([...]) cylinder(d=3.8, h=-6, $fn=20);
}
```

#### Issue: No Curved Surfaces

**Symptom:**
```
Curved surfaces: False vs True
Complexity: Simple vs Complex
```

**Cause:** Using cube() instead of cylinder()

**Fix:** Replace with curved geometry
```scad
// Instead of cube, use:
cylinder(d=housing_width, h=housing_depth, $fn=30);
```

#### Issue: Missing Cavities

**Symptom:**
```
Cavities: 1 vs 16
```

**Cause:** Not subtracting interior features

**Fix:** Use difference() to create cavities
```scad
difference() {
    // Main shape
    cube([width, height, depth]);
    
    // Subtract cavities
    translate([x, y, z]) cylinder(d=hole_d, h=hole_h, $fn=20);
}
```

#### Issue: Over-Complex Model

**Symptom:**
```
Complexity: Very Complex vs Complex (120 Z level difference)
```

**Cause:** Model more detailed than needed, excessive $fn value

**Fix:** Reduce detail level
```scad
// Change from:
cylinder(d=10, h=20, $fn=100);

// To:
cylinder(d=10, h=20, $fn=30);
```

---

## Technical Details

### Coordinate System

The tool uses standard 3D coordinates:

- **X (Width)**: Left-right direction
- **Y (Height)**: Front-back direction
- **Z (Depth)**: Down-up direction

**Special note for pegboard models:**
- Z = 0 is the mounting surface
- Negative Z values indicate downward features (pegs)
- Positive Z values indicate upward features (main housing)

### Format Detection

**ASCII STL**
- Human-readable text format
- Larger file sizes
- Auto-detected by looking for "solid" keyword
- Uses regex parsing

**Binary STL**
- Compact binary format
- Standard for CAD software
- Auto-detected after ASCII detection fails
- Uses struct unpacking

### Complexity Measurement

Z-level counting with 0.1mm precision:

1. Collect all Z coordinates
2. Round to 0.1mm precision
3. Count unique values
4. More values = more geometric detail

### Feature Detection Methods

**Mounting Pegs**
- Threshold: `min_z < -2`
- Measures: Distance below Z=0
- Detects: Any downward extending features

**Curved Surfaces**
- Method: Analyzes Y-coordinate distribution at each Z level
- Threshold: More than 15 unique Y values per Z level
- Samples: First 20 Z levels
- Requires: 5+ levels showing curvature

**Interior Cavities**
- Method: Finds coordinate clusters
- Threshold: X/Y range < 70% of overall model
- Counts: Distinct cavity regions
- Filters: Only clusters with 20+ vertices

**Symmetry**
- Method: Compares vertex count on each side of center
- Tolerance: Less than 10% asymmetry acceptable
- Types: X-axis and Y-axis checked independently

**Wall Thickness**
- Method: Analyzes gaps in coordinate distribution
- Source: Peaks and valleys in vertex density
- Limits: Capped at 20% of model width

### Performance

- **Small models** (< 50K vertices): < 100ms
- **Medium models** (100K vertices): < 500ms
- **Large models** (> 500K vertices): < 2s
- **Batch (13 files)**: < 5s total

Memory usage is proportional to vertex count (approximately 32 bytes per vertex).

### Compatibility

- **Python**: 3.6+
- **Operating Systems**: Linux, macOS, Windows
- **STL Formats**: ASCII and binary
- **Dependencies**: Python standard library only (no external packages)

### Modifying Material Density

To estimate weight for materials other than PLA, edit the source:

```python
# In print_properties() method, change:
density_pla = 1.24  # g/cm³ for PLA

# To your material:
density_pla = 1.04  # g/cm³ for PETG
density_pla = 1.18  # g/cm³ for ABS
```

---

## Tips & Best Practices

### For SCAD Developers

1. **Always compare with reference**: Use `--compare` before committing
2. **Check Z levels first**: Gives quick indication of complexity match
3. **Look for pegs and curves**: Two most commonly missing elements
4. **Verify cavities**: Important for functional designs
5. **Use batch mode for review**: See all variations at once

### For 3D Printing

1. **Check wall thickness**: Ensure 2mm+ for strength
2. **Review weight**: Plan print time and material
3. **Verify dimensions**: Before importing to slicer
4. **Analyze cavities**: Ensure support structures will work
5. **Check symmetry**: For aesthetic designs

### For Quality Assurance

1. **Batch analyze all variants**: Ensure consistency
2. **Compare against golden reference**: Detect regressions
3. **Archive analysis results**: Track design history
4. **Validate material estimates**: Match actual weights
5. **Monitor complexity trends**: Detect over-engineering

---

## Troubleshooting

### "File not found" Error

**Problem**: Script can't locate file

**Solution**:
```bash
# Check file exists
ls -la model.stl

# Use full path if needed
python3 stl_tool.py /full/path/to/model.stl
```

### "Failed to parse STL file" Error

**Problem**: File is corrupted or unsupported format

**Solution**:
```bash
# Check file type
file model.stl

# Check file integrity
head -c 100 model.stl  # ASCII should show "solid"
```

### Unexpected Complexity Scores

**Problem**: Z-level count seems wrong

**Solution**:
1. Check file is fully rendered in OpenSCAD (use spacebar preview)
2. Verify no rendering errors in console
3. Export only after clean preview

### Feature Detection Issues

**Problem**: Features not detected when they should be

**Solution**:
- Check threshold values in source code
- Verify model actually has the features (view in preview)
- Try different analysis mode (`--features`)

### Performance Issues

**Problem**: Script running slowly

**Solution**:
1. Try `--dimensions` mode instead of full analysis
2. Analyze single file instead of batch
3. Check available system memory

---

## Support & Contributing

For issues or improvements:

1. Check this documentation first
2. Review example models and tests
3. Test with `--verbose` mode for debugging
4. Report specific metrics that are unexpected

---

## Version Information

- **Created**: December 24, 2024
- **Status**: Production Ready
- **Python**: 3.6+
- **Dependencies**: None (standard library only)

---

## Quick Reference Cheat Sheet

```bash
# Most common commands
python3 stl_tool.py model.stl                           # Full analysis
python3 stl_tool.py --compare gen.stl ref.stl          # Validate
python3 stl_tool.py --dimensions model.stl              # Size check
python3 stl_tool.py examples/*.stl                      # Batch review
python3 stl_tool.py --features model.stl                # Feature check
python3 stl_tool.py --geometry model.stl                # Complexity check
python3 stl_tool.py --help                              # Show help

# SCAD workflow
openscad -o /tmp/test.stl -D 'param="value"' gen.scad
python3 stl_tool.py --compare /tmp/test.stl examples/ref.stl

# Interpretation quick guide
✓ MODELS MATCH               → Generated model is correct
✗ MODELS DIFFER              → SCAD needs fixing
False vs True (any feature)  → Missing that feature type
Z level diff > 30            → Geometry significantly different
```

