# OpenSCAD Toolgrid Generator V2

A parametric OpenSCAD script for generating customizable toolbox organization grids with interlocking tiles. Create single tiles or complete drawer grids that tessellate together like puzzle pieces.

## 📋 Overview

This generator creates modular pegboard-style organizing grids designed for tool storage. Each tile interlock with its neighbors through male/female tab systems, allowing flexible configuration and scalability.

### Key Features
- **Single Tile Mode**: Generate individual tiles with custom dimensions (4×4 up to 16×16 holes)
- **Drawer Mode**: Automatically tile a complete drawer with perfect fit, creating edge-matched remainder pieces
- **Lightweight Option**: Cross-brace design reduces material while maintaining strength
- **Interlocking Tabs**: Male/female locking tabs ensure tiles stay aligned
- **Customizable Holes**: Adjust hole diameter and spacing for different tool peg sizes
- **Connector Pieces**: Optional connector pieces for joining tiles without gluing
- **Labeling**: Add quantity and custom labels to tiles for organization
- **Print-Optimized**: Tiles nest efficiently for 3D printing

---

## 🎯 Current Functionality

### 1. **Single Tile Generation**
Generate an individual tile with specified dimensions:
- **Hole Range**: 4 to 16 columns × 4 to 16 rows
- **Customizable**: Hole diameter, hole spacing, board thickness
- **Trimming**: Adjust width/length by ±8mm for custom fit
- **Optional**: Apply lightweight (lite) mode, add labels

**Use Case**: Create tiles to fit a specific space or test design before printing full set.

### 2. **Drawer Grid Mode**
Generate a complete set of tiles to perfectly fill a drawer:
- **Automatic Layout**: Calculates how many full tiles fit, plus edge remainder pieces
- **Edge Handling**: Creates appropriate partial tiles for width/length remainders
- **Optimized Nesting**: All tiles output in single STL with qty labels for batch printing
- **Visual Preview**: Color-coded tile types in preview mode (red/blue checkerboard for full tiles, yellow/green/pink for remainders)

**Use Case**: Print organized grid system for existing drawer or toolbox.

### 3. **Interlocking Tab System**
Tiles connect together without fasteners using tab-and-slot mechanism:
- **Tab Types**: Male (raised), Female (recessed), None
- **Independent Per-Side**: Front, back, left, and right can be configured separately
- **Flexible Patterns**: Mix and match for different layout options
- **Clearance Adjustable**: Fine-tune fit tolerance

**Tab System Details**:
- Female slots are cut into tile surfaces
- Male tabs lock into these slots on adjacent tiles
- Creates rigid, self-supporting grid structure
- Optional connector pieces can join female-to-female faces

### 4. **Lightweight (Lite) Mode**
Reduces material usage with cross-brace internal structure:
- **Cross-Pattern**: Grid of thin support webs instead of solid material
- **Material Savings**: ~40-50% less plastic
- **Performance**: Maintains strength for most tool weights
- **Customizable**: Adjust web thickness and spacing

**How It Works**:
- Creates a grid of circular profiles around each hole region
- Spacing adjustable: controls how many holes between support webs
- Compatible with both single tile and drawer modes

### 5. **Connector Piece**
Optional part for joining tiles:
- **Purpose**: Connects two female tab faces together
- **Design**: Two cylindrical pegs matching male tab dimensions
- **Use Case**: Connect tiles in creative patterns or extend existing grids

---

## 🎮 Getting Started

### Requirements
- [OpenSCAD](https://openscad.org/) (free, open-source 3D modeling software)
- 3D Printer (FDM recommended - PLA, PETG, ABS)

### Basic Usage

1. **Open in OpenSCAD**
   ```bash
   open toolgrid-generator-v2.scad
   ```

2. **Customize Parameters** (View → Customizer)
   - Set `drawer = false` for single tile
   - Set `drawer = true` for complete drawer grid
   - Adjust tile dimensions, hole size, board thickness

3. **Preview** (Press spacebar or View → Preview)
   - Single tile: Shows one tile
   - Drawer mode: Shows color-coded tile arrangement

4. **Export** (File → Export as STL)
   - Choose filename and location
   - Configure slice/print settings in your slicer

---

## ⚙️ Customizer Parameters

### Mode Selection
- **`drawer`** (true/false): Generate full drawer grid vs single tile
- **`part`** (tiles/connector): Generate tiles or connector piece only

### Drawer Dimensions
- **`drawer_width`** (mm): Interior width of drawer
- **`drawer_length`** (mm): Interior length of drawer

### Tile Configuration
- **`num_cols`** (4-16): Hole columns per standard tile
- **`num_rows`** (4-16): Hole rows per standard tile

### Hole Settings
- **`hole_diameter`** (mm): Size of tool peg holes
- **`hole_spacing`** (mm): Center-to-center distance between holes

### Material
- **`lite`** (true/false): Enable lightweight cross-brace mode
- **`board_thickness`** (mm): Base thickness (6mm minimum recommended)
- **`lite_thickness`** (mm): Cross-brace thickness in lite mode
- **`web_spacing`** (4-16): Holes between support webs (lite mode)

### Interlocking Tabs
- **`tab_front`**, **`tab_back`**, **`tab_left`**, **`tab_right`**: (male/female/none)
  - Male: Raised tabs that lock into slots
  - Female: Recessed slots that accept male tabs
  - None: No tabs on this edge
- **`tab_diameter`** (mm): Size of locking hole
- **`tab_side`** (mm): Distance from edge to tab center
- **`tab_clearance`** (mm): Tolerance around male tabs

### Single Tile Trim
*(Ignored in drawer mode)*
- **`trim_width`** (mm): Add/subtract width
- **`trim_length`** (mm): Add/subtract length

### Advanced
- **`minimum_width`** (mm): Minimum width for edge tiles (narrower discarded)
- **`label`**: Custom text label for backside

---

## 📐 Design Details

### Hole Layout
- Holes are arranged in a regular grid
- Hole spacing defines both X and Y spacing (default 9.5mm)
- First hole is centered 0.5 × hole_spacing from origin

### Tile Dimensions Formula
```
Board Width (mm) = num_cols × hole_spacing + trim_width
Board Length (mm) = num_rows × hole_spacing + trim_length
```

### Drawer Mode Algorithm
1. Calculate how many complete full-size tiles fit
2. Calculate remainder dimensions
3. For remainders ≥ minimum_width: create partial tiles
4. For remainders < minimum_width: expand previous tile or discard
5. Output all pieces with qty labels

**Example**: 231mm drawer width with 16-column tiles (152mm each)
- 1 full tile (152mm) fits
- Remainder: 79mm → creates edge tile with 8 columns (76mm actual)

### Lite Mode Geometry
- Divides tile into grid of sections
- Sections determined by `web_spacing` parameter
- Creates circular profiles around hole regions
- Minkowski operation generates curved support webs

### Tab System
- Tabs positioned at 4th and 12th hole positions (standard layout)
- Female slots cut as cylinders through board thickness
- Male tabs extend tab_side distance beyond board edge
- Clearance allows male tab to slide into female slot with slight resistance

---

## 🖨️ Printing & Assembly

### Print Settings
- **Support**: Generally not needed
- **Infill**: 15-20% (tiles have interior geometry for strength)
- **Orientation**: Flat on build plate (largest surface area)
- **Nesting**: Can print multiple tiles at once

### Assembly
1. Print all tiles and connectors
2. Arrange tiles in desired layout
3. Insert male tabs into female slots
4. Use connectors to join faces without tabs
5. Adjust spacing to ensure grid is square

### Post-Processing
- Clean support marks if needed
- Test tab fit before committing to layout
- Consider sanding high-friction tabs for smoother sliding

---

## 🐛 Known Issues & Limitations

### Current Known Issues
See [`docs/todo.md`](docs/todo.md) for detailed bug list and improvements.

**Critical**: 
- Drawer mode remainder calculation has bug with non-square tile counts (Line 81)
- Lite mode doesn't properly handle remainders in some cases (Line 118)

### Limitations
- Tab positions fixed at 4th and 12th holes (doesn't adapt to all tile sizes)
- Connector piece designed only for standard 2-tab system
- Text labels may overlap with small tiles
- Maximum practical tile size ~16×16 holes (size constraints for printing)

---

## 🔧 Customization Examples

### Example 1: Small Tool Pegs (1/4" Pegboard)
```
hole_diameter = 6.0
hole_spacing = 10.0  // matches standard pegboard spacing
num_cols = 16
num_rows = 16
board_thickness = 8
```

### Example 2: Lightweight Setup (filament savings)
```
lite = true
lite_thickness = 3
web_spacing = 6  // more webs for strength with thin material
board_thickness = 6
```

### Example 3: Interconnected Wall Display
```
drawer = false
num_cols = 8
num_rows = 8
tab_front = "male"
tab_back = "female"
tab_left = "male"
tab_right = "female"
// Creates checkerboard interlocking when tiles placed in grid
```

### Example 4: Large Drawer (multiple standard tiles + edges)
```
drawer = true
drawer_width = 400
drawer_length = 600
num_cols = 16
num_rows = 16
// Automatically calculates all needed pieces
```

---

## 📊 Output Files

The script generates:

### Single Tile Mode
- **Main output**: Single pegboard tile with configured holes and tabs
- **Contains**: Qty label (1) and optional custom label

### Drawer Mode (Export)
- **All tiles stacked** in single STL file
- **Labels**: Each tile type marked with quantity ("x4" means 4 identical tiles)
- **Organization**: 
  - Base tiles labeled "Base"
  - Right edge tiles labeled "Side-Right"
  - Back edge tiles labeled "Side-Back"
  - Corner tile labeled "Corner"

### Connector Mode
- **Connector piece**: Small connector with two pegs
- **Use**: Join two female-tab faces

---

## 📈 Console Output

The script echoes helpful information:
```
Board width:  X mm
Board length: Y mm
Board width:  X inches
Board length: Y inches
Total width:  X mm (drawer mode)
Total length: Y mm (drawer mode)
```

Use this to verify dimensions before printing.

---

## 📚 Technical Documentation

### File Structure
```
toolgrid-generator-v2.scad
├── Customizer Parameters (lines 1-67)
├── Calculated Parameters (lines 70-87)
├── Module Definitions:
│   ├── pegboard() - creates base board with holes
│   ├── lite() - adds lightweight cross-braces
│   ├── tabs() - creates male tabs
│   ├── slot() - creates female slots
│   ├── connector() - creates connector piece
│   └── unit() - combines all above into complete tile
└── Main Generation Logic (lines 201-299)
```

### Key Variables
- `num_cols`, `num_rows`: Tile grid dimensions
- `board_width_mm`, `board_length_mm`: Calculated tile dimensions
- `full_tiles_width`, `full_tiles_length`: Count of complete tiles in drawer
- `remainder_cols`, `remainder_rows`: Columns/rows in partial tiles
- `tab_position`: X positions where tabs are placed

### Tab System
- Female slots: Subtracted (difference operation) from main board
- Male tabs: Added (union operation) at board edges
- Both use same diameter and clearance parameters for fit

---

## 🚀 Future Improvements

Planned enhancements (see `docs/todo.md`):
- [ ] Improved variable naming for clarity
- [ ] Dynamic tab positioning based on tile size
- [ ] Input validation with helpful warnings
- [ ] Support for custom hole patterns
- [ ] Honeycomb lite mode alternative
- [ ] Edge beveling for easier assembly
- [ ] Magnetic insert support holes

---

## 📞 Support & Troubleshooting

### Common Issues

**Tiles don't fit together**
- Check `tab_clearance` - increase if too tight
- Verify `hole_spacing` matches between all tiles
- Ensure no scaling applied during export

**Edge remainders missing or too small**
- Check `minimum_width` parameter
- Verify drawer dimensions in mm
- Look at console output to confirm tile counts

**Holes not aligned after printing**
- Verify `hole_spacing` and `hole_diameter` in export
- Check printer calibration (especially X/Y)
- Ensure no scale applied in slicer

**Text labels overlapping**
- Reduce label length or choose "none" for label
- Use smaller `custom_label` text
- Manually relocate label if needed

**Lite mode looks wrong**
- Confirm `lite_thickness` > 2mm
- Check `web_spacing` isn't too large
- Verify `hole_diameter` is appropriate for material

---

## 📜 License & Credits

This script is open-source and available for personal and commercial use. Modifications and derivative works encouraged.

---

## 📝 Version History

**v2.0** (Current)
- Complete drawer mode with automatic tiling
- Interlocking tab system
- Lightweight (lite) mode with cross-braces
- Connector piece support
- Label and quantity tracking
- Multi-language comment support

**v1.0** 
- Basic single tile generation
- Fixed tab positions

---

## 📖 Examples & Gallery

See included STL files for reference:
- `base_tile_full.stl` - Standard 16×16 tile (full solid)
- `base_tile_lite.stl` - Standard 16×16 tile (lightweight)
- `connector.stl` - Connector piece for joining
- `example_set.stl` - Sample of different tile types
- `test-drawer.stl` - Complete drawer fill (473×231mm)

---

**Last Updated**: December 21, 2024  
**Script Version**: 2.0  
**OpenSCAD Compatibility**: 2019.05+
