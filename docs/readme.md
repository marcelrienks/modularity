# Modularity – Modular Pegboard Grid & Tool Holder System

A collection of parametric OpenSCAD scripts for generating customizable modular tool storage solutions. Create interlocking pegboard grids that perfectly fit any drawer, plus specialized holders for wrenches, sockets, torque wrenches, and other square drive tools.

## Overview

**Modularity** is a complete tool organization system designed around a flexible modular grid pattern. The system consists of:

- **Pegboard Grid Tiles**: Interlocking tiles with customizable hole patterns, adjustable thickness, and optional lightweight web structures
- **Tool Holders**: Mounting blocks that attach to the grid to hold wrenches, sockets, and other tools at any angle
- **Flexible Sizing**: Automatically calculates and generates all tiles needed to fill a drawer of any size
- **Parametric Design**: Every dimension and feature is adjustable via OpenSCAD's Customizer interface

The modular approach lets you design once and print multiple pieces that lock together without fasteners, creating a perfectly organized storage solution tailored to your tools and drawer dimensions.

## Requirements

### Software
- **OpenSCAD** (free, open-source): https://openscad.org/
  - Version 2021.01 or later recommended
  - Includes built-in Customizer for easy parameter adjustment

### Hardware
- **3D Printer**: FDM printer capable of printing ~50×50mm or larger pieces
  - Layer height: 0.2mm or finer (0.1mm recommended for hole precision)
  - Nozzle: Standard 0.4mm
  - Material: PLA, PETG, or ABS (PLA recommended for ease)

### Optional
- **3D Slicer Software**: Cura, PrusaSlicer, SuperSlicer (to prepare STL files for printing)
- **Actual Pegboard Pegs/Hooks**: Standard 1/4" diameter (6mm) pegs compatible with most commercial pegboard systems

## Quick Start

### 1. Design Your Grid Layout

**For a drawer:**
```
1. Open toolgrid-generator.scad in OpenSCAD
2. Go to View → Customizer
3. Set print_mode = "drawer_grid"
4. Measure your drawer interior dimensions and enter:
   - drawer_width = [your width in mm]
   - drawer_length = [your length in mm]
5. Keep other defaults or customize as needed
6. Press spacebar to preview (color-coded tiles show layout)
```

**For a single test tile:**
```
1. Open toolgrid-generator.scad in OpenSCAD
2. Set print_mode = "single_tile"
3. Adjust tile_columns and tile_rows (e.g., 8×8 for a small test)
4. Press spacebar to preview
```

### 2. Export & Print

```
1. Verify the preview looks correct
2. File → Export as STL
3. Save to the models/ directory in this project (recommended location)
   - Example: models/toolgrid_tile_full.stl
4. Import STL into your slicer (Cura, PrusaSlicer, etc.)
5. Slice with appropriate settings for your printer
6. Print and assemble
```

### 3. Add Tool Holders (Optional)

```
1. Open wrench-holder.scad or torque-wrench-holder.scad
2. Set parameters to match your grid (hole_center_spacing, pin_hole_diameter)
3. Choose your drive_size and rotation angle
4. Export as STL and print
5. Mount onto grid by inserting pegs into pegboard holes
```

### 4. Assembly

- Tiles interlock via male/female tab system (no glue or fasteners needed)
- Arrange tiles to fit your drawer based on color-coded layout
- Insert tool holders onto pegboard holes at desired positions
- Arrange tools and adjust holder angles as needed

---

# Generators

## ToolGrid Generator

**File**: `toolgrid-generator.scad`

**Purpose**: Generates the foundation of your storage system. Creates interlocking pegboard tiles with adjustable hole patterns, material options, and customizable grid arrangements.

### Key Features
- Generate single tiles or complete drawer-filling tile sets
- Interlocking male/female tab system (no fasteners required)
- Lightweight mode reduces material by 40-50% while maintaining strength
- Automatic edge tile calculation for perfect drawer fit
- Optional connector pieces for extending grids

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single_tile" | "drawer_grid")
- `"single_tile"`: Creates one tile with fixed hole grid (good for prototyping)
- `"drawer_grid"`: Calculates and generates all tiles needed to fill drawer dimensions

**`generate_part`** (dropdown: "tiles" | "connector_only")
- `"tiles"`: Outputs all pegboard tiles (standard mode)
- `"connector_only"`: Outputs only connector pieces for joining female slots

#### Drawer Dimensions
*(Only used in "drawer_grid" mode)*

**`drawer_width`** (mm, range: 100–600)
- Interior width of your drawer (X direction)
- Script calculates how many full tiles fit and creates appropriately-sized edge pieces

**`drawer_length`** (mm, range: 100–600)
- Interior length of your drawer (Y direction)

#### Tile Grid Configuration

**`tile_columns`** (range: 4–16)
- Number of hole columns per tile
- Larger values = wider tiles, fewer pieces needed

**`tile_rows`** (range: 4–16)
- Number of hole rows per tile
- Larger values = taller tiles

#### Hole Settings

**`pin_hole_diameter`** (mm, range: 3–8)
- Diameter of peg holes
- **Common values**:
  - 4.2mm: Standard metric, tight fit
  - 5.0mm: Compromise between metrics and imperial
  - 6.0mm: 1/4" pegboard standard, loose fit (most flexible)
- **Important**: This must match your actual pegs and match across all holder scripts

**`hole_center_spacing`** (mm, range: 8–12)
- Distance between hole centers (horizontal and vertical)
- Directly affects final tile size
- **Common values**:
  - 8.0mm: Very tight (European standard)
  - 9.5mm: Balanced default (recommended)
  - 10.0mm: 1/4" spacing (standard pegboard compatible)
- **Important**: Must match across all scripts for compatibility

#### Material & Weight Reduction

**`use_lightweight`** (true | false)
- `true`: Replaces solid board with circular web pattern (~40-50% material savings)
- `false`: Solid board (standard pegboard style)
- Recommended: `true` for filament efficiency

**`base_thickness`** (mm, range: 6–12)
- Overall board thickness (Z height)
- Minimum: 6mm (smaller risks hole collapse)
- Recommended: 8mm (good balance of strength and weight)

**`lightweight_thickness`** (mm, range: 2–8)
- *(Only used if `use_lightweight = true`)*
- Thickness of the support webs around holes
- Recommended: 3–4mm (adequate strength with minimal material)

**`lightweight_web_spacing`** (range: 4–16)
- *(Only used if `use_lightweight = true`)*
- Number of hole spaces between support webs
- Lower = denser support (stronger but heavier)
- Higher = sparser support (lighter but potentially fragile)
- Recommended: 6–8 (good balance)

#### Interlocking Tabs

**`tab_front`** / **`tab_back`** / **`tab_left`** / **`tab_right`** (dropdown: "male" | "female" | "none")
- **"male"**: Raised cylindrical pegs protrude from this edge (lock into female slots)
- **"female"**: Recessed cylindrical slots cut into this edge (receive male pegs)
- **"none"**: Flat edge with no tabs or slots
- **Tip**: Use alternating male/female pattern for adjacent tiles to interlock properly

**`tab_hole_diameter`** (mm, range: 2–6)
- Diameter of male tabs and female slots
- Recommended: 4mm (standard 3D printer tolerance)
- Larger values = stronger locking but harder to assemble
- Smaller values = easier assembly but weaker locking

**`tab_offset`** (mm, range: 0.5–3)
- Distance from tile edge to center of tabs
- Default: 1.52mm (prevents tabs from sticking out past edge)
- **Leave at default** unless you have specific fitting needs

**`male_tab_clearance`** (mm, range: 0–0.5)
- Tolerance gap added to male tab diameter
- Larger = looser fit (easier assembly)
- Smaller = tighter fit (more secure locking)
- Recommended: 0.1mm (standard clearance for most printers; adjust after first test print)

#### Single Tile Only
*(Only used in "single_tile" mode)*

**`trim_width`** (mm, range: -3 to +8)
- Add or subtract width from tile beyond the standard grid calculation
- Positive values = wider tile
- Negative values = narrower tile

**`trim_length`** (mm, range: -3 to +8)
- Add or subtract length from tile

**`custom_label`** (text)
- Optional embossed text label on tile (for identification in multi-tile projects)

#### Advanced Parameters

**`edge_tile_min_width`** (mm, range: 5–25)
- Minimum acceptable width for partial edge tiles in drawer mode
- If calculated edge tile is smaller than this value, it's not generated
- Recommended: 12mm (avoids tiny, fragile pieces)

### Usage Examples

**Standard 1/4" Pegboard-Compatible Setup**
```
pin_hole_diameter = 6.0
hole_center_spacing = 10.0
tile_columns = 12, tile_rows = 12
base_thickness = 8
use_lightweight = false
```

**Lightweight Drawer Fill**
```
print_mode = "drawer_grid"
drawer_width = 400, drawer_length = 500
use_lightweight = true
lightweight_thickness = 3
lightweight_web_spacing = 8
base_thickness = 6
```

**Wall-Mounted Display (Interlocking)**
```
print_mode = "single_tile"
tile_columns = 10, tile_rows = 10
tab_front = "male", tab_back = "female"
tab_left = "male", tab_right = "female"
base_thickness = 6
```

## STL Tool - Model Analysis & Validation

A comprehensive unified Python tool for analyzing and validating 3D models. Essential for debugging SCAD scripts and ensuring generated models match design specifications.

**File**: `stl_tool.py`

**Documentation**: See [stl_tool.md](stl_tool.md) for complete guide with quick start, full feature reference, and usage examples.

### Quick Usage

```bash
# Analyze a single model
python3 stl_tool.py model.stl

# Compare generated model with reference
python3 stl_tool.py --compare generated.stl reference.stl

# Batch analyze multiple files
python3 stl_tool.py examples/*.stl

# View only dimensions
python3 stl_tool.py --dimensions model.stl
```

### What It Does

- **Parses** ASCII and binary STL files automatically
- **Analyzes** dimensional metrics (width, height, depth, center point)
- **Detects** geometric features (mounting pegs, curved surfaces, cavities)
- **Measures** complexity (Z-level distribution for geometry detail)
- **Estimates** material properties (volume, surface area, weight)
- **Compares** models to validate SCAD generator output
- **Batch processes** multiple files with summary tables

### Key Features

✓ Mounting peg detection (for pegboard compatibility)
✓ Curved surface detection (cylindrical/rounded geometry)
✓ Interior cavity detection and counting
✓ Symmetry analysis (X/Y axis balance)
✓ Wall thickness estimation
✓ Material weight estimation (adjustable for different filaments)
✓ Comprehensive comparison mode
✓ Multiple output modes (full, dimensions-only, geometry-only, features-only)
✓ Zero external dependencies (Python 3.6+ only)

### SCAD Debugging Workflow

```bash
# 1. Generate test model
openscad -o /tmp/test.stl -D 'param="value"' generator.scad

# 2. Compare with reference
python3 stl_tool.py --compare /tmp/test.stl examples/reference.stl

# 3. Check results
# If ✓ MODELS MATCH → Done! Export to models/
# If ✗ MODELS DIFFER → Fix SCAD, regenerate, repeat
```

**For complete documentation**: See [stl_tool.md](stl_tool.md)

---

## 🙏 Attribution

**Original ToolGrid Creator**: [Akmjoe](https://www.printables.com/@Akmjoe_246598)

This project is derived from the original **Toolgrid Board Generator** published on Printables:
- **Printables Model**: https://www.printables.com/model/1455970-toolgrid-board-generator/files
- **Creator Profile**: https://www.printables.com/@Akmjoe_246598

**Tool Holder Model Examples**: [MaxTheSpy](https://thangs.com/designer/MaxTheSpy)

The tool holder generator scripts (wrench holders, ratchet holders, socket trees, and tool end holders) were built as parametric generators based on design examples and models by MaxTheSpy:
- **Thangs Profile**: https://thangs.com/designer/MaxTheSpy
- **Reference**: Used as design foundation for customizable generator scripts

**This Version** (Modularity, December 2024) includes:
- Comprehensive documentation and parameter guides
- Parametric generator scripts for all tool holder types
- Rotation parameter for angled tool placement
- Multiple drive size and configuration support
- Enhanced usability and customization examples
- Complete ToolGrid tile system with lightweight mode support

**Repository**: https://github.com/marcelrienks/modularity
