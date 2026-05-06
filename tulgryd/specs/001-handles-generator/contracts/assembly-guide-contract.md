# Contract: Assembly Guide Template

**Phase**: 1 (Design)  
**Feature**: Parametric Handles Generator  
**Date**: 2026-05-06  
**Contract Type**: Assembly guide markdown template specification

## Template Overview

Assembly guides are auto-generated Markdown documents paired with each handle model. They provide specifications, print settings, and usage instructions tailored to the specific `(diameter, height)` parameters.

**File**: `handle_d{diameter}_h{height}_README.md`  
**Generator**: Jinja2 template + parameter injection (assembly_guide.py)  
**Regenration**: Every model generation; overwrites on repeat parameters

## Template Structure

```jinja2
# Handle d{{ diameter }}mm h{{ height }}mm

*Auto-generated {{ generated_timestamp }} by ToolGrid Handles Generator*

## Quick Facts

| Property | Value |
|----------|-------|
| Diameter | {{ diameter }} mm |
| Height | {{ height }} mm |
| Material | PLA (recommended) |
| Print time | ~45–60 min (FDM, typical) |
| Layer count | {{ layer_count }} |
| Grid compatibility | ToolGrid 10mm spacing |

## Template Variables & Calculation

| Variable | Source | Example |
|----------|--------|---------|
| `{{ diameter }}` | User input (--diameter) | `2.6` |
| `{{ height }}` | User input (--height) | `2.0` |
| `{{ layer_count }}` | Auto-calculated: `ceil(height / 0.2)` | `10` |
| `{{ generated_timestamp }}` | System (ISO 8601) | `2026-05-06T14:30:00Z` |

### Layer Count Formula

```
layer_count = ceil(height_mm / 0.2)
```

**Examples**:
- height = 0.5mm → ceil(0.5 / 0.2) = 3 layers
- height = 1.0mm → ceil(1.0 / 0.2) = 5 layers
- height = 2.0mm → ceil(2.0 / 0.2) = 10 layers
- height = 2.5mm → ceil(2.5 / 0.2) = 13 layers

**Interpretation**: Assumes 0.2mm standard layer height (industry default). Adjustment optional.

## Print Settings

### Recommended (PLA)

```
Nozzle temperature:    200–210°C
Bed temperature:       60°C
Print speed:           40 mm/s
Layer height:          0.2 mm
Infill:                20% (grid)
Supports:              None
Adhesion:              Brim (optional)
```

### Alternative Materials

**PETG** (more durable):
- Nozzle: 220–230°C
- Bed: 80°C
- Speed: 35 mm/s (slower for strength)

**TPU** (flexible grip):
- Nozzle: 210–230°C (material-dependent)
- Bed: Room temperature or 60°C
- Speed: 20 mm/s (flexible materials need slower extrusion)

## Assembly & Usage

### Step 1: Print the Model

Print the `handle_d{{ diameter }}_h{{ height }}.stl` file on your FDM 3D printer using settings above.

### Step 2: Post-Processing

1. Remove from print bed (if stuck, use spatula)
2. Clean support material (none expected; design is optimized)
3. Optional: Sand surface with 120–220 grit for smooth finish
4. Inspect layers for uniformity (visible layer lines are normal)

### Step 3: Attach to ToolGrid

1. Locate mounting interface (base of handle)
2. Align grip with ToolGrid peg holes (10mm spacing)
3. Press firmly downward (magnetic interface, if equipped)
4. Verify handle is secure (no wobbling)

### Step 4: Insert Tool

1. Insert tool shaft into grip diameter ({{ diameter }} mm)
2. Rotation should be smooth with slight friction
3. Tool should be removable without excessive force
4. If tool slips: Possibly too loose (see Troubleshooting)

## Specifications

### Geometric Parameters

```
Grip Diameter:  {{ diameter }} mm
Grip Height:    {{ height }} mm
Base Width:     10 mm (standard ToolGrid)
Material:       PLA / PETG / TPU (user choice)
Structural:     Solid (no hollow sections)
```

### Reference Parameters (Locked)

These design parameters are fixed and ensure structural integrity:

```
Wall Thickness:   0.6–0.8 mm (layer-dependent)
Fillet Radius:    0.3 mm (all edges)
Mounting Pegs:    3.8 mm diameter (interlocking)
Tolerance:        ±0.1 mm (design nominal)
```

*Reference parameters are optimized for ToolGrid system; modifications may break compatibility.*

## Troubleshooting

### Print Quality Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Layer separation | Temperature too low | +5°C nozzle temp |
| Stringing | Temperature too high | -10°C nozzle temp |
| Warping | Bed not level | Re-calibrate bed |
| Incomplete top | Infill too low | Re-print with 30% infill |
| First layer fails | Bad bed adhesion | Clean bed with IPA, roughen if smooth |

### Grip Fit Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Tool slips out | Grip too loose | Re-generate with `--diameter {{ diameter + 0.2 }}` |
| Tool won't fit | Grip too tight | Re-generate with `--diameter {{ diameter - 0.1 }}` |
| Tool only fits halfway | Diameter OK, height wrong | Re-generate with adjusted `--height` |
| Inconsistent fit | Material deformation | Check temperature; ensure PLA (not TPU) at rest |

### File & Model Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| STL file corrupted | Export error (rare) | Re-generate with same parameters |
| STEP file won't import | Format error | Report issue with command used |
| Dimensions wrong in final print | Calibration issue | Check printer firmware Z-offset |

## Advanced Customization

### Re-generate with Adjusted Parameters

If grip is too loose/tight after test print:

```bash
# Original
python generate.py --diameter {{ diameter }} --height {{ height }}

# Grip too loose? Increase diameter
python generate.py --diameter {{ diameter + 0.2 }} --height {{ height }}

# Grip too tight? Decrease diameter
python generate.py --diameter {{ diameter - 0.1 }} --height {{ height }}

# Prefer longer grip? Increase height
python generate.py --diameter {{ diameter }} --height {{ height + 0.3 }}
```

Repeat test prints with ±0.1 mm adjustments until fit is perfect.

### Combine Multiple Handles

You can print multiple handles in one job:

```bash
# Generate two handles with different diameters
python generate.py --diameter 2.6 --height 2.0
python generate.py --diameter 3.0 --height 1.5

# Both files in ./output/
# Arrange on build plate in your slicer software
```

## Material Recommendations

### Best for 3D Printing: **PLA**
- Easy to print (low warping)
- Good detail (sharp edges)
- Recommended for most users

### Best for Durability: **PETG**
- More flexible than PLA
- Resists impact better
- Tolerates higher temperatures
- Slightly harder to print (calibration critical)

### Best for Flexibility: **TPU**
- Grip material (highly flexible)
- Comfortable for extended use
- Most difficult to print (requires slow speed)
- Not recommended for beginners

**Default recommendation**: PLA (ease + reliability)

## Maintenance & Storage

- **Storage**: Cool, dry place (away from sunlight)
- **Cleaning**: Warm soapy water; dry thoroughly
- **Life expectancy**: 1–5 years (PLA), 5+ years (PETG/TPU) with normal use
- **Replacement**: Re-print when handle shows cracks or deformation

## Support & Documentation

For more information:
- **Generator options**: `python generate.py --help`
- **Project repo**: [ToolGrid modularity repository]
- **Issue tracking**: Report bugs/improvements via GitHub Issues
- **Design source**: `handles/origin/handles.json` (parametric design data)

---

**Generated**: {{ generated_timestamp }}  
**Model**: handle_d{{ diameter }}_h{{ height }}  
**Generator version**: 1.0  
**ToolGrid version**: Compatible with all ToolGrid systems using 10mm hole spacing

```

## Template Parameters (Jinja2 Substitution)

| Variable | Type | Source | Example |
|----------|------|--------|---------|
| `{{ diameter }}` | float | User input | 2.6 |
| `{{ height }}` | float | User input | 2.0 |
| `{{ generated_timestamp }}` | ISO 8601 | datetime.now() | 2026-05-06T14:30:45Z |
| `{{ layer_count }}` | int | Calculated from height | 10 |

### Calculated Variables

- `{{ layer_count }}` = `ceil(height / 0.2)` — assuming 0.2mm layer height
- `{{ generated_timestamp }}` = Python `datetime.now(timezone.utc).isoformat()`

## Validation Checklist

Template must generate markdown that:

- [ ] Renders correctly in GitHub flavored markdown (GFM)
- [ ] All code blocks have proper syntax highlighting (bash, yaml, etc.)
- [ ] All tables render correctly
- [ ] All links work (or are marked as TBD)
- [ ] No missing template variables (all {{ }} filled)
- [ ] Filename matches `handle_d{d}_h{h}_README.md`
- [ ] Timestamp is accurate and formatted as ISO 8601
- [ ] Material recommendations are concrete (not generic)
- [ ] Troubleshooting table is actionable (not vague)
- [ ] Print settings are tested/recommended (not guesses)

## Generation Rules

1. **One guide per model**: Each handle model paired with exactly one guide
2. **Overwrite on repeat**: If parameters repeated, README overwrites (no versioning)
3. **Parallel naming**: README name matches model filename (except for `_README.md` suffix)
4. **Auto-timestamp**: Timestamp should reflect generation time, not stored value
5. **No user edits expected**: Guide is auto-generated; users view/print/follow, not edit

