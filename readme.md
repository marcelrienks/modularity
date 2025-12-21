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
   - `drawer`: true for drawer grid, false for single tile
   - `num_cols` / `num_rows`: 4-16 holes per tile
   - `hole_diameter`: Size of tool peg holes
   - `hole_spacing`: Distance between hole centers
   - `board_thickness`: Base thickness in mm (6mm minimum)
   - `lite`: Enable lightweight cross-braces (true/false)
   - Tab configuration: Set front, back, left, right to male/female/none

3. **Preview** (Press spacebar or View → Preview)
   - Single tile mode: Shows one tile
   - Drawer mode: Color-coded layout showing full and edge tiles

4. **Export as STL** (File → Export as STL)
   - Choose filename and location
   - Import into your 3D slicer software


---

## ⚙️ Parameters

### Mode
- **`drawer`** (true/false): Drawer grid mode or single tile
- **`part`** (tiles/connector): Generate tiles or connector only

### Drawer
- **`drawer_width`** (mm): Interior width
- **`drawer_length`** (mm): Interior length

### Tile Grid
- **`num_cols`** (4-16): Hole columns per tile
- **`num_rows`** (4-16): Hole rows per tile

### Holes
- **`hole_diameter`** (mm): Peg hole size
- **`hole_spacing`** (mm): Center-to-center distance

### Material
- **`lite`** (true/false): Enable lightweight mode
- **`board_thickness`** (mm): Base thickness (6mm minimum)
- **`lite_thickness`** (mm): Cross-brace thickness
- **`web_spacing`** (4-16): Holes between support webs

### Tabs
- **`tab_front`**, **`tab_back`**, **`tab_left`**, **`tab_right`**: male/female/none
- **`tab_diameter`** (mm): Tab hole size
- **`tab_side`** (mm): Distance from edge to tab center
- **`tab_clearance`** (mm): Tolerance around male tabs

### Single Tile Only
- **`trim_width`** (mm): Add/subtract width (ignored in drawer mode)
- **`trim_length`** (mm): Add/subtract length (ignored in drawer mode)
- **`label`**: Optional custom label

## 📐 Design Reference

**Hole Layout Formula:**
```
Board Width (mm) = num_cols × hole_spacing + trim_width
Board Length (mm) = num_rows × hole_spacing + trim_length
```

**Drawer Mode:** Automatically calculates how many full tiles fit, then generates edge tiles for remainders.

**Lite Mode:** Creates a grid of circular support webs around holes instead of solid material, reducing filament by ~40-50%.

**Tab System:** Female slots are cut into surfaces; male tabs on adjacent tiles lock into them. Optional connector pieces join female-to-female faces.

## 🔧 Examples

**Small Pegs (1/4" Pegboard Standard)**
```
hole_diameter = 6.0
hole_spacing = 10.0
num_cols = 16, num_rows = 16
board_thickness = 8
```

**Lightweight Setup**
```
lite = true
lite_thickness = 3
web_spacing = 6
board_thickness = 6
```

**Wall Display (Interconnected)**
```
drawer = false
num_cols = 8, num_rows = 8
tab_front = "male", tab_back = "female"
tab_left = "male", tab_right = "female"
```

**Large Drawer Fill**
```
drawer = true
drawer_width = 400, drawer_length = 600
num_cols = 16, num_rows = 16
```

---

## 🙏 Attribution

**Original Creator:** [Akmjoe](https://www.printables.com/@Akmjoe_246598)

This project is derived from the original **Toolgrid Board Generator** published on Printables:
- **Printables Model:** https://www.printables.com/model/1455970-toolgrid-board-generator/files
- **Creator Profile:** https://www.printables.com/@Akmjoe_246598

This version (maintained December 2024) includes comprehensive documentation, a detailed code review with improvement roadmap, and enhanced usability features. See [`docs/todo.md`](docs/todo.md) for the complete list of identified improvements and fixes.

**Repository:** https://github.com/marcelrienks/ToolGrid
