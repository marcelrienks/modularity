# tulgryd Generator

Parametric 3D model generator for modular tool grid tiles with interlocking edges.

## Features

- ✅ **Assembly Generation**: Input total dimensions, get optimized tile layout
- ✅ **Smart Layout**: Automatically calculates 100×100mm standard tiles + custom edge pieces
- ✅ **Quantity-Coded Filenames**: `tile_100x100_qty4.stl` = make 4 copies
- ✅ **Auto-Generated Assembly Guide**: Complete instructions with layout diagram
- ✅ **Multiple Formats**: Export to STL, STEP
- ✅ **Fully Parametric**: Customize all dimensions via JSON

## Quick Start

### Usage Examples

**Generate tiles for a 250×180mm drawer:**
```bash
python generate.py --total-width 250 --total-length 180
```

**Generate single 100×100mm standard tile:**
```bash
python generate.py --single-tile
```

**Generate with adjusted hole diameter (compensate for printer tolerance):**
```bash
# Adjustment affects total hole diameter (not radius)
python generate.py --single-tile --hole-adjust 0.2   # Ø4.2mm holes (0.2mm larger)
python generate.py --single-tile --hole-adjust -0.1  # Ø3.9mm holes (0.1mm smaller)
```

**Generate custom single tile:**
```bash
python generate.py --single-tile --tile-width 100 --tile-length 45
```

**Specify output format:**
```bash
python generate.py --total-width 250 --total-length 180 --format step
```

## Project Structure

- `core/` - Core modules for layout calculation, model building, and assembly guide generation
- `origin/` - Original model files that this script was built upon
- `tests/` - Test suite for the generator

## Output Structure

```
output/2026-01-13_091700_250x180mm/
├── tile_100x100_qty4.stl          # Standard tiles (make 4)
├── tile_50x100_qty2.stl           # Right edge (make 2)
├── tile_100x80_qty2.stl           # Top edge (make 2)
├── tile_50x80_qty1.stl            # Corner (make 1)
├── layout_diagram.txt             # Visual layout
└── ASSEMBLY_README.md             # Complete instructions
```

## Assembly Guide

Each generation creates a comprehensive `ASSEMBLY_README.md` with:

- ✅ File manifest with quantities
- ✅ Layout diagram
- ✅ Step-by-step assembly instructions
- ✅ Interlocking system explanation
- ✅ Troubleshooting tips

## Tile Specifications

**Standard 100×100mm Tile:**
- Grid: 10×10 holes (100 mounting points)
- Hole diameter: 4mm (M3 compatible)
- Hole adjustment: Use `--hole-adjust` to compensate for printer tolerance
  - Adjusts total hole **diameter** (not radius)
  - Example: `--hole-adjust 0.2` → Ø4.2mm holes (0.2mm larger diameter)
  - Example: `--hole-adjust -0.1` → Ø3.9mm holes (0.1mm smaller diameter)
- Thickness: 6mm
- Tabs: Ø3.8mm on top/right edges
- Slots: Ø4.0mm on bottom/left edges

**Custom Edge Tiles:**
- Variable dimensions (<100mm)
- Partial grid maintaining 10mm spacing
- Compatible interlocking features

## Requirements

- Python 3.8+
- CadQuery 2.4+
- NumPy
- Click (CLI framework)
- Jinja2 (templating engine)
- pytest (testing framework)

## Command Line Options

```
Options:
  --total-width FLOAT         Total width in mm
  --total-length FLOAT        Total length in mm
  --single-tile               Generate single tile instead of assembly
  --tile-width FLOAT          Tile width for single tile mode (default: 100)
  --tile-length FLOAT         Tile length for single tile mode (default: 100)
  --output-dir PATH           Output directory (default: ./output)
  --format [stl|step|both]    Output format (default: stl)
  --config PATH               JSON config file
  --preset TEXT               Use preset configuration
  --help                      Show this message and exit
```

## Python API

```python
from core import LayoutCalculator, ModelBuilder, Parameters, AssemblyGuideGenerator

# Calculate layout
calculator = LayoutCalculator(total_width=250, total_length=180)
print(calculator.generate_layout_diagram())

# Generate tile
params = Parameters()
params.set_dimensions(width=100, length=100)
builder = ModelBuilder(params)
builder.build()
builder.export_stl('tile.stl')

# Generate assembly guide
guide = AssemblyGuideGenerator(calculator)
guide.generate_readme(output_dir='./output')
```

## Customization

Edit `../parameters.json` to customize:
- Grid spacing
- Hole diameter
- Cylinder diameter
- Tab/slot dimensions
- Wall thickness

## License

MIT License - See repository root for details

## Version

1.0.0 - Initial release
