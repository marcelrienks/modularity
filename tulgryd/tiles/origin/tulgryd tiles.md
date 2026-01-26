# tulgryd tiles - Detailed 3D Model Analysis

## Overall Dimensions

### Bounding Box
- **Perimeter walls outer edge:** 100.00 mm × 100.00 mm (excluding tabs)
- **Absolute dimensions (including tabs):** 103.80 mm × 104.00 mm
  - Tabs extend 1.90 mm beyond the 100mm wall boundary on top and right edges (R1.9mm)
  - Slots extend 2.00 mm inward from the 0mm boundary on bottom and left edges (R2.0mm)
- **Height (Z-axis):** 6.00 mm (total thickness)
  - **First extrusion (Z=0 to Z=3.5):**
    - Perimeter walls: 2.0mm thick (outer edge at 100mm, inner edge at 98mm)
    - Tabs: Ø3.8mm half-cylindrical protrusions (R1.9mm extends beyond 100mm wall boundary)
    - Slots: Ø4.0mm half-cylindrical recesses (R2.0mm cuts into perimeter wall)
    - Cylinders: Ø7mm separate bodies
  - **Second extrusion (Z=3.5 to Z=6):**
    - Top layer: 2.50 mm solid layer covering entire area
    - Tabs continue through top layer (total height Z=0→6)
    - Slots continue through top layer (total depth Z=0→6)
  - **Final result:** Single unified solid body

### Base Geometry
- **Shape:** Rectangular plate/panel
- **Origin:** Corner at (0, 0, 0)
- **Maximum extent:** (100, 100, 6) mm (perimeter boundary, excluding tabs which extend to 103.8mm on top/right)
- **Bottom surface:** Open structure - only perimeter walls and Ø7mm cylinder bases contact the resting surface (no solid base plate between cylinders)
- **Corner geometry:** Sharp 90-degree corners with no fillets, chamfers, or additional geometry
- **Slot recesses:** Bottom and left edges have R2.0mm (Ø4mm) semi-circular cutouts that define the edge profile

---

## Feature Pattern Analysis

The model contains **100 interior through-holes** (10×10 main grid) and **36 edge interlocking features** (18 tabs + 18 slots).

### Interior Grid: Ø4mm Through-Holes
- **Quantity:** 100 holes (10×10 pattern)
- **Diameter:** 4.0 mm (2.0 mm radius)
- **Cylinder structure:** Each hole is centered within a Ø7.0mm cylinder (united by top layer)
- **Pattern:** 10×10 regular grid with 10mm spacing
- **Grid Spacing:** 10 mm (center-to-center)
- **First hole center:** 5 mm from left edge (X), 5 mm from bottom edge (Y)
- **Last hole center:** 95 mm from left edge (X), 95 mm from bottom edge (Y) - maintains 5mm clearance from all edges
- **X Positions:** 5, 15, 25, 35, 45, 55, 65, 75, 85, 95 mm (10 positions)
- **Y Positions:** 5, 15, 25, 35, 45, 55, 65, 75, 85, 95 mm (10 positions)
- **Z Position:** 0 to 6 mm (through entire tile thickness)
- **Hole depth:** 6 mm total (3.5mm through cylinder Z=0→3.5, 2.5mm through top layer Z=3.5→6)
- **Cylinder Details:**
  - Each Ø7mm cylinder (Z=0 to Z=3.5) is a 3.5mm extrusion from bottom surface
  - Ø4mm through-hole penetrates cylinder (Z=0→3.5) and continues through top layer (Z=3.5→6)
  - Top layer (Z=3.5 to Z=6) sits flush above cylinders and unites them into single solid body
  - Bottom view: Empty space exists between/around Ø7mm cylinder bases from Z=0→3.5 (cylinders occupy only their Ø7mm footprint, remainder is empty space with no material infill)
  - The bottom surface of cylinders and perimeter walls form the resting surface of the tile

## Edge Interlocking Features (Tabs & Slots)

### Tab Features: Ø3.8mm Half-Cylindrical Extrusions (Top & Right Edges)
- **Quantity:** 18 tabs total
  - **Right edge (X=100):** 9 tabs
  - **Top edge (Y=100):** 9 tabs
- **Diameter:** 3.8 mm (1.9 mm radius)
- **Geometry:** 180-degree cylindrical arc with center positioned directly on the outer edge of the tile wall, radius protruding outward 1.9mm from the wall edge
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
- **Geometry:** 180-degree cylindrical arc cutout with center positioned directly on the outer edge of the tile wall (X=0 or Y=0), radius cutting 2.0mm inward into the wall material
- **Pattern:** L-shaped arrangement along bottom and left edges
- **Positions:**
  - **Left edge (X=0):** 9 slots at Y = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
  - **Bottom edge (Y=0):** 9 slots at X = 10, 20, 30, 40, 50, 60, 70, 80, 90 mm
- **Spacing:** 10 mm (center-to-center)
- **Z Position:** 0 to 6 mm (6mm extrusion through full tile height)
- **Depth:** 6 mm (full plate thickness)
- **Note:** These slots receive the tabs from adjacent tiles, enabling tile-to-tile connection. Slot centers are located at the edge boundary (X=0 or Y=0), cutting into the tile material.

---

## Parameterization Guidelines

### Primary Parameters for Scripting

#### Base Plate
```
plate_length = 100.0              // mm (X-axis outer perimeter)
plate_width = 100.0               // mm (Y-axis outer perimeter)
plate_thickness = 6.0             // mm (Z-axis)
perimeter_wall_thickness = 2.0    // mm
perimeter_wall_extrusion = 3.5    // mm (Z=0 to Z=3.5)
cylinder_extrusion = 3.5          // mm (Z=0 to Z=3.5)
top_layer_extrusion = 2.5         // mm (Z=3.5 to Z=6)
tab_extrusion = 6.0               // mm (full height Z=0→6)
```

#### Interior Grid Holes
```
interior_grid_rows = 10
interior_grid_cols = 10
interior_grid_spacing = 10.0      // mm
interior_grid_offset_x = 5.0      // mm (first hole from left edge)
interior_grid_offset_y = 5.0      // mm (first hole from bottom edge)
interior_hole_dia = 4.0           // mm
interior_cylinder_dia = 7.0       // mm
interior_hole_depth = 6.0         // mm (full thickness)
```

#### Edge Slots - Bottom/Left (X=0, Y=0)
```
edge_slot_count = 9               // per edge
edge_slot_spacing = 10.0          // mm
edge_slot_start_offset = 10.0     // mm (first slot at 10mm)
edge_slot_dia = 4.0               // mm (R2.0mm per drawing)
edge_slot_radius = 2.0            // mm
edge_slot_depth = 6.0             // mm
```

#### Edge Tabs - Top/Right (X=100, Y=100)
```
edge_tab_count = 9                // per edge
edge_tab_spacing = 10.0           // mm
edge_tab_start_offset = 10.0      // mm (first tab at 10mm)
edge_tab_dia = 3.8                // mm (R1.9mm per drawing)
edge_tab_radius = 1.9             // mm
edge_tab_height = 6.0             // mm
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
- Multiple tiles can be connected to cover custom areas for toolbox drawer organization

### Assembly Strategy

#### Interior Grid
- 10×10 array provides 100 mounting points for tool-holding attachments
- Ø7mm cylinders united by top layer into final single solid body
- Intentional empty space between cylinders for lightweight design

#### Edge Interlocking System
- **Bottom/Left edges:** Slots receive tabs from adjacent tiles
- **Top/Right edges:** Tabs insert into adjacent tile slots
- **Corners:** No features at corners - connection via edge features only
- Tiles connect in any direction to form custom layouts 

---

## Manufacturing Considerations

This document describes the geometric model only. No specific material properties, manufacturing processes, tolerances, or production methods are specified or required for this geometric definition.

---

## Verification Checklist

For recreating this model parametrically, verify:

- [ ] Perimeter wall thickness: 2.0mm (outer edge at 100mm, inner edge at 98mm), 3.5mm extrusion (Z=0 to Z=3.5)
- [ ] Perimeter walls outer edge: 100×100 mm (wall boundary), inner edge at 98×98 mm
- [ ] Tabs extend 1.9mm beyond 100mm wall boundary (R1.9 = Ø3.8mm, absolute dimensions 103.8mm on top/right edges)
- [ ] Cylinder structure: 100 Ø7mm cylinders, 3.5mm extrusion Z=0 to Z=3.5
- [ ] Top layer: 2.5mm extrusion (Z=3.5 to Z=6) unites cylinders and perimeter walls into final single solid body
- [ ] Intentional empty space: Between/around cylinders from Z=0→3.5 for lightweight design (no material infill except cylinder and perimeter footprints)
- [ ] Bottom surface: Open structure with only perimeter walls and cylinder bases forming resting surface (no solid base plate)
- [ ] Interior grid: 10×10 holes, 10mm spacing, first hole at (5,5), last hole at (95,95)
- [ ] Interior holes maintain 5mm clearance from all edges
- [ ] Total interior through-holes: 100 Ø4.0mm holes
- [ ] Interior through-holes: Ø4.0mm (6mm deep: 3.5mm through cylinder + 2.5mm through top layer)
- [ ] Each cylinder has Ø4mm through-hole penetrating cylinder (Z=0→3.5) continuing through top layer (Z=3.5→6)
- [ ] Bottom edge (Y=0): 9 slots (180° arc cutouts, center at Y=0 edge boundary, R2.0mm cutting inward), 10mm spacing, X positions: 10,20,30,40,50,60,70,80,90
- [ ] Left edge (X=0): 9 slots (180° arc cutouts, center at X=0 edge boundary, R2.0mm cutting inward), 10mm spacing, Y positions: 10,20,30,40,50,60,70,80,90
- [ ] Top edge (Y=100): 9 tabs (180° arc, center on Y=100 outer wall edge, R1.9mm extending outward), extend through full height Z=0→6, 10mm spacing, X positions: 10,20,30,40,50,60,70,80,90
- [ ] Right edge (X=100): 9 tabs (180° arc, center on X=100 outer wall edge, R1.9mm extending outward), extend through full height Z=0→6, 10mm spacing, Y positions: 10,20,30,40,50,60,70,80,90
- [ ] Tabs: Ø3.8mm (R1.9mm), slots: Ø4.0mm (R2.0mm) - provides 0.1mm clearance per side for fit tolerance
- [ ] Tabs and slots integrated into perimeter wall sketch profile, extend through full tile height (Z=0→6)
- [ ] Corners: Sharp 90° corners with no interlocking features, fillets, or chamfers at (0,0), (100,0), (0,100), (100,100)

---

## Notes for Parametric Script Development

### Recommended Script Structure
1. **Define global parameters** (see values above)
2. **Create base perimeter frame sketch** (includes tab/slot geometry in 2D profile)
   - Perimeter walls: 2mm thick, outer edge at 100×100mm, inner edge at 98×98mm
   - Tabs on top/right edges: Ø3.8mm (R1.9mm) half-circles extending outward from X=100/Y=100
   - Slots on bottom/left edges: Ø4.0mm (R2.0mm) half-circles with centers at X=0/Y=0, cutting into tile material
3. **First extrusion (Z=0 to Z=3.5):**
   - Extrude perimeter frame with tabs/slots (3.5mm height)
   - Create 100 interior Ø7mm cylinders at grid locations (10×10 pattern)
4. **Second extrusion (Z=3.5 to Z=6):**
   - Create top layer 2.5mm thick (unites all components into single solid body)
   - Extend tabs/slots through top layer to full 6mm height
5. **Create interior through-holes:**
   - 100 Ø4mm holes penetrating full 6mm depth (10×10 pattern at 5,15,25...95)

### Key Scripting Considerations
- Use **arrays/patterns** for repetitive features (10×10 main grid, 9×4 edge features)
- Implement **hole feature API** for through-holes (100 Ø4mm holes)
- Model the **two-layer extrusion structure** (perimeter walls and cylinders at Z=0→3.5, then top layer at Z=3.5→6 unites all)
- **Tab geometry:** 180° arc with center on outer wall edge (X=100/Y=100), R1.9mm (Ø3.8mm) extending outward
- **Slot geometry:** 180° arc cutout with center at edge boundary (X=0/Y=0), R2.0mm (Ø4.0mm) cutting inward into wall material
- **Tab/Slot mismatch:** Tabs are Ø3.8mm, slots are Ø4.0mm (0.2mm clearance per side for fit tolerance)
- Include **parameter validation** (spacing > hole diameter, cylinder_dia > hole_dia, slot_dia > tab_dia for clearance)
- Add **comments** documenting feature groups

### Flexibility Parameters
Consider making these adjustable:
- Plate dimensions (length, width, thickness)
- Layer extrusion heights (perimeter, cylinder, top layer)
- Wall thickness
- Grid resolution and spacing
- Hole offset from edges
- Hole and cylinder diameters
- Edge tab/slot diameter and spacing
