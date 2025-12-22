# OpenSCAD Toolgrid Generator V2

A parametric OpenSCAD script for generating customizable toolbox organization grids with interlocking tiles. Create single tiles or complete drawer grids.

## 📋 Overview

Generate modular pegboard-style organizing grids for tool storage. Tiles interlock using male/female tab systems for flexible, scalable configurations.

### Key Features
- **Single Tile**: Generate individual tiles (4×4 to 16×16 holes)
- **Drawer Mode**: Automatically create tile sets that perfectly fit a drawer
- **Interlocking Tabs**: Male/female locking tabs keep tiles aligned
- **Lightweight Option**: Cross-brace design reduces material usage
- **Customizable**: Adjust hole size, spacing, thickness, and more
- **Connector Pieces**: Optional connectors for joining tiles without gluing

---

## 🎯 Current Functionality

**Single Tile Generation** - Create individual tiles with custom dimensions. Control hole count (4-16), diameter, spacing, board thickness, and add optional lightweight cross-braces.

**Drawer Grid Mode** - Input drawer dimensions and automatically generate all tiles needed to fill it perfectly. The script calculates full tiles and creates appropriately-sized edge pieces for complete coverage.

**Interlocking Tabs** - Tiles connect without fasteners. Each side (front, back, left, right) can be configured independently as male tab (raised), female slot (recessed), or none. Clearance is adjustable for fit tolerance.

**Lightweight Mode** - Optional cross-brace pattern reduces material by ~40-50% while maintaining strength. Customize web thickness and spacing between support structures.

**Connector Piece** - Generate connector pieces to join two female-slot faces together for extended grids.

---

## 🎮 How to Use

1. **Open in OpenSCAD** (free download: https://openscad.org/)
   ```bash
   open toolgrid-generator-v2.scad
   ```

2. **Customize Parameters** (View → Customizer)
   - `print_mode`: "drawer_grid" for drawer, "single_tile" for single tile
   - `tile_columns` / `tile_rows`: 4-16 holes per tile
   - `pin_hole_diameter`: Size of tool peg holes
   - `hole_center_spacing`: Distance between hole centers
   - `base_thickness`: Board thickness in mm (6mm minimum)
   - `use_lightweight`: Enable lightweight cross-braces (true/false)
   - Tab configuration: Set tab_front, tab_back, tab_left, tab_right to male/female/none

3. **Preview** (Press spacebar or View → Preview)
   - Single tile mode: Shows one tile
   - Drawer mode: Color-coded layout showing full and edge tiles

4. **Export as STL** (File → Export as STL)
   - Choose filename and location
   - Import into your 3D slicer software

---

## ⚙️ Parameters

### Display Mode

#### `print_mode` (dropdown: "single_tile" / "drawer_grid")
**What it does:** Switches between two fundamental generation modes.
- **"single_tile"**: Creates one tile with fixed hole grid (tile_columns × tile_rows holes)
- **"drawer_grid"**: Automatically calculates and generates all tiles needed to fill a drawer of specified dimensions
- **Effect on model**: Changes entire layout and quantity of generated parts. Single tile is optimal for prototyping; drawer mode handles full projects

**When to use:**
- Single tile: Testing designs, wall displays, specific sizes
- Drawer grid: Filling existing storage drawers, organized multi-tile projects

---

#### `generate_part` (dropdown: "tiles" / "connector_only")
**What it does:** Chooses what component(s) to generate.
- **"tiles"**: Outputs all pegboard tiles (default)
- **"connector_only"**: Outputs only connector pieces that join two female-slot faces
- **Effect on model**: In "tiles" mode, generates full tile layout. In "connector_only", produces just the small joiner pieces (used to connect female slots without gluing)

**When to use:**
- Tiles: Your main output when designing the grid layout
- Connector only: After printing tiles, print connectors for weak connections

---

### Drawer Dimensions

#### `drawer_width` (mm, range: 100–600)
**What it does:** Specifies the interior width of your drawer (distance in X direction).
- **Effect on model**: Determines how many full tiles fit width-wise. Remaining space gets edge tiles (narrower)
- **Example**: 300mm width with 16-column tiles (152.4mm per tile) = 1 full tile + 1 edge tile
- **Increase**: More tiles in width, more coverage; scale up project
- **Decrease**: Fewer tiles, more compact; reduces filament

**Impact on calculations:**
```
Full tiles in width = floor(drawer_width / (tile_columns × hole_spacing))
Edge tile width = drawer_width % (tile_columns × hole_spacing)
```

---

#### `drawer_length` (mm, range: 100–600)
**What it does:** Specifies the interior length of your drawer (distance in Y direction).
- **Effect on model**: Determines how many full tiles fit length-wise. Remaining space gets edge tiles (shorter)
- **Example**: 400mm length with 16-row tiles (152.4mm per tile) = 2 full tiles + 1 edge tile
- **Increase**: More rows of tiles, larger projects
- **Decrease**: Fewer tiles, more compact layouts

**Note**: Only used in "drawer_grid" mode; ignored in "single_tile" mode.

---

### Tile Grid Configuration

#### `tile_columns` (integer, range: 4–16)
**What it does:** Number of hole columns in each tile (horizontal hole count).
- **Effect on model**: Determines tile width: `tile_width = tile_columns × hole_center_spacing`
- **Increase (e.g., 12→16)**: Wider tiles, fewer tiles needed to fill space, fewer interlocking edges
- **Decrease (e.g., 16→8)**: Narrower tiles, more flexibility in placement, more edges to manage
- **Example**: 16 columns + 9.5mm spacing = 152mm tile width (standard size)

**Impact**: Directly affects physical tile dimensions and required storage space.

---

#### `tile_rows` (integer, range: 4–16)
**What it does:** Number of hole rows in each tile (vertical hole count).
- **Effect on model**: Determines tile height: `tile_height = tile_rows × hole_center_spacing`
- **Increase (e.g., 12→16)**: Taller tiles, better for vertical storage
- **Decrease (e.g., 16→8)**: Shorter tiles, easier to print, lighter pieces
- **Example**: 16 rows + 9.5mm spacing = 152mm tile height

**Impact**: Affects print time, material usage, and comfort of accessing tools.

---

### Hole Settings

#### `pin_hole_diameter` (mm, range: 3–8)
**What it does:** Diameter of the peg holes in the pegboard.
- **Effect on model**: Directly sizes all peg holes throughout the grid
- **Increase (e.g., 4.2→6.0)**: Larger holes, fits 1/4" (6.35mm) standard pegs, less precision-dependent, easier to insert pegs
- **Decrease (e.g., 4.2→3.5)**: Tighter fit, holds smaller pegs, may require more careful printing/insertion
- **Common standards**:
  - 4.2mm: Standard metric, tight fit
  - 6.0mm: 1/4" pegboard standard, loose fit for easy adjustment
  - 5.0mm: Compromise between tightness and standard compatibility

**Impact**: Determines tool peg compatibility; smaller holes = tighter fit, larger holes = more room for adjustment.

---

#### `hole_center_spacing` (mm, range: 8–12)
**What it does:** Distance between hole centers (both horizontally and vertically).
- **Effect on model**: Scales entire grid spacing; directly affects tile dimensions
- **Formula**: `tile_width = tile_columns × hole_center_spacing`
- **Increase (e.g., 9.5→10.0)**: Larger grid spacing, bigger tiles, tools spaced farther apart
- **Decrease (e.g., 9.5→9.0)**: Tighter grid, more tools per tile, more compact design
- **Standard spacing**:
  - 8.0mm: Very tight, European standard
  - 9.5mm: Balanced default (recommended)
  - 10.0mm: 1/4" spacing, compatible with standard pegs

**Impact**: Critical for overall tile size and tool density. Changing by 0.5mm affects final tile dimensions by 8mm (16 columns).

---

### Material & Weight Reduction

#### `use_lightweight` (checkbox: true/false)
**What it does:** Enables/disables lightweight cross-brace structure.
- **true**: Replaces solid board with circular web pattern around holes, reducing material ~40-50%
- **false**: Solid board throughout (standard pegboard)
- **Effect on model**: Dramatic change in appearance and material usage
- **When true**: Print time reduced, filament reduced, but maintains strength around holes
- **When false**: Heavier pieces, more filament, simpler printing

**Trade-off**: Lightweight mode saves filament but creates web pattern visible on surfaces.

---

#### `base_thickness` (mm, range: 6–12)
**What it does:** Thickness of the pegboard material (Z-height).
- **Effect on model**: Affects hole depth and overall board sturdiness
- **Increase (e.g., 6→10)**: Thicker, stronger boards, holds pegs more securely, heavier
- **Decrease (e.g., 10→6)**: Thinner, lighter, less material, may be fragile
- **Minimum**: 6mm (hard limit—smaller may collapse holes)
- **Recommended**: 8mm (good balance of strength and weight)

**Impact on pegs**: Thicker boards grip pegs better; thinner boards may let pegs shift.

---

#### `lightweight_thickness` (mm, range: 2–8) - Only affects lightweight mode
**What it does:** Thickness of the support web in lightweight mode.
- **Effect on model**: Controls how thick the circular reinforcements are around holes
- **Increase (e.g., 3→5)**: Stronger webs, more material, stronger board
- **Decrease (e.g., 4→2)**: Thinner webs, minimum material, potential weak points
- **Recommended**: 3–4mm (balances strength and material savings)

**Note**: Ignored if `use_lightweight = false`

**Impact**: Determines structural integrity of web supports; too thin may cause layer adhesion issues.

---

#### `lightweight_web_spacing` (integer, range: 4–16) - Only affects lightweight mode
**What it does:** Number of hole spaces between support web patterns.
- **Effect on model**: Controls density/frequency of support webs
- **Increase (e.g., 6→12)**: More space between webs, fewer supports, lighter, less coverage
- **Decrease (e.g., 10→4)**: More frequent webs, denser support, heavier, stronger
- **Example**: Value of 6 = web every 6 holes (creates regular grid of webs)
- **Recommended**: 6–8 (good balance of support and weight reduction)

**Impact**: More webs = stronger but heavier; fewer webs = lighter but potentially fragile.

---

### Interlocking Tabs

#### `tab_front` / `tab_back` / `tab_left` / `tab_right` (dropdown: "male" / "female" / "none")
**What it does:** Configures which edge of the tile has interlocking tabs.
- **"male"**: Raised cylindrical pegs protrude from this edge (lock into female slots on adjacent tiles)
- **"female"**: Recessed cylindrical slots cut into this edge (receive male pegs from adjacent tiles)
- **"none"**: Flat edge, no tabs or slots
- **Effect on model**: Creates 3D interlocking geometry on specified edges
- **Usage pattern**: Tiles mesh together like puzzle pieces
  - Front tile has male → back tile has female (front-to-back connection)
  - Left tile has male → right tile has female (left-to-right connection)

**Example configuration for 2×2 grid:**
```
Back row: tab_back = "none" (external edge)
Front row: tab_front = "female" (joins with back row)
Left column: tab_left = "none" (external edge)
Right column: tab_right = "female" (joins with left column)
Internal connections use male/female alternation
```

**Impact**: Determines how tiles physically lock together; wrong config results in gaps or misalignment.

---

#### `tab_hole_diameter` (mm, range: 2–6)
**What it does:** Diameter of the cylindrical male tabs (and matching female slots).
- **Increase (e.g., 4→5)**: Larger tabs, stronger locking, harder to separate
- **Decrease (e.g., 4→3)**: Smaller tabs, easier to adjust, weaker locking, may fall apart
- **Recommended**: 4mm (good balance; typical print tolerance handles this well)

**Impact**: Controls interlocking strength; too small = tiles slide apart, too large = difficult to assemble.

---

#### `tab_offset` (mm, range: 0.5–3)
**What it does:** Distance from edge to the center of male tabs.
- **Effect on model**: Positions tabs inward from the edge (prevents tabs from sticking out)
- **Increase (e.g., 1.5→2.5)**: Tabs positioned deeper from edge, more interior placement
- **Decrease (e.g., 1.5→0.8)**: Tabs closer to edge, more exposed
- **Default**: 1.52mm (positioned to avoid edge breakage)

**Impact**: Affects tab placement reliability; improper values may place tabs outside tile or too close to edge.

---

#### `male_tab_clearance` (mm, range: 0–0.5)
**What it does:** Tolerance gap around male tabs for fit adjustment.
- **Effect on model**: Enlarges male tab diameter slightly to account for print shrinkage/fit
- **Increase (e.g., 0.1→0.3)**: Looser fit, tabs slide easily, easier assembly
- **Decrease (e.g., 0.1→0.05)**: Tighter fit, snugger connection, may be hard to assemble
- **Typical tuning**: Start at 0.1mm, adjust based on first print

**Note**: Female slots automatically match this clearance.

**Impact**: Critical for assembly experience; too tight = stuck tiles, too loose = no locking.

---

### Single Tile Only

#### `trim_width` (mm, range: -3 to +8)
**What it does:** Adds or subtracts width from a single tile.
- **Effect on model**: Adjusts final tile width beyond the standard grid calculation
- **Positive (e.g., +2)**: Makes tile 2mm wider (adds solid material on edges)
- **Negative (e.g., -3)**: Makes tile 3mm narrower (reduces material)
- **Formula**: `final_width = (tile_columns × hole_center_spacing) + trim_width`
- **Use case**: Fitting exact drawer dimensions, custom sizing

**Note**: Ignored in "drawer_grid" mode; only applies in "single_tile" mode.

**Impact**: Fine-tunes final dimensions for tight-fit applications.

---

#### `trim_length` (mm, range: -3 to +8)
**What it does:** Adds or subtracts length from a single tile.
- **Effect on model**: Adjusts final tile length beyond the standard grid calculation
- **Positive (e.g., +2)**: Makes tile 2mm longer
- **Negative (e.g., -3)**: Makes tile 3mm shorter
- **Formula**: `final_length = (tile_rows × hole_center_spacing) + trim_length`

**Note**: Ignored in "drawer_grid" mode; only applies in "single_tile" mode.

**Impact**: Fine-tunes final dimensions for exact-fit projects.

---

#### `custom_label` (text field)
**What it does:** Adds optional text label to the tile for identification.
- **Effect on model**: Embossed text appears on tile surface (for organization/naming)
- **Example**: "Tool-A", "Drill-Bits", "Drawers-1" for multi-tile projects
- **Empty string**: No label (default)
- **Length**: Keep short (3–15 characters recommended) for readability at typical print size

**Impact**: Helps organize multi-tile projects; purely informational, doesn't affect function.

---

### Advanced Parameters

#### `edge_tile_min_width` (mm, range: 5–25)
**What it does:** Minimum acceptable width for partial edge tiles in drawer mode.
- **Effect on model**: Controls whether small remainder pieces are generated or discarded
- **How it works**: If remainder < `edge_tile_min_width`, no edge tile is generated; if remainder > this value, an edge tile is created
- **Increase (e.g., 12→15)**: Discards more remainder tiles, simpler output, may waste space
- **Decrease (e.g., 12→8)**: Generates more small edge tiles, complete coverage, more pieces to manage
- **Recommended**: 12mm (avoids tiny, fragile pieces)

**Example**:
- Drawer width: 400mm, Full tile: 152.4mm
- 400 % 152.4 = 95.2mm remainder
- If `edge_tile_min_width = 100`: Remainder < 100 → no edge tile generated (wastes 95.2mm)
- If `edge_tile_min_width = 90`: Remainder > 90 → edge tile created (95.2mm piece generated)

**Impact**: Balances between complete coverage and avoiding impractically small pieces.

## 📐 Design Reference

**Hole Layout Formula:**
```
Board Width (mm) = num_cols × hole_spacing + trim_width
Board Length (mm) = num_rows × hole_spacing + trim_length
```

**Drawer Mode:** Automatically calculates how many full tiles fit, then generates edge tiles for remainders.

**Lite Mode:** Creates a grid of circular support webs around holes instead of solid material, reducing filament by ~40-50%.

**Tab System:** Female slots are cut into surfaces; male tabs on adjacent tiles lock into them. Optional connector pieces join female-to-female faces.

---

## 🚀 Quick Start Scenarios

### Scenario 1: Fill Existing Drawer (Beginner)
**Goal:** Create a pegboard grid to fit your existing toolbox drawer.

**Steps:**
1. Measure your drawer interior: width and length (in mm)
2. Set `print_mode = "drawer_grid"`
3. Set `drawer_width` and `drawer_length` to your measurements
4. Keep defaults for everything else
5. Preview to see color-coded tiles; export STL

**Expected result:** Automatic tile layout perfectly sized for your drawer, with interlocking connections.

---

### Scenario 2: Lightweight Project (Filament-Conscious)
**Goal:** Create pegboard tiles while saving 40-50% on filament.

**Steps:**
1. Set `use_lightweight = true`
2. (Optional) Reduce `base_thickness` from 8mm to 6mm
3. (Optional) Adjust `lightweight_web_spacing` (lower = stronger, higher = lighter)
4. Keep other parameters at defaults
5. Export and slice

**Expected result:** Web-pattern design visible on surfaces; significantly less material; same functionality.

**Tuning tips:**
- If webs seem too sparse: decrease `lightweight_web_spacing` to 4–5
- If too heavy: increase to 10–12
- `lightweight_thickness = 3` is a good balance

---

### Scenario 3: Custom Single Tile (Prototyping)
**Goal:** Create one test tile to evaluate your design before full project.

**Steps:**
1. Set `print_mode = "single_tile"`
2. Set `tile_columns = 8` and `tile_rows = 8` (reasonable starting point)
3. Adjust `pin_hole_diameter` to match your pegs (common: 4.2–6.0mm)
4. Test print with defaults

**Expected result:** Single 76×76mm tile (with 8×8 holes, 9.5mm spacing).

**Next steps:**
- Once satisfied, scale up to 16×16 for full projects
- Test interlocking by setting one tab direction to "male" and adjacent to "female"

---

### Scenario 4: Wall-Mounted Display (Advanced)
**Goal:** Create an interlocking wall-mounted pegboard display.

**Steps:**
1. Set `print_mode = "single_tile"`
2. Set `tile_columns = 12`, `tile_rows = 12` (suitable for wall)
3. Configure tabs for specific interlocking pattern:
   - Back/left: `tab_back = "female"`, `tab_left = "female"`
   - Front/right: `tab_front = "male"`, `tab_right = "male"`
4. Set `base_thickness = 6` (lighter for wall mounting)
5. Export multiple copies

**Expected result:** Tiles that interlock horizontally and vertically when arranged; strong wall-mount connection.

**Assembly hint:** Arrange like checkerboard so male tabs always meet female slots.

---

### Scenario 5: Standard Pegboard (1/4" Compatible)
**Goal:** Create standard 1/4" pegboard-compatible tiles.

**Steps:**
1. Set `pin_hole_diameter = 6.0` (1/4" = 6.35mm, 6.0mm is practical)
2. Set `hole_center_spacing = 10.0` (standard 1/4" spacing)
3. Set `tile_columns = 12`, `tile_rows = 12`
4. Set `base_thickness = 8` (standard pegboard thickness)
5. Optional: add `use_lightweight = true` for material savings

**Expected result:** Standard pegboard-compatible tiles (91×91mm with 12×12 holes).

**Compatibility:** Works with existing 1/4" pegboard pegs and accessories.

---

## 🔧 Examples

**Small Pegs (1/4" Pegboard Standard)**
```
pin_hole_diameter = 6.0
hole_center_spacing = 10.0
tile_columns = 16, tile_rows = 16
base_thickness = 8
```

**Lightweight Setup**
```
use_lightweight = true
lightweight_thickness = 3
lightweight_web_spacing = 6
base_thickness = 6
```

**Wall Display (Interconnected)**
```
print_mode = "single_tile"
tile_columns = 8, tile_rows = 8
tab_front = "male", tab_back = "female"
tab_left = "male", tab_right = "female"
```

**Large Drawer Fill**
```
print_mode = "drawer_grid"
drawer_width = 400, drawer_length = 600
tile_columns = 16, tile_rows = 16
```

---

## 🔗 Parameter Interaction Guide

This section explains how parameters interact with each other and what happens when you change combinations.

### Tile Size Calculation

**Formula for single tiles:**
```
Tile Width (mm)  = (tile_columns × hole_center_spacing) + trim_width
Tile Height (mm) = (tile_rows × hole_center_spacing) + trim_length
```

**Example:**
- `tile_columns = 16`, `hole_center_spacing = 9.5`, `trim_width = 0`
- Result: Width = (16 × 9.5) + 0 = **152mm**

**Changing `hole_center_spacing` affects all tiles:**
- Increase spacing by 0.5mm → All tiles grow by 8mm width (0.5 × 16)
- This cascades through drawer calculations

### Drawer Mode Automatic Calculation

**In drawer_grid mode:**
1. Script calculates full tiles: `floor(drawer_width / (tile_columns × hole_spacing))`
2. Calculates remainder: `drawer_width % (tile_columns × hole_spacing)`
3. If remainder > `edge_tile_min_width` → creates edge tile
4. Otherwise → discards and previous full tile covers remainder

**Example scenario:**
```
drawer_width = 400mm
tile_columns = 16
hole_center_spacing = 9.5

Full tile width = 16 × 9.5 = 152mm
Full tiles in width = floor(400 / 152) = 2 full tiles
Remainder = 400 % 152 = 96mm

If edge_tile_min_width = 12 (96 > 12):
  → Generate 1 edge tile of 96mm width
  → Total: 2 full tiles + 1 edge tile

If edge_tile_min_width = 100 (96 < 100):
  → Don't generate edge tile
  → Total: 2 full tiles (covers 304mm, wastes 96mm)
```

### Lightweight Mode Interactions

**When `use_lightweight = true`:**
- `lightweight_thickness` determines web strength
- `lightweight_web_spacing` determines support density
- `base_thickness` still determines overall Z-height

**Trade-off equation:**
```
Material = ~40-50% of solid mode (controlled by web_spacing)
Strength = proportional to web_thickness + web_spacing density
Print time = reduced by ~50%
```

**Optimization example:**
- Want lightest possible: `web_spacing = 12`, `lightweight_thickness = 2`
- Want strongest webs: `web_spacing = 4`, `lightweight_thickness = 4`
- Balanced default: `web_spacing = 8`, `lightweight_thickness = 3`

### Tab System Dependencies

**Tab configuration requires thinking ahead:**
```
Tile placement:  [A] [B]
                 [C] [D]

Tile A needs:    Right edge = MALE (to lock into B)
                 Bottom edge = MALE (to lock into C)

Tile B needs:    Left edge = FEMALE (receives from A)
                 Bottom edge = MALE (to lock into D)

Tile C needs:    Top edge = FEMALE (receives from A)
                 Right edge = MALE (to lock into D)

Tile D needs:    Top edge = FEMALE (receives from C)
                 Left edge = FEMALE (receives from B)
```

**Male tab diameter must match female slot:**
- `tab_hole_diameter` controls both male tab size and female slot size
- `male_tab_clearance` enlarges male tabs for easier assembly
- Changing either affects interlocking fit

### Peg Compatibility Chain

**Your tool pegs determine these parameters:**
```
Tool peg diameter
    ↓
pin_hole_diameter (should be 0.2-0.4mm larger for clearance)
    ↓
Hole layout on board
    ↓
Board width/height
    ↓
Lightweight web placement (webs positioned around holes)
```

**Example for 6mm pegs:**
- Set `pin_hole_diameter = 6.2` (slight clearance)
- 6.0mm pegs will fit with light friction
- Lightweight webs won't interfere with peg insertion

### Printing Impact Summary

| Parameter | Increase | Decrease |
|-----------|----------|----------|
| `tile_columns` / `tile_rows` | Wider/taller tiles, fewer pieces | Smaller tiles, more pieces |
| `base_thickness` | Slower print, more weight | Faster print, lighter, fragile |
| `use_lightweight = true` | -50% print time, -50% weight | Solid mode, normal strength |
| `pin_hole_diameter` | Larger holes, easier pegs | Tighter fit, precise tolerance |
| `hole_center_spacing` | All tiles grow, fewer fit drawer | All tiles shrink, more fit |
| `tab_hole_diameter` | Stronger locking, hard to assemble | Weak locking, easy to separate |

### Common Mistake Prevention

**Mistake #1: Changing spacing mid-project**
- If you print tile A with 9.5mm spacing, don't print tile B with 10.0mm spacing
- They won't interlock; spacing must be consistent across all tiles

**Mistake #2: Wrong tab directions**
- If `tab_right = "male"` on all tiles, they can't connect horizontally
- Ensure alternating male/female pattern

**Mistake #3: Too tight male tab clearance**
- Default 0.1mm is good for most 3D printers
- If assembly is impossible, increase to 0.2-0.3mm
- If tabs are too loose, decrease to 0.05mm

**Mistake #4: Lightweight webs too sparse**
- If `lightweight_web_spacing = 16` on 4-column tiles, you may have sections with no support
- Keep spacing ≤ 2× number of columns for adequate support

---

## 🙏 Attribution

**Original Creator:** [Akmjoe](https://www.printables.com/@Akmjoe_246598)

This project is derived from the original **Toolgrid Board Generator** published on Printables:
- **Printables Model:** https://www.printables.com/model/1455970-toolgrid-board-generator/files
- **Creator Profile:** https://www.printables.com/@Akmjoe_246598

This version (maintained December 2024) includes comprehensive documentation, a detailed code review with improvement roadmap, and enhanced usability features. See [`docs/todo.md`](docs/todo.md) for the complete list of identified improvements and fixes.

**Repository:** https://github.com/marcelrienks/ToolGrid
