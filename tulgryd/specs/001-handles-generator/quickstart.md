# Quickstart: Parametric Handles Generator

**Feature**: Handles Generator v1.0  
**For**: Users who want to generate custom grip handles for ToolGrid workshop organization  
**Time**: 2–5 minutes to generate your first handle

---

## What Is This?

The Handles Generator is a CLI tool that creates custom 3D printable grip handles for ToolGrid. You specify two dimensions (grip diameter and height), and the tool generates a ready-to-print STL file plus usage instructions.

**Example workflow**:
```bash
python generate.py --diameter 2.6 --height 2.0
# → Creates handle_d2.6_h2.0.stl + README
# → Ready to slice and print!
```

---

## Before You Start

✓ Python 3.8 or newer installed  
✓ CadQuery 2.4+ installed (`pip install cadquery`)  
✓ Write access to a folder for output files  
✓ 3D printer and slicing software (Cura, PrusaSlicer, etc.)

**Check your setup**:
```bash
python --version          # Should be 3.8+
python -c "import cadquery; print(cadquery.__version__)"  # Should be 2.4+
```

---

## Your First Handle (60 seconds)

### Step 1: Run the generator with default parameters

```bash
cd handles
python generate.py --diameter 2.6 --height 2.0
```

**What happens**:
- Generator validates inputs (1–10mm diameter, 0.5–5mm height)
- Builds 3D geometry in CadQuery
- Exports to STL file
- Generates assembly guide (Markdown README)
- Exits with success message

### Step 2: Check the output

```bash
ls -lh output/
```

You should see:
```
handle_d2.6_h2.0.stl        (45 KB)
handle_d2.6_h2.0_README.md  (2.5 KB)
```

### Step 3: Prepare for printing

Open `handle_d2.6_h2.0.stl` in your slicer (Cura, PrusaSlicer, etc.):
1. Load the file
2. Arrange on build plate
3. Use print settings from `handle_d2.6_h2.0_README.md`
4. Slice and send to printer

### Step 4: Print!

Print the model and follow the assembly guide (README) for attachment and usage.

---

## Common Use Cases

### Case 1: Custom grip diameter for a specific tool

Your tool shaft is 3.0mm; you want a snug grip.

```bash
python generate.py --diameter 3.0 --height 2.0
# Output: handle_d3.0_h2.0.stl + README
```

### Case 2: Multiple grips (different sizes) in one print job

```bash
# Generate two handles
python generate.py --diameter 2.6 --height 2.0
python generate.py --diameter 3.5 --height 1.5

# Output directory now has:
# - handle_d2.6_h2.0.stl
# - handle_d2.6_h2.0_README.md
# - handle_d3.5_h1.5.stl
# - handle_d3.5_h1.5_README.md

# In your slicer, load both STL files and arrange on build plate
```

### Case 3: Export to STEP format for CAD refinement

You want to modify the design further in Fusion 360 or another CAD tool.

```bash
python generate.py --diameter 2.6 --height 2.0 --format step
# Output: handle_d2.6_h2.0.step
```

### Case 4: Export both STL (printing) and STEP (refinement)

```bash
python generate.py --diameter 2.6 --height 2.0 --format both
# Output:
# - handle_d2.6_h2.0.stl
# - handle_d2.6_h2.0.step
# - handle_d2.6_h2.0_README.md
```

### Case 5: Custom output directory

Generated files are placed in `./output/` by default. Change it:

```bash
python generate.py --diameter 2.6 --height 2.0 --output-dir ~/3d_prints/handles
# Output directory: ~/3d_prints/handles/handle_d2.6_h2.0.*
```

---

## Parameter Ranges & Recommendations

### Diameter (Grip Width)

| Range | Use Case | Material | Notes |
|-------|----------|----------|-------|
| 1.0–2.0 mm | Tiny screwdrivers, precision tools | PLA | Delicate; print with care |
| 2.0–3.0 mm | M3 screws, standard tools | PLA (default) | Most common; reliable |
| 3.0–4.0 mm | M4 bolts, power tool bits | PETG | Strong; good durability |
| 4.0–5.0 mm | Large tools, frequent use | PETG/TPU | Heavy-duty applications |
| 5.0–10.0 mm | Industrial tools, extreme grip | TPU | Flexible grip for safety |

**Recommendation**: Start with 2.6mm (standard ToolGrid default).

### Height (Grip Elevation)

| Range | Use Case | Notes |
|-------|----------|-------|
| 0.5–1.0 mm | Minimal; tool sits nearly flush | Low profile; minimal reach |
| 1.0–2.0 mm | Standard height; good reach | Default is 2.0mm |
| 2.0–3.0 mm | Tall grip; extended reach | Good for small hand tools |
| 3.0–5.0 mm | Maximum height; easy access | Use for difficult-to-reach slots |

**Recommendation**: Start with 2.0mm (standard ToolGrid default).

---

## Parameter Validation

The generator validates inputs before building geometry. Here are common errors and fixes:

### Error: Diameter out of range

```
❌ ERROR: diameter must be between 1.0 and 10.0 mm (got: 15.0)
```

**Fix**: Use a value between 1.0 and 10.0 mm.

```bash
python generate.py --diameter 5.0 --height 2.0  # ✓ Valid
```

### Error: Height out of range

```
❌ ERROR: height must be between 0.5 and 5.0 mm (got: 10.0)
```

**Fix**: Use a value between 0.5 and 5.0 mm.

```bash
python generate.py --diameter 2.6 --height 3.0  # ✓ Valid
```

### Error: Non-numeric input

```
❌ ERROR: diameter must be a number (got: 'abc')
```

**Fix**: Provide numeric values (integers or decimals are OK).

```bash
python generate.py --diameter 2.6 --height 2.0     # ✓ Valid (decimals)
python generate.py --diameter 3 --height 2         # ✓ Valid (integers)
```

### Error: Missing required parameter

```
❌ ERROR: diameter required. Usage: generate.py --diameter <float> --height <float>
```

**Fix**: Provide both `--diameter` and `--height`.

```bash
python generate.py --diameter 2.6 --height 2.0  # ✓ Valid (both provided)
```

---

## File Overwrite Behavior

**Scenario**: You run the generator twice with the same parameters.

```bash
python generate.py --diameter 2.6 --height 2.0
# → Generates handle_d2.6_h2.0.stl

python generate.py --diameter 2.6 --height 2.0
# → File exists! Script asks:
#   ⚠️  File exists: ./output/handle_d2.6_h2.0.stl
#      Overwrite? [y/N]:
```

**Your options**:
- Enter `y` or `yes` → Overwrites the existing file
- Enter `n` or `no` → Aborts; file not changed
- Press Enter (empty) → Aborts (default is "no")

**Tip**: Overwrite is useful for testing new parameters; just use a different diameter/height to avoid the prompt.

---

## Understanding Output Files

### handle_d{diameter}_h{height}.stl

**What**: 3D model ready for printing  
**Format**: Binary STL (triangle mesh)  
**Size**: 40–80 KB typical  
**Usage**: Open in your slicer (Cura, PrusaSlicer, OrcaSlicer, etc.)

### handle_d{diameter}_h{height}.step (optional)

**What**: Design file for CAD refinement  
**Format**: STEP (AP214 standard)  
**Size**: 50–150 KB typical  
**Usage**: Open in Fusion 360, FreeCAD, or professional CAD software to modify further

### handle_d{diameter}_h{height}_README.md

**What**: Assembly guide + specifications  
**Format**: Markdown  
**Size**: 2–5 KB typical  
**Usage**: Read before printing; follow print settings and troubleshooting steps

---

## Print Settings (Quick Reference)

**Default: PLA**

```
Nozzle:  200°C
Bed:     60°C
Speed:   40 mm/s
Layer:   0.2 mm
Infill:  20%
Time:    45–60 min
```

**For PETG** (more durable):
```
Nozzle:  225°C
Bed:     80°C
Speed:   35 mm/s (slower)
Time:    50–70 min
```

**For TPU** (flexible):
```
Nozzle:  215°C
Bed:     60°C
Speed:   20 mm/s (much slower!)
Time:    90–120 min
```

See `handle_d{diameter}_h{height}_README.md` for full settings.

---

## Troubleshooting

### Print failed or grip too loose after printing

**Solution**: Regenerate with adjusted diameter.

```bash
# Original
python generate.py --diameter 2.6 --height 2.0

# Grip too loose? Try +0.2mm
python generate.py --diameter 2.8 --height 2.0

# Still loose? Try +0.4mm
python generate.py --diameter 3.0 --height 2.0
```

### Tool rotates too easily in grip

**Possible cause**: Printer tolerance; hole slightly larger than designed.

**Solution 1**: Re-print same file with tighter tolerances (if printer allows).

**Solution 2**: Re-generate with slightly smaller diameter.

```bash
python generate.py --diameter 2.5 --height 2.0  # 0.1mm smaller
```

### Can't open STL file in slicer

**Possible cause**: File was corrupted or incomplete.

**Solution**: Regenerate the handle.

```bash
python generate.py --diameter 2.6 --height 2.0
```

If still fails, check that CadQuery is installed and working:
```bash
python -c "import cadquery; print('CadQuery OK')"
```

---

## Next Steps

1. **Generate your first handle**: `python generate.py --diameter 2.6 --height 2.0`
2. **Read the assembly guide**: Open `handle_d2.6_h2.0_README.md`
3. **Print it**: Use the settings in the README
4. **Iterate**: Adjust diameter/height if grip fit needs tuning
5. **Explore**: Try other diameters and heights for different tools

---

## Help & Support

- **Get help**: `python generate.py --help`
- **Report bugs**: Check project GitHub issues
- **Design reference**: `handles/origin/handles.json` (parameter definitions)
- **Related project**: See `tiles/` directory for similar tile generator

Happy printing! 🎉

