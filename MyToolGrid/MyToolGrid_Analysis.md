# MyToolGrid - Detailed 3D Model Analysis

## Overview
**Model Name:** MyToolGrid  
**Version:** v1  
**Format:** STEP AP214 (AUTOMOTIVE_DESIGN)  
**Units:** Millimeters (mm)  

---

## Overall Dimensions

### Bounding Box
- **Perimeter walls outer edge:** 100.00 mm × 100.00 mm (excluding tabs)
- **Absolute dimensions (including tabs):** 102.00 mm × 102.00 mm
  - Tabs extend 2.00 mm beyond the 100mm wall boundary on top and right edges
- **Height (Z-axis):** 6.00 mm (total thickness)
  - **First extrusion (Z=0 to Z=3):**
    - Perimeter walls: 1.5mm thick (outer edge at 100mm, inner edge at 98.5mm)
    - Tabs: Ø4mm half-cylindrical protrusions (extend 2mm beyond 100mm wall boundary, adding to wall thickness)
    - Slots: Ø4mm half-cylindrical recesses (cut into perimeter)
    - Cylinders: Ø7mm separate bodies
  - **Second extrusion (Z=3 to Z=6):**
    - Top layer: 3.00 mm solid layer covering entire area
    - Tabs continue through top layer (total height Z=0→6)
    - Slots continue through top layer (total depth Z=0→6)
  - **Final result:** Single unified solid body

### Base Geometry
- **Shape:** Rectangular plate/panel
- **Origin:** Corner at (0, 0, 0)
- **Maximum extent:** (100, 100, 6) mm

## Feature Pattern Analysis

The model contains **100 interior through-holes** and **36 edge interlocking features** (18 tabs + 18 slots).

### Interior Grid: Ø4mm Through-Holes
- **Quantity:** 100 holes
- **Diameter:** 4.0 mm (2.0 mm radius)
- **Cylinder structure:** Each hole is centered within a Ø7.0mm cylinder (initially separate solid, united by top layer)
- **Pattern:** 10×10 regular grid
- **Grid Spacing:** 10 mm (center-to-center)
- **First hole center:** 5 mm from left edge (X), 5 mm from bottom edge (Y)
- **Last hole center:** 95 mm from left edge (X), 95 mm from bottom edge (Y) - maintains 5mm clearance from all edges
- **X Positions:** 5, 15, 25, 35, 45, 55, 65, 75, 85, 95 mm
- **Y Positions:** 5, 15, 25, 35, 45, 55, 65, 75, 85, 95 mm
- **Z Position:** 0 to 6 mm (through entire tile thickness)
- **Hole depth:** 6 mm total (3mm through cylinder Z=0→3, 3mm through top layer Z=3→6)
- **Cylinder Details:**
  - Each Ø7mm cylinder (Z=0 to Z=3) is initially a separate body, 3mm extrusion from bottom surface
  - Ø4mm through-hole penetrates cylinder (Z=0→3) and continues through top layer (Z=3→6)
  - Top layer (Z=3 to Z=6) sits flush above cylinders and unites them into single solid
  - From below: Empty space exists between/around Ø7mm cylinder bases from Z=0→3 (cylinders occupy only their Ø7mm footprint, remainder is empty space with no material infill)

## Edge Interlocking Features (Tabs & Slots)

### Tab Features: Ø4.0mm Half-Cylindrical Extrusions (Top & Right Edges)
- **Quantity:** 18 tabs total
  - **Right edge (X=100):** 9 tabs
  - **Top edge (Y=100):** 9 tabs
- **Diameter:** 4.0 mm (2.0 mm radius)
- **Geometry:** Half-cylindrical protrusions extending outward from the tile edge
- **Pattern:** L-shaped arrangement along top and right edges
- **Positions:**
  - **Right edge (X=100):** 9 tabs at Y = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
  - **Top edge (Y=100):** 9 tabs at X = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
- **Spacing:** 10 mm (center-to-center)
- **Z Position:** 0 to 6 mm (6mm extrusion through full tile height)
- **Height:** 6 mm (full plate thickness)
- **Note:** These tabs fit into the corresponding slots on adjacent tiles

### Slot Features: Ø4.0mm Half-Cylindrical Cutouts (Bottom & Left Edges)
- **Quantity:** 18 slots total
  - **Left edge (X=0):** 9 slots
  - **Bottom edge (Y=0):** 9 slots
- **Diameter:** 4.0 mm (2.0 mm radius)
- **Geometry:** Half-cylindrical recesses cut into the tile edge (semi-circular slots)
- **Pattern:** L-shaped arrangement along bottom and left edges
- **Positions:**
  - **Left edge (X=0):** 9 slots at Y = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
  - **Bottom edge (Y=0):** 9 slots at X = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
- **Spacing:** 10 mm (center-to-center)
- **Z Position:** 0 to 6 mm (6mm extrusion through full tile height)
- **Depth:** 6 mm (full plate thickness)
- **Note:** These slots receive the tabs from adjacent tiles, enabling tile-to-tile connection

---

## Feature Summary by Location

### Interior Grid (Center Area)
- **100 through-holes** within cylindrical structures:
  - Through-hole diameter: Ø4.0mm (6mm deep total: 3mm through cylinder + 3mm through top layer)
  - Cylinder outer diameter: Ø7.0mm (visible from bottom view)
  - Cylinder extrusion: 3mm (Z=0 to Z=3), separate bodies until united by top layer
  - Top layer: 3mm extrusion (Z=3 to Z=6) unites cylinders and perimeter into single solid
  - Top layer surface is continuous; only Ø4mm holes visible from above
  - Bottom view shows intentional empty space between/around cylinders from Z=0→3 for lightweight design (cylinders occupy only their Ø7mm footprint)
- **Grid:** 10×10 array
- **Spacing:** 10mm × 10mm (center-to-center)
- **First hole center:** 5mm from left edge (X), 5mm from bottom edge (Y)
- **Purpose:** Mounting points for tool-holding attachments

### Edge Interlocking Features

#### Bottom and Left Edges (X=0 and Y=0)
- **18 slots total**
  - **Bottom edge (Y=0):** 9 slots
  - **Left edge (X=0):** 9 slots
- **Diameter:** Ø4.0mm
- **Type:** Half-cylindrical recesses (semi-circular cutouts at edge)
- **Spacing:** 10mm
- **Start position:** 10mm from corner
- **Purpose:** Receives tabs from adjacent tiles

#### Top and Right Edges (X=100 and Y=100)
- **18 tabs total**
  - **Top edge (Y=100):** 9 tabs
  - **Right edge (X=100):** 9 tabs
- **Diameter:** Ø4.0mm
- **Type:** Half-cylindrical protrusions extending from edge
- **Spacing:** 10mm
- **Start position:** 10mm from corner
- **Purpose:** Inserts into slots of adjacent tiles

---

## Parameterization Guidelines

### Primary Parameters for Scripting

#### Base Plate
```
plate_length = 100.0              // mm (X-axis)
plate_width = 100.0               // mm (Y-axis)
plate_thickness = 6.0             // mm (Z-axis, total height Z=0 to Z=6)
perimeter_wall_thickness = 1.5    // mm (thickness in X-Y plane)
perimeter_wall_extrusion = 3.0    // mm (Z=0 to Z=3)
cylinder_extrusion = 3.0          // mm (Z=0 to Z=3)
top_layer_extrusion = 3.0         // mm (Z=3 to Z=6, covering perimeter walls and cylinders)
tab_extrusion = 6.0               // mm (Z=0 to Z=6, integrated into perimeter walls)
```

#### Interior Grid Holes
```
interior_grid_rows = 10
interior_grid_cols = 10
interior_grid_spacing = 10.0       // mm (center-to-center)
interior_grid_offset_x = 5.0       // mm (first hole center from left edge)
interior_grid_offset_y = 5.0       // mm (first hole center from bottom edge)
interior_hole_dia = 4.0            // mm (through-hole diameter)
interior_cylinder_dia = 7.0        // mm (cylinder outer diameter)
interior_hole_depth = 6.0          // mm (3mm through cylinder Z=0→3 + 3mm through top layer Z=3→6)
// Note: Cylinders initially separate bodies (Ø7mm, 3mm extrusion Z=0→3), top layer (3mm extrusion Z=3→6) unites all into single solid
// Note: Intentional empty space between cylinders from Z=0→3 for lightweight design (no material infill except cylinder footprints and perimeter walls)
// Note: 5mm offset creates 5mm clearance from all edges (last hole at 95mm, 5mm from 100mm wall edge)
// Note: Tabs extend 2mm beyond 100mm wall boundary (absolute dimensions 102×102mm including tabs)
```

#### Edge Slots - Bottom/Left (X=0, Y=0)
```
edge_slot_count = 9                // per edge (18 total)
edge_slot_spacing = 10.0           // mm
edge_slot_start_offset = 10.0      // mm from corner
edge_slot_dia = 4.0                // mm (half-cylindrical cutout)
edge_slot_depth = 6.0              // mm (through)
```

#### Edge Tabs - Top/Right (X=100, Y=100)
```
edge_tab_count = 9                 // per edge (18 total)
edge_tab_spacing = 10.0            // mm
edge_tab_start_offset = 10.0       // mm from corner
edge_tab_dia = 4.0                 // mm (half-cylindrical protrusion)
edge_tab_height = 6.0              // mm (through)
```

### Derived Relationships
```
// Grid coverage area
grid_width = (interior_grid_cols - 1) * interior_grid_spacing   // 90mm
grid_height = (interior_grid_rows - 1) * interior_grid_spacing  // 90mm

// Total features
interior_holes_total = interior_grid_rows * interior_grid_cols  // 100
edge_slots_total = edge_slot_count * 2                          // 18 (9 bottom + 9 left)
edge_tabs_total = edge_tab_count * 2                            // 18 (9 top + 9 right)
total_edge_features = edge_slots_total + edge_tabs_total        // 36
```

---

## Design Intent & Functional Analysis

### Purpose
This is a **modular tool mounting tile** for toolbox organization with:
- Regular grid pattern for flexible tool positioning
- Interlocking edge features for connecting multiple tiles together

**Detailed Description:**
Multiple tiles with varying dimensions can be connected together to cover a predefined area for toolbox drawer organization. 

**From Top View (Smooth Surface):**
- Continuous solid top layer (3mm thick, Z=3 to Z=6) unites cylinders and perimeter walls into single part
- 100 through-holes (Ø4mm) in a 10×10 grid for mounting tool-holding attachments
- Holes spaced 10mm center-to-center, positioned 5mm from all edges (first at 5mm, last at 95mm)
- Half-circular tabs (6mm extrusion Z=0 to Z=6) on top edge (9 tabs) and right edge (9 tabs), Ø4mm
- Half-circular slots (6mm extrusion Z=0 to Z=6) on bottom edge (9 slots) and left edge (9 slots), Ø4mm

**Bottom View:**
- Interior reveals 100 individual Ø7mm cylinders, each with a Ø4mm through-hole
- Cylinders are 3mm extrusions (Z=0 to Z=3) from bottom surface, initially separate bodies
- Top layer (3mm thick, Z=3 to Z=6) unites cylinders and perimeter into final single solid part
- Perimeter walls (1.5mm thick, 3mm extrusion Z=0 to Z=3): outer edge at 100mm, inner edge at 98.5mm
- Bottom view shows intentional empty space between cylinders for lightweight design (Z=0→3, only cylinder footprints and perimeter walls occupy space)

**Edge Interlocking System:**
- **Tabs** (top/right edges): Half-cylindrical protrusions (Ø4mm) integrated into perimeter wall sketch, extend through both extrusions Z=0→6, project 2mm beyond 100mm wall boundary (add to wall thickness)
- **Slots** (bottom/left edges): Half-cylindrical recesses (Ø4mm) integrated into perimeter wall sketch as negative space, extend through both extrusions Z=0→6
- This tab-slot system allows multiple tiles to lie adjacent and interlock seamlessly
- **Absolute tile dimensions:** 102mm × 102mm including tab projections on top and right edges
- **Corner behavior:** No features at corners (0,0), (100,0), (0,100), (100,100) - tiles connect via edge tabs/slots only

### Assembly Strategy

#### Interior Grid
- 10×10 array provides 100 mounting points (Ø4mm through-holes) for tool-holding attachments
- Each Ø7mm cylinder is initially a separate body with 3mm extrusion (Z=0 to Z=3) from bottom surface
- Ø4mm through-holes penetrate cylinders (Z=0→3) and continue through top layer (Z=3→6) for 6mm total depth
- Top layer (3mm thick, Z=3 to Z=6) unites all cylinders and perimeter into final single solid part
- Intentional empty space between cylinders from Z=0→3 for lightweight design (material only at cylinder/perimeter locations)
- Interior holes positioned 5mm from perimeter wall edges with 10mm spacing creates 5mm clearance to all wall edges

#### Edge Interlocking System
- **Bottom/Left edges:** Slots (Ø4mm half-cylindrical recesses) receive tabs from adjacent tiles
- **Top/Right edges:** Tabs (Ø4mm half-cylindrical protrusions) insert into adjacent tile slots
- **Corners:** No interlocking features at four corners - tiles connect only via edge tabs/slots
- Tiles can be connected in any direction to form custom layouts, lying adjacent with edges interlocking 

---

## Manufacturing Considerations

### Tolerances
- Hole positions: ±0.1mm typical
- Hole diameters: H11 or H12 tolerance class

---

## Verification Checklist

For recreating this model parametrically, verify:

- [ ] Perimeter wall thickness: 1.5mm (outer edge at 100mm, inner edge at 98.5mm), 3mm extrusion (Z=0 to Z=3)
- [ ] Perimeter walls outer edge: 100×100 mm (wall boundary), inner edge at 98.5×98.5 mm
- [ ] Tabs extend 2mm beyond 100mm wall boundary (add to wall thickness, absolute dimensions 102×102mm including tabs)
- [ ] Cylinder structure: 100 Ø7mm cylinders (initially separate bodies), 3mm extrusion Z=0 to Z=3
- [ ] Top layer: 3mm extrusion (Z=3 to Z=6) unites cylinders and perimeter walls into final single solid part
- [ ] Intentional empty space: Between/around cylinders from Z=0→3 for lightweight design (no material infill except cylinder and perimeter footprints)
- [ ] Interior grid: 10×10 holes, 10mm spacing, first hole at (5,5), last hole at (95,95)
- [ ] Interior holes maintain 5mm clearance from all edges
- [ ] Interior through-holes: Ø4.0mm (6mm deep: 3mm through cylinder + 3mm through top layer)
- [ ] Each cylinder has Ø4mm through-hole penetrating cylinder (Z=0→3) continuing through top layer (Z=3→6)
- [ ] Bottom edge (Y=0): 9 slots (Ø4mm half-cylindrical recesses), integrated into perimeter walls, 10mm spacing, starting at 10mm
- [ ] Left edge (X=0): 9 slots (Ø4mm half-cylindrical recesses), integrated into perimeter walls, 10mm spacing, starting at 10mm
- [ ] Top edge (Y=100): 9 tabs (Ø4mm half-cylindrical protrusions), integrated into perimeter wall sketch, extend through both extrusions Z=0→6, extend 2mm beyond 100mm wall boundary (add to wall thickness), 10mm spacing, starting at 10mm
- [ ] Right edge (X=100): 9 tabs (Ø4mm half-cylindrical protrusions), integrated into perimeter wall sketch, extend through both extrusions Z=0→6, extend 2mm beyond 100mm wall boundary (add to wall thickness), 10mm spacing, starting at 10mm
- [ ] Tabs and slots are integrated into perimeter wall sketch profile (part of initial 2D outline, tabs add to wall thickness), extend through first extrusion (Z=0→3) and continue through second extrusion/top layer (Z=3→6)
- [ ] Corners: No interlocking features at (0,0), (100,0), (0,100), (100,100) - connection via edge features only

---

## Notes for Parametric Script Development

### Recommended Script Structure
1. **Define global parameters** (all dimensions listed above)
2. **Create base perimeter frame sketch** (100×100 outer wall rectangle with 1.5mm thick walls (outer edge at 100mm, inner edge at 98.5mm), includes tab/slot geometry as protrusions and recesses in the 2D profile; tabs add to wall thickness and extend 2mm beyond 100mm boundary for absolute dimensions of 102×102mm)
3. **First extrusion (Z=0 to Z=3):**
   - Extrude perimeter frame with tabs/slots (3mm extrusion)
   - Create interior cylinders (100 separate body cylinders, Ø7mm outer diameter, 3mm extrusion, positioned at grid locations, intentional empty space between cylinders for lightweight design)
4. **Second extrusion (Z=3 to Z=6):**
   - Create top layer (3mm thick solid layer covering entire area, unites all cylinders and perimeter into final single solid part)
   - Extend tabs/slots through top layer (tabs and slots continue from first extrusion for total height Z=0→6)
5. **Create interior through-holes** (100 holes, Ø4mm, 6mm deep total: penetrating cylinders Z=0→3 and continuing through top layer Z=3→6)

### Key Scripting Considerations
- Use **arrays/patterns** for repetitive features
- Implement **hole feature API** for through-holes (Ø4mm, 6mm deep: 3mm through cylinder + 3mm through top layer)
- Model the **two-extrusion structure**: 
  - **First extrusion (Z=0→3):**
    - Perimeter walls sketch (1.5mm thick, outer edge at 100mm, inner edge at 98.5mm) with tabs/slots as part of 2D profile
    - Tabs add to wall thickness and extend 2mm beyond 100mm wall boundary (radius of Ø4mm half-cylinder, absolute dimensions 102×102mm)
    - Perimeter and tabs/slots extrusion (3mm Z=0→3)
    - Cylinders (Ø7mm outer diameter, initially separate bodies, 3mm extrusion Z=0 to Z=3)
    - Intentional empty space between cylinders from Z=0→3 for lightweight design (no material infill)
  - **Second extrusion (Z=3→6):**
    - Top layer (3mm thick solid covering entire area, 3mm extrusion Z=3 to Z=6)
    - Tabs/slots continue through top layer (total height Z=0→6)
    - Unites all components into final single solid part
- **Half-cylinder geometry** for edge features: integrate into perimeter wall 2D sketch profile before extrusion (tabs add to wall thickness)
- Include **parameter validation** (e.g., spacing > hole diameter, cylinder_dia > hole_dia)
- **Grid positioning:** First hole at (5, 5), last hole at (95, 95) maintains 5mm clearance from all wall edges
- **Edge feature positioning:** Tabs/slots start at 10mm from corners, integrated into perimeter wall sketch, tabs add to wall thickness and extend 2mm beyond 100mm wall boundary (absolute dimensions 102×102mm), no features at corners
- **Final result:** Single unified solid part after top layer unites all components (Z=3→6)
- Add **comments** documenting each feature group purpose

### Flexibility Parameters
Consider making these adjustable:
- Plate dimensions (length, width, total thickness 6mm)
- Top layer extrusion height (currently 3mm, Z=3 to Z=6)
- Perimeter wall thickness (currently 1.5mm inward projection, 3mm extrusion Z=0 to Z=3)
- Cylinder extrusion height (currently 3mm, Z=0 to Z=3)
- Grid resolution (rows, columns)
- Grid spacing (currently 10mm)
- First hole offset (currently 5mm from edges, creates equal clearance on all sides)
- Interior hole diameter (Ø4mm)
- Cylinder outer diameter (Ø7mm)
- Edge tab/slot diameter (Ø4mm)
- Edge feature count and spacing (currently 9 per edge, 10mm spacing, starting 10mm from corners)
