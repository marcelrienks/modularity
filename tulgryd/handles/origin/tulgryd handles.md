# tulgryd handles - Detailed 3D Model Analysis

## Overall Dimensions

### Bounding Box

- **Parametric Base (Default Values):**
  - **Handle diameter:** 26.00 mm (primary driving parameter)
  - **Base height/Total extrusion:** 33.00 mm (handle_height parameter)
  - **Base dimensions:** Square footprint derived from grip outer dimensions
  - **Grip structure:** Hollow cylinder (3mm walls) with open front
  - **Wall thickness:** 3.0 mm (constant on sides and top)
  - **Grip slope:** 25 degrees backward (constant, non-parametric)
  - **Mounting holes:** 4.5mm through-all + 7.5mm countersunk

### Base Geometry

- **Shape:** Square prism with solid construction (except mounting holes)
- **Origin:** Corner at (0, 0, 0)
- **Footprint:** Square derived from grip outer dimensions (handle_radius + 3mm offset on each side)
- **Base structure:** Solid throughout
- **Mounting interface:** Two concentric through-holes at center for tile attachment
- **Corner geometry:** All surfaces chamfered (1.3mm radius) except grip-to-base join
- **Bottom surface:** Flat, rests against tile mounting surface

### Grip Geometry

- **Shape:** Hollow cylindrical grip with 3mm walls, open front
- **Diameter:** Equal to handle_diameter (26.00 mm default)
- **Radius:** handle_diameter / 2 (13.00 mm)
- **Outer wall radius:** handle_radius + 3.0 mm (16.00 mm for 26mm diameter)
- **Height:** Determined by handle_height parameter (33.00 mm default)
- **Wall thickness:** 3.0 mm (applied to left side, right side, and top wall only)
- **Wall structure:** 4-section after shelling:
  - **Front:** Open (no wall - ergonomic grip access)
  - **Left side:** 3mm wall
  - **Right side:** 3mm wall
  - **Top:** 3mm wall
  - **Interior:** Hollow cavity sized for comfortable hand grip
- **Slope angle:** **25 degrees** (hardcoded, constant for ergonomic backward lean)
- **Slope direction:** Tilts backward away from open front face
- **Chamfer:** 1.3mm radius applied to all edges (including large hole lip)

---

## Feature Analysis

### Base Section

#### Geometry
- **Type:** Square prism, solid construction
- **Dimensions:** Square footprint × 33mm height (determined by handle_height parameter)
- **Position:** Z = -33 to Z = 0 (extends downward from grip base)
- **Surface:** Flat bottom for tile mounting, tapers to grip section above
- **Footprint origin:** Derived from grip dimensions (radius + 3mm wall offset)

#### Structural Characteristics
- **Solid:** No internal hollow structure (except mounting holes)
- **All surfaces chamfered:** 1.3mm radius except at grip transition
- **Mounting interface:** Center-mounted attachment points (two concentric holes)

### Mounting Holes

#### Hole 1 (Small - Through-All Primary Mount)
- **Diameter:** 4.5 mm (hardcoded, non-parametric)
- **Type:** Through-hole (pierces entire model from bottom base to top grip)
- **Position:** Center of square base
- **Coordinates:** (handle_diameter/2, handle_diameter/2, Z = -33 to Z = +top_surface)
- **Extrusion:** Through entire model height (base + grip)
- **Depth:** Full model height
- **Purpose:** Primary mounting point for tile attachment system
- **Compatibility:** Designed to mate with tulgryd tile 4.5mm mounting points

#### Hole 2 (Large - Countersunk Secondary Mount)
- **Diameter:** 7.5 mm (hardcoded, non-parametric)
- **Type:** Countersunk through-hole (extrudes upward through top section only)
- **Position:** Center of square base (concentric with Hole 1)
- **Coordinates:** (handle_diameter/2, handle_diameter/2)
- **Extrusion method:** Upward through top grip section with 4.5mm offset
- **Creates:** Beveled lip protruding 4.5mm above top surface
- **Chamfer:** 1.3 mm chamfered edge on lip perimeter
- **Spatial relationship:** Overlaps concentrically with Hole 1
- **Purpose:** Alternative/secondary mounting for flexible tile connection options
- **Compatibility:** Designed to mate with tulgryd tile 7.5mm mounting points

### Grip Section

#### Cylindrical Hollow Structure
- **Construction method:** 
  1. Create circular sketch (radius = handle_diameter/2) with wall boundaries
  2. Extrude half-section with 25° backward tilt to handle_height
  3. Mirror across vertical axis through center to create full grip
  4. Shell operation: 3mm walls (remove front, keep sides and top)
- **Diameter:** handle_diameter (26.00 mm)
- **Radius:** handle_diameter / 2 (13.00 mm)
- **Height:** handle_height (33.00 mm)
- **Wall thickness:** 3.0 mm (constant on all remaining walls after shell)

#### Grip Architecture After Shelling
- **Front face:** Open (removed during shell operation)
- **Left wall:** 3mm thickness
- **Right wall:** 3mm thickness
- **Top wall:** 3mm thickness
- **Interior cavity:** Hollow space for ergonomic hand grip
- **Wall edge offset:** Interior walls positioned at (radius - 3mm) from centerline
- **Outer edge offset:** Outer walls positioned at (radius + 3mm) from centerline

#### Ergonomic Tilt and Orientation
- **Tilt angle:** 25 degrees backward (constant, not parameter-dependent)
- **Tilt axis:** Vertical axis through handle_diameter midpoint (Y-axis traditional)
- **Tilt direction:** Backward away from open front (tilts away from the open face)
- **Effect:** Creates natural wrist position when holding tool, reduces strain
- **Reference point:** Bottom of model serves as vertical reference for tilt calculation

#### Grip-to-Base Transition
- **Connection type:** Solid union of grip bottom to base top
- **Surface texture:** Sharp 90-degree edge (no fillet between grip and base)
- **Chamfers elsewhere:** 1.3mm radius chamfers on all other edges for safety and appearance

---

## Parameterization Guidelines

### Primary Parameters (User-Input Only)

#### Handle Diameter - Primary Scaling Parameter
```
handle_diameter = 26.0              // mm (default)
                                    // Controls: grip diameter, base proportions, wall positions
                                    // Range: 15mm - 50mm (practical grip sizes)
                                    // Used in: All dimension calculations
```

**Derived from handle_diameter:**
- `grip_radius` = handle_diameter / 2
- `outer_wall_radius` = grip_radius + 3.0mm
- `base_footprint` = square sized to accommodate outer walls

#### Handle Height - Secondary Scaling Parameter
```
handle_height = 33.0                // mm (default)
                                    // Controls: total extrusion distance (base goes down, grip goes up)
                                    // Range: 20mm - 60mm (practical reach)
                                    // Independent: Does NOT scale with handle_diameter
```

**Used in:**
- Base extrusion distance (downward from grip base)
- Grip extrusion height (upward from origin)

### Hardcoded Parameters (Non-Parametric - Fixed Constants)

```
slope_angle = 25.0                  // degrees (backward ergonomic tilt)
                                    // Reason: Design intent for grip comfort
                                    // Never adjustable - constant design element

wall_thickness = 3.0                // mm (shelled grip walls)
                                    // Applied to: left, right, and top walls after shelling
                                    // Never adjustable - structural design

grip_edge_offset = 3.0              // mm (distance from diameter circle to inner wall)
                                    // Calculation: inner_wall_radius = radius - 3.0mm
                                    // Calculation: outer_wall_radius = radius + 3.0mm
                                    // Never adjustable - proportional design element

small_hole_diameter = 4.5           // mm (through-all mounting hole)
                                    // Reason: Tile attachment system compatibility
                                    // Never adjustable - system integration

large_hole_diameter = 7.5           // mm (countersunk mounting hole)
                                    // Reason: Tile attachment system compatibility
                                    // Never adjustable - system integration

large_hole_offset = 4.5             // mm (upward extrusion creating countersink lip)
                                    // Creates: 4.5mm tall countersunk mount point
                                    // Never adjustable - mounting system design

chamfer_radius = 1.3                // mm (all edge chamfers)
                                    // Applied to: All edges except grip-base junction
                                    // Never adjustable - safety and aesthetic feature
```

### Derived Relationships

```
// Primary calculations from handle_diameter
grip_radius = handle_diameter / 2                           // 13.0mm for 26mm diameter
outer_wall_radius = grip_radius + grip_edge_offset          // 16.0mm for 26mm diameter
inner_wall_radius = grip_radius - grip_edge_offset          // 10.0mm for 26mm diameter

// Base geometry
base_center_x = handle_diameter / 2                         // 13.0mm
base_center_y = handle_diameter / 2                         // 13.0mm
base_footprint = "square derived from outer walls"

// Grip height calculation
grip_top_height = handle_height                             // 33.0mm (extrudes upward)
base_bottom_depth = handle_height                           // 33.0mm (extrudes downward)

// Mounting holes (both at base center)
hole_1_diameter = 4.5                                       // mm (constant)
hole_2_diameter = 7.5                                       // mm (constant)
hole_center_x = handle_diameter / 2                         // 13.0mm
hole_center_y = handle_diameter / 2                         // 13.0mm

// Countersunk feature
countersink_height = large_hole_offset                      // 4.5mm above top surface
countersink_chamfer = chamfer_radius                        // 1.3mm bevel radius
```

---

## Construction Workflow (Fusion 360 Based)

### Step 1: Create Sketch
- Origin: Center of handle_diameter circle
- Define circular profile at radius = handle_diameter / 2
- Define wall boundaries:
  - Inner radius = handle_radius - 3.0mm
  - Outer radius = handle_radius + 3.0mm

### Step 2: Half-Grip Extrusion
- Profile: Half of circular sketch (one side)
- Direction: Upward (+Z)
- Distance: handle_height
- Tilt: 25 degrees backward (away from open front)
- Result: Half-cylindrical grip section

### Step 3: Mirror to Full Grip
- Operation: Mirror around vertical axis
- Axis: Vertical line through handle_diameter circle center
- Result: Complete cylindrical grip (two halves united)

### Step 4: Shell Operation
- Operation: Hollow out
- Remove faces: Front face (facing -Y direction)
- Keep faces: Left, right, and top walls
- Wall thickness: 3.0mm on remaining walls
- Result: Hollow grip with 4-wall structure

### Step 5: Base Extrusion
- Profile: Square base derived from grip outer footprint
- Direction: Downward (-Z)
- Distance: handle_height
- Result: Square base prism extending downward

### Step 6: Create Through-Holes
- **Small hole (4.5mm):** Through entire model (base to grip top)
- **Large hole (7.5mm):** Through top section only, with 4.5mm offset upward
- Location: Both centered at (handle_diameter/2, handle_diameter/2)
- Result: Two concentric mounting holes

### Step 7: Chamfer All Edges
- Chamfer radius: 1.3mm
- Applied to: All edges throughout model
- Exception: Sharp edge at grip-to-base junction
- Result: Smoothed edges for safety and ergonomics

### Step 8: Boolean Union
- Operation: Combine all bodies
- Components: Base + grip + mounting holes
- Result: Single unified solid body

---

## Design Intent & Functional Analysis

### Purpose

This is a **modular tool handle** designed to attach to tulgryd tiles for organized toolbox storage. The design provides:
- Comfortable hollow grip for extended use
- Ergonomic 25-degree backward tilt reducing wrist strain
- Secure mounting to modular tulgryd tile system via dual mounting holes
- Scalable parametric design for different tool types and hand sizes
- Lightweight hollow structure optimizing material usage

### Assembly Strategy

#### Base Mounting
- Solid square base with two concentric attachment holes
- Small hole (4.5mm): Primary mounting to standard tile points
- Large hole (7.5mm): Alternative mounting or dual-point security
- Both holes centered for symmetric, stable mounting

#### Grip Assembly
- Hollow cylindrical grip with 3mm structural walls
- Open front allows comfortable hand positioning
- 25-degree backward tilt for ergonomic hand position
- Centered on base for balanced tool handling

#### Integration with Tiles
- Handles mount to tulgryd tiles via base holes
- Allows tool attachment and storage in modular drawers
- Multiple handles can be mounted on single tile for organized tool sets
- Hole sizing ensures compatibility with tile mounting system

### Scalability Through Parameters

The model supports parametric sizing:
- **Small handles:** 15-20mm diameter for precision tools
- **Standard handles:** 25-30mm diameter (like the 26mm default)
- **Large handles:** 35-50mm diameter for leverage tools
- **Custom heights:** 20-60mm range allows tool-specific proportions
- **Constant elements:** Slope angle, wall thickness, hole sizes remain fixed

---

## Manufacturing Considerations

This document describes the geometric model only. No specific material properties, manufacturing processes, tolerances, or production methods are specified or required for this geometric definition.

### Feature Specifications for Manufacturing
- **Small hole:** 4.5mm diameter through-hole (full depth)
- **Large hole:** 7.5mm diameter through-hole (partial, with 4.5mm offset creating countersink)
- **Hole positions:** Both centered on base
- **Clearance:** Holes maintain adequate spacing from base edges
- **Chamfer:** 1.3mm radius on all edges except grip-base junction
- **Wall thickness:** 3mm consistent throughout grip (after shelling)
- **Tolerance class:** Standard 3D printing or CNC machining

---

## Verification Checklist

For recreating this model parametrically, verify:

- [ ] Primary parameter: handle_diameter = 26.0 mm (adjustable: 15-50mm range)
- [ ] Primary parameter: handle_height = 33.0 mm (adjustable: 20-60mm range)
- [ ] Derived: Grip radius = handle_diameter / 2 (13.0 mm)
- [ ] Derived: Outer wall radius = grip_radius + 3.0mm (16.0 mm)
- [ ] Derived: Inner wall radius = grip_radius - 3.0mm (10.0 mm)
- [ ] Hardcoded: Slope angle = 25 degrees (constant for ergonomic lean)
- [ ] Hardcoded: Wall thickness = 3.0mm (constant shelled walls)
- [ ] Hardcoded: Grip edge offset = 3.0mm (constant wall positioning)
- [ ] Hardcoded: Small hole diameter = 4.5 mm (constant, through-all)
- [ ] Hardcoded: Large hole diameter = 7.5 mm (constant, countersunk)
- [ ] Hardcoded: Large hole offset = 4.5 mm (constant, creates lip)
- [ ] Hardcoded: Chamfer radius = 1.3 mm (constant, all edges)
- [ ] Base geometry: Square prism with solid construction
- [ ] Base bottom surface: Flat, rests on tiles (Z=-33 position)
- [ ] Grip geometry: Hollow cylinder with 3 walls (front open)
- [ ] Grip height: equals handle_height parameter (33.0 mm)
- [ ] Grip slope: exactly 25 degrees backward from vertical (away from open front)
- [ ] Grip structure: 4-section walls after shelling (front open, left/right/top walls remain)
- [ ] Mounting holes: Both positioned at center (handle_diameter/2, handle_diameter/2)
- [ ] Small hole (4.5mm): Through-hole from base bottom through grip top
- [ ] Large hole (7.5mm): Through-hole through top section only (4.5mm offset upward)
- [ ] Countersink feature: 7.5mm hole creates 4.5mm tall lip with 1.3mm chamfer
- [ ] Holes do not overlap: Both concentric at same center point
- [ ] Grip-to-base transition: Union at Z=0 with sharp 90° edge (no fillet)
- [ ] Edge chamfers: 1.3mm radius on all surfaces except grip-base junction
- [ ] Model structure: Single unified solid body after all operations
- [ ] Mounting compatibility: Hole sizing matches tulgryd tile attachment system
- [ ] Ergonomic slope: 25-degree angle tilts away from open front for comfortable use
- [ ] Scalability: Can reproduce with different handle_diameter and handle_height values

---

## Notes for Parametric Script Development

### Recommended Script Structure

```
1. Define input parameters
   - handle_diameter = 26.0 (user input: range 15-50)
   - handle_height = 33.0 (user input: range 20-60)

2. Define hardcoded constants
   - slope_angle = 25.0
   - wall_thickness = 3.0
   - grip_edge_offset = 3.0
   - small_hole_diameter = 4.5
   - large_hole_diameter = 7.5
   - large_hole_offset = 4.5
   - chamfer_radius = 1.3

3. Calculate derived dimensions
   - grip_radius = handle_diameter / 2
   - outer_wall_radius = grip_radius + grip_edge_offset
   - inner_wall_radius = grip_radius - grip_edge_offset
   - base_center_x = handle_diameter / 2
   - base_center_y = handle_diameter / 2
   - hole_center_x = handle_diameter / 2
   - hole_center_y = handle_diameter / 2

4. Create base sketch
   - Circular profile (radius = grip_radius)
   - Wall boundary circles at inner and outer radii

5. Create half-grip extrusion
   - Extrude half-sketch upward
   - Height = handle_height
   - Tilt = 25 degrees backward (away from +Y direction)

6. Mirror half-grip
   - Mirror across vertical axis through center
   - Result: Complete cylindrical grip

7. Shell the grip
   - Remove front face (Y-facing surface)
   - Keep 3mm walls on remaining surfaces

8. Extrude base downward
   - Square profile from grip footprint
   - Extrude downward by handle_height distance

9. Create small through-hole
   - Diameter = 4.5mm
   - Through entire model

10. Create large countersunk hole
   - Diameter = 7.5mm
   - Partial depth with 4.5mm offset upward
   - Chamfer = 1.3mm on top edge

11. Chamfer all edges
   - Radius = 1.3mm
   - Exception: Skip grip-base junction

12. Boolean union
   - Combine all bodies into single solid

13. Output final solid body
```

### Key Scripting Considerations

- **Primary driver:** handle_diameter scales grip and base proportionally
- **Independent parameter:** handle_height controls extrusion distances (base down, grip up)
- **Hardcoded constants:** All fixed values must never change (25°, 3.0mm, hole sizes, etc.)
- **Shell operation:** Critical step - removes front, keeps 3 walls for hollow grip
- **Mirror pattern:** Essential for creating symmetric full grip from half-extrusion
- **Hole concentric positioning:** Both holes at same center point for stacked mounting
- **Countersink feature:** Large hole offset + chamfer creates beveled lip
- **Chamfer exceptions:** Apply 1.3mm radius everywhere except grip-base sharp edge
- **Scaling behavior:** As handle_diameter increases, all proportions scale; grip walls remain 3mm
- **Height independence:** handle_height change affects extrusion depth, NOT grip proportions

### Validation in Script

Implement validation to ensure:
```
1. handle_diameter >= 15 AND <= 50
2. handle_height >= 20 AND <= 60
3. slope_angle == 25.0
4. wall_thickness == 3.0
5. grip_edge_offset == 3.0
6. small_hole_diameter == 4.5
7. large_hole_diameter == 7.5
8. large_hole_offset == 4.5
9. chamfer_radius == 1.3
10. grip_radius == handle_diameter / 2
11. outer_wall_radius == grip_radius + 3.0
12. inner_wall_radius == grip_radius - 3.0
13. Both holes positioned at (diameter/2, diameter/2)
14. Grip-to-base edge has NO fillet (sharp 90°)
15. All other edges have 1.3mm chamfer
```

### Relationship to Tiles System

The tulgryd system consists of:

| Component | Tiles | Handles |
|-----------|-------|---------|
| **Purpose** | Grid mounting surface | Removable tools |
| **Dimensions** | 100×100mm base | Parametric (26mm default) |
| **Interior grid** | 10×10 Ø4mm holes | 2 mounting holes (4.5mm + 7.5mm) |
| **Structure** | Perimeter walls + cylinders | Hollow grip + solid base |
| **Mounting system** | 100 grid holes | 2 concentric holes at center |
| **Height** | 6mm plate | 33+mm total (base down + grip up) |
| **Parameterization** | ~15 parameters | 2 primary parameters + 7 hardcoded |
| **Integration** | Standalone grid | Attaches to tiles via holes |

---

## Parameter Reference Card

```
PARAMETRIC (Adjustable by User)
├─ handle_diameter = 26.0 mm (default, range: 15-50mm)
│  └─ Controls grip diameter, base size, all proportional dimensions
└─ handle_height = 33.0 mm (default, range: 20-60mm)
   └─ Controls total extrusion distance (base down + grip up)

HARDCODED (Fixed Constants - Never Change)
├─ slope_angle = 25.0 degrees (ergonomic backward tilt)
├─ wall_thickness = 3.0 mm (shelled grip walls)
├─ grip_edge_offset = 3.0 mm (wall positioning offset)
├─ small_hole_diameter = 4.5 mm (primary mounting through-hole)
├─ large_hole_diameter = 7.5 mm (secondary countersunk hole)
├─ large_hole_offset = 4.5 mm (countersink lip height)
└─ chamfer_radius = 1.3 mm (edge smoothing except grip-base)

DERIVED (Calculated from Primary Parameters)
├─ grip_radius = handle_diameter / 2
├─ outer_wall_radius = grip_radius + 3.0
├─ inner_wall_radius = grip_radius - 3.0
├─ base_center = [diameter/2, diameter/2]
└─ hole_center = [diameter/2, diameter/2]

STRUCTURE OVERVIEW
├─ Base (extends downward by handle_height)
│  └─ Solid square prism with 2 concentric holes at center
├─ Grip (extends upward by handle_height with 25° tilt)
│  ├─ Hollow cylinder: 3mm walls on left, right, top
│  ├─ Open front face (for hand grip access)
│  └─ All edges chamfered 1.3mm (except grip-base junction)
└─ Mounting holes (at base center, concentric)
   ├─ Small: 4.5mm through-all
   └─ Large: 7.5mm partial with 4.5mm offset + 1.3mm chamfer lip
```
