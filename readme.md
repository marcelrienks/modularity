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
3. Import STL into your slicer (Cura, PrusaSlicer, etc.)
4. Slice with appropriate settings for your printer
5. Print and assemble
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

---

## Wrench Holder Generator

**File**: `wrench-holder.scad`

**Purpose**: Creates mounting blocks that attach to the pegboard grid to hold any square drive tools (wrenches, sockets, etc.). Highly flexible for different drive sizes and orientations.

### Key Features
- Supports all standard square drive sizes (1/4" through 3/4")
- Internal pin support system prevents tool rotation
- Adjustable rotation angle for compact storage or ergonomic access
- Batch printing support (multi-row mode)
- Compatible with toolgrid peg pattern

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single" | "multi_row")
- `"single"`: Generates one holder unit
- `"multi_row"`: Generates 4 holders in a row (for batch printing)

#### Grid Integration

**`hole_center_spacing`** (mm, range: 8–12)
- **Must match** the value used in toolgrid-generator.scad
- Default: 9.5mm

**`pin_hole_diameter`** (mm, range: 3–8)
- **Must match** the value used in toolgrid-generator.scad
- Used to calculate mounting peg sizing
- Default: 4.2mm

#### Housing Dimensions

**`housing_width`** (mm, range: 20–50)
- Width of the holder opening
- Should be slightly larger than the drive tool being held
- Recommended: 30mm for standard wrenches

**`housing_height`** (mm, range: 15–35)
- Height of the holder opening
- Recommended: 20mm for standard wrenches

**`housing_depth`** (mm, range: 30–60)
- Depth of protrusion from the grid
- Controls how far the tool extends outward
- Recommended: 40mm for easy access

#### Tool Specifications

**`drive_size`** (dropdown: "1/4" | "3/8" | "1/2" | "5/8" | "3/4")
- Select the square drive size of your tool
- Automatically converts to mm:
  - 1/4" = 6.35mm
  - 3/8" = 9.53mm
  - 1/2" = 12.7mm
  - 5/8" = 15.88mm
  - 3/4" = 19.05mm

**`clearance`** (mm, range: 0–1)
- Extra clearance around the drive opening
- Larger = easier insertion but looser fit
- Recommended: 0.5mm (easy fit with slight friction)

#### Pin Configuration

**`pin_diameter`** (mm, range: 3–6)
- Diameter of internal support pins (prevents tool rotation)
- Recommended: 4.0mm (compatible with standard pegs)

**`num_pins_x`** (range: 1–4)
- Number of support pins horizontally
- More pins = more support but more material

**`num_pins_y`** (range: 1–4)
- Number of support pins vertically
- Recommended: 2×2 for stable support

#### Rotation

**`holder_rotation`** (degrees, range: 0–360)
- Rotation angle of the holder relative to mounting pegs
- **Common angles**:
  - 0°: Upright (default, horizontal tool)
  - 45°: Diagonal angle
  - 90°: Horizontal (vertical tool orientation)
  - -27°: Diagonal angle matching your layout (from image analysis)
- Allows compact angled storage or ergonomic access patterns

#### Wall Thickness

**`wall_thickness`** (mm, range: 2–5)
- Thickness of housing walls
- Recommended: 3mm (adequate strength and material balance)

**`floor_thickness`** (mm, range: 1–4)
- Thickness of bottom floor of housing
- Recommended: 2mm

#### Advanced

**`pin_offset_from_edge`** (mm, range: 1–8)
- Distance from mounting surface (pegs) to first internal pin
- Recommended: 3mm (allows tool to slide over pegs initially)

**`fillet_radius`** (mm, range: 0–3)
- Radius of corner roundings for easier tool insertion
- Recommended: 1mm (reduces sharp edges)

### Usage Examples

**Standard 1/2" Wrench Holder (Upright)**
```
drive_size = "1/2"
housing_width = 30, housing_height = 20, housing_depth = 40
holder_rotation = 0
num_pins_x = 2, num_pins_y = 2
```

**Compact Angled Storage (45°)**
```
drive_size = "3/8"
housing_width = 25, housing_height = 18, housing_depth = 35
holder_rotation = 45
```

**Horizontal Orientation (90°)**
```
drive_size = "1/2"
housing_width = 30, housing_height = 20, housing_depth = 50
holder_rotation = 90
```

---

## Torque Wrench Holder Generator

**File**: `torque-wrench-holder.scad`

**Purpose**: Optimized variant of wrench-holder.scad specifically designed for torque wrenches and other cylindrical tools. Includes larger default housing dimensions to comfortably accommodate the wrench body.

### Key Features
- Optimized dimensions for torque wrench bodies (~25-30mm diameter)
- All parameters identical to wrench-holder.scad (see above)
- Pre-configured for typical torque wrench applications
- Perfect for toolbox layout integration

### Differences from wrench-holder.scad

**Larger Default Housing Dimensions**
- `housing_width`: 35mm (vs 30mm) – accommodates larger cylindrical body
- `housing_height`: 28mm (vs 20mm) – taller for tool clearance
- `housing_depth`: 50mm (vs 40mm) – deeper for secure hold and access

**All other parameters are identical** to wrench-holder.scad. Refer to wrench-holder.scad section above for complete parameter documentation.

### Typical Configuration for Toolbox Layout

```
drive_size = "1/2"
housing_width = 35
housing_height = 28
housing_depth = 50
num_pins_x = 2
num_pins_y = 2
holder_rotation = 0        // Or -27 to match diagonal layout
hole_center_spacing = 9.5
pin_hole_diameter = 4.2
```

### Usage Notes

- **Rotation Angle**: Set `holder_rotation = -27` to match the diagonal positioning from your toolbox layout image analysis
- **Pin Support**: The 2×2 pin grid provides stable support for the torque wrench without excessive material
- **Clearance**: Default 0.5mm clearance is appropriate for most 1/2" torque wrenches

---

## Tool End Holder Generator

**File**: `tool-end-holder-generator.scad`

**Purpose**: Creates holders for tool ends, bits, and small implements. Flexible design for various end tool sizes and configurations.

### Key Features
- Holds various tool ends and bits
- Central cavity design for organized storage
- Support pin grid for stability
- Rotation support for angled placement
- Batch printing capability

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single" | "multi_row")
- `"single"`: Generates one holder unit
- `"multi_row"`: Generates 4 holders in a row

#### Grid Integration

**`hole_center_spacing`** (mm, range: 8–12)
- Must match toolgrid-generator.scad
- Default: 9.5mm

**`pin_hole_diameter`** (mm, range: 3–8)
- Must match toolgrid-generator.scad
- Default: 4.2mm

#### Housing Dimensions

**`housing_width`** (mm, range: 20–50)
- Width of holder opening
- Default: 30mm

**`housing_height`** (mm, range: 15–40)
- Height of holder opening
- Default: 25mm

**`housing_depth`** (mm, range: 25–60)
- Depth/protrusion from grid
- Default: 35mm

#### Pin Configuration

**`pin_diameter`** (mm, range: 3–6)
- Support pin diameter
- Default: 4.0mm

**`num_pins_x`** (range: 1–4)
- Horizontal pin count
- Default: 2

**`num_pins_y`** (range: 1–4)
- Vertical pin count
- Default: 2

#### Rotation

**`holder_rotation`** (degrees, range: 0–360)
- Rotation angle relative to mounting pegs
- Default: 0°

#### Wall Thickness

**`wall_thickness`** (mm, range: 2–5)
- Housing wall thickness
- Default: 3mm

**`floor_thickness`** (mm, range: 1–4)
- Floor thickness
- Default: 2mm

#### Advanced

**`pin_offset_from_edge`** (mm, range: 1–8)
- Distance from mounting surface to pin
- Default: 3mm

**`fillet_radius`** (mm, range: 0–3)
- Corner radius
- Default: 1mm

---

## Wrench Holder Generator

**File**: `wrench-holder-generator.scad`

**Purpose**: Flexible holder for wrenches in various sizes (small/large). Easily customizable for different wrench dimensions.

### Key Features
- Size selector for different wrench types
- Fine-tune width offset for custom sizing
- Central cavity design
- Support pin grid
- Rotation support

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single" | "multi_row")
- `"single"`: Generates one holder unit
- `"multi_row"`: Generates 4 holders in a row

#### Grid Integration

**`hole_center_spacing`** (mm, range: 8–12)
- Must match toolgrid-generator.scad
- Default: 9.5mm

**`pin_hole_diameter`** (mm, range: 3–8)
- Must match toolgrid-generator.scad
- Default: 4.2mm

#### Wrench Size

**`wrench_size`** (dropdown: "small" | "large")
- Select wrench category
- Default: "large"

**`width_offset`** (mm, range: -5 to +5)
- Fine-tune width beyond standard
- Default: 0mm

#### Housing Dimensions

**`housing_width`** (mm, range: 25–55)
- Width of holder opening
- Default: 40mm

**`housing_height`** (mm, range: 20–45)
- Height of holder opening
- Default: 30mm

**`housing_depth`** (mm, range: 30–70)
- Depth/protrusion from grid
- Default: 45mm

#### Pin Configuration

**`pin_diameter`** (mm, range: 3–6)
- Support pin diameter
- Default: 4.0mm

**`num_pins_x`** (range: 1–4)
- Horizontal pin count
- Default: 2

**`num_pins_y`** (range: 1–4)
- Vertical pin count
- Default: 2

#### Rotation

**`holder_rotation`** (degrees, range: 0–360)
- Rotation angle relative to mounting pegs
- Default: 0°

#### Wall Thickness

**`wall_thickness`** (mm, range: 2–5)
- Housing wall thickness
- Default: 3mm

**`floor_thickness`** (mm, range: 1–4)
- Floor thickness
- Default: 2mm

#### Advanced

**`pin_offset_from_edge`** (mm, range: 1–8)
- Distance from mounting surface to pin
- Default: 3mm

**`fillet_radius`** (mm, range: 0–3)
- Corner radius
- Default: 1mm

---

## Ratchet Holder Generator

**File**: `ratchet-holder-generator.scad`

**Purpose**: Specialized holders for ratchets in various drive sizes (1/4", 3/8"). Optimized cavity design for ratchet head accommodation.

### Key Features
- Drive size selector (1/4", 3/8")
- Optimized central cavity for ratchet heads
- Support pin grid for stability
- Rotation support
- Customizable dimensions

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single" | "multi_row")
- `"single"`: Generates one holder unit
- `"multi_row"`: Generates 4 holders in a row

#### Grid Integration

**`hole_center_spacing`** (mm, range: 8–12)
- Must match toolgrid-generator.scad
- Default: 9.5mm

**`pin_hole_diameter`** (mm, range: 3–8)
- Must match toolgrid-generator.scad
- Default: 4.2mm

#### Drive Size

**`drive_size`** (dropdown: "1-4" | "3-8")
- Select ratchet drive size
- Default: "1-4"

#### Housing Dimensions

**`housing_width`** (mm, range: 25–50)
- Width of holder opening
- Default: 35mm

**`housing_height`** (mm, range: 18–40)
- Height of holder opening
- Default: 28mm

**`housing_depth`** (mm, range: 30–70)
- Depth/protrusion from grid
- Default: 45mm

#### Pin Configuration

**`pin_diameter`** (mm, range: 3–6)
- Support pin diameter
- Default: 4.0mm

**`num_pins_x`** (range: 1–4)
- Horizontal pin count
- Default: 2

**`num_pins_y`** (range: 1–4)
- Vertical pin count
- Default: 2

#### Rotation

**`holder_rotation`** (degrees, range: 0–360)
- Rotation angle relative to mounting pegs
- Default: 0°

#### Wall Thickness

**`wall_thickness`** (mm, range: 2–5)
- Housing wall thickness
- Default: 3mm

**`floor_thickness`** (mm, range: 1–4)
- Floor thickness
- Default: 2mm

#### Advanced

**`pin_offset_from_edge`** (mm, range: 1–8)
- Distance from mounting surface to pin
- Default: 3mm

**`fillet_radius`** (mm, range: 0–3)
- Corner radius
- Default: 1mm

---

## Socket Tree Generator

**File**: `socket-tree-generator.scad`

**Purpose**: Creates organized socket storage trees for holding sockets in grid patterns. Configurable socket holes for different socket sets.

### Key Features
- Drive size selector (1/2", 1/4", 3/8")
- Configurable socket hole grid (rows × columns)
- Adjustable socket hole diameter
- Support pin grid
- Rotation support
- Batch printing capability

### Parameters

#### Display Mode

**`print_mode`** (dropdown: "single" | "multi_row")
- `"single"`: Generates one tree unit
- `"multi_row"`: Generates 3 trees in a row

#### Grid Integration

**`hole_center_spacing`** (mm, range: 8–12)
- Must match toolgrid-generator.scad
- Default: 9.5mm

**`pin_hole_diameter`** (mm, range: 3–8)
- Must match toolgrid-generator.scad
- Default: 4.2mm

#### Drive Size

**`drive_size`** (dropdown: "1-2" | "1-4" | "3-8")
- Select socket drive size
- Default: "1-2"

#### Tree Dimensions

**`tree_width`** (mm, range: 30–60)
- Width of socket tree
- Default: 45mm

**`tree_height`** (mm, range: 40–80)
- Height of socket tree
- Default: 60mm

**`tree_depth`** (mm, range: 10–30)
- Depth/thickness of tree
- Default: 15mm

#### Socket Configuration

**`socket_diameter`** (mm, range: 5–15)
- Diameter of socket holes
- Default: 8mm

**`num_socket_rows`** (range: 1–5)
- Number of socket hole rows
- Default: 3

**`sockets_per_row`** (range: 2–8)
- Number of sockets per row
- Default: 4

#### Pin Configuration

**`pin_diameter`** (mm, range: 3–6)
- Support pin diameter
- Default: 4.0mm

**`num_pins_x`** (range: 1–4)
- Horizontal pin count
- Default: 2

**`num_pins_y`** (range: 1–4)
- Vertical pin count
- Default: 2

#### Rotation

**`holder_rotation`** (degrees, range: 0–360)
- Rotation angle relative to mounting pegs
- Default: 0°

#### Wall Thickness

**`wall_thickness`** (mm, range: 2–5)
- Housing wall thickness
- Default: 3mm

**`floor_thickness`** (mm, range: 1–4)
- Floor thickness
- Default: 2mm

#### Advanced

**`pin_offset_from_edge`** (mm, range: 1–8)
- Distance from mounting surface to pin
- Default: 3mm

---

## Parameter Compatibility

When creating multiple holders and tiles for the same project, ensure these parameters match across **all scripts**:

| Parameter | Location | Purpose |
|-----------|----------|---------|
| `hole_center_spacing` | All scripts | Must be identical for grid alignment |
| `pin_hole_diameter` | All scripts | Must be identical for peg compatibility |
| `drive_size` | Holder scripts | Must match the tool specification |

**Common Configuration**
```
All scripts:
  hole_center_spacing = 9.5
  pin_hole_diameter = 4.2
```

---

## Design Tips & Troubleshooting

### Grid Spacing Mismatch
- If holders don't align with grid holes, verify `hole_center_spacing` and `pin_hole_diameter` match between scripts
- Changing spacing by 0.5mm affects full tile width by 8mm (for 16-column tile)

### Interlocking Tab Issues
- Use **alternating male/female** pattern: if tile A has male on the right, tile B should have female on the left
- If assembly is too tight, increase `male_tab_clearance` to 0.2–0.3mm
- If tabs are too loose, decrease to 0.05mm

### Lightweight Mode Weak Points
- If webs are too sparse, decrease `lightweight_web_spacing` to 4–5
- If model is too heavy, increase spacing to 10–12
- Ensure `lightweight_thickness` is at least 2.5mm for layer adhesion

### Tool Rotation & Access
- Test angles before committing to full print (preview different `holder_rotation` values)
- -27° diagonal is optimal for drawer space efficiency
- 45° works well for wall displays
- 90° horizontal for vertical storage

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
