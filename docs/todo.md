# OpenSCAD Toolgrid Generator V2 - Code Review & Improvements

**Review Date**: December 21, 2024  
**Script**: `toolgrid-generator-v2.scad` (322 lines)

---

## 🔴 CRITICAL BUGS - MUST FIX

### 1. Line 81: Incorrect Dimension Calculation
**Issue**: Uses `num_cols` instead of `num_rows` for length calculation  
**Current Code**:
```openscad
r_length = drawer_length%(num_cols * hole_spacing)+((drawer_length%(num_cols * hole_spacing) > minimum_width)?0:board_width_mm);
```
**Should Be**:
```openscad
r_length = drawer_length%(num_rows * hole_spacing)+((drawer_length%(num_rows * hole_spacing) > minimum_width)?0:board_width_mm);
```
**Impact**: 🔴 Drawer layout completely fails for non-square tile configurations. Edge tiles calculated with wrong dimensions.  
**Priority**: P0 - Fix before any releases  
**Testing**: Test drawer mode with different row/column counts (e.g., 4x16, 8x12, 16x8)

---

### 2. Lines 89-90: Dead Code - Unused Functions
**Issue**: Functions `w_reduce()` and `l_reduce()` defined but never called  
**Current Code**:
```openscad
function w_reduce() = (r_width < tab_position.x+tab_diameter && r_length < tab_position.x+tab_diameter && r_width < r_length)?1:0;
function l_reduce() = (r_width < tab_position.x+tab_diameter && r_length < tab_position.x+tab_diameter && r_width >= r_length)?1:0;
```
**Problem**: Variables `w_reduce` and `l_reduce` (lines 80, 82) are used instead. This creates confusion between functions and variables with identical names.  
**Action**: Delete lines 89-90 completely - these functions are never referenced.  
**Priority**: P0  
**Testing**: Search codebase to confirm these functions aren't called anywhere

---

### 3. Line 118: Wrong Variable Reference in lite() Module
**Issue**: Incorrect trim calculation for remainder tiles  
**Current Code** (line 119):
```openscad
trim_w = (drawer?board_width_mm%hole_spacing:trim_width);
```
**Should Be**:
```openscad
trim_w = (drawer?r_width%hole_spacing:trim_width);
```
**Impact**: 🔴 Lite mode (cross-brace structure) doesn't properly align in remainder tiles. May cause geometry misalignment.  
**Priority**: P0  
**Testing**: Generate drawer with lite=true and non-perfect tile fit. Verify cross-braces align with holes.

---

## 🟠 HIGH PRIORITY ISSUES

### 4. Customizer Variable Names - Not User Friendly

**Issue**: Variable names are cryptic and lack clear descriptions for end users.

| Current | Problem | Recommended | Description |
|---------|---------|-------------|-------------|
| `drawer` | Single letter boolean, unclear intent | `print_mode` | Options: "single_tile" / "drawer_grid" |
| `lite` | Vague - what does "lite" mean? | `use_lightweight` | "Enable lightweight mode - thin cross-braces instead of solid" |
| `part` | Single letter, "tiles" vs "connector" unclear | `generate_part` | Options: "tiles" / "connector_only" |
| `label` | Conflicts with qty indicator already added to tiles | `custom_label` | "Optional label for tiles (may conflict with qty indicator)" |
| `minimum_width` | Too abstract | `edge_tile_min_width` | "Minimum width (mm) for edge tiles; narrower remainders discarded" |
| `board_thickness` | OK but vague context | `base_thickness` | "Base board thickness in mm (6mm minimum recommended)" |
| `num_cols` | Should specify "per tile" | `tile_columns` | "Number of hole columns per standard tile (4-16)" |
| `num_rows` | Should specify "per tile" | `tile_rows` | "Number of hole rows per standard tile (4-16)" |
| `hole_diameter` | OK but missing context | `pin_hole_diameter` | "Diameter of tool peg holes in mm" |
| `hole_spacing` | OK but could be clearer | `hole_center_spacing` | "Center-to-center distance between holes (mm)" |
| `lite_thickness` | Missing context | `lightweight_thickness` | "Thickness of cross-braces in lightweight mode (mm)" |
| `web_spacing` | Too cryptic | `lightweight_web_spacing` | "Number of holes between support webs in lightweight mode (4-16)" |
| `tab_diameter` | Unclear what tabs do | `tab_hole_diameter` | "Diameter of interlocking tab holes (mm)" |
| `tab_side` | Cryptic | `tab_offset` | "Distance from edge to tab center (mm)" |
| `tab_clearance` | OK but should clarify direction | `male_tab_clearance` | "Clearance around male tabs (mm) for fit tolerance" |
| `tab_position` | Not user-editable, but poorly named | `tab_positions` | Consider making configurable per user needs |

**Action**: Rename all parameters as above. Update Customizer section headers and add helpful descriptions.  
**Priority**: P1  
**Testing**: Verify all parameters appear correctly in OpenSCAD Customizer with clear descriptions.

---

### 5. Tab Position Hardcoded & Inflexible
**Issue**: Line 62 - `tab_position = [hole_spacing*4, hole_spacing*12];` assumes 16-column tiles  
**Problem**: If user changes `num_cols` to 8 or 4, tabs may be placed outside tile bounds.  
**Current**: Only 2 tabs, at fixed positions (4th hole and 12th hole)  
**Options**:
- Make `tab_position` a customizer parameter (allow users to set)
- Or: Calculate dynamically based on tile size (e.g., quarter and three-quarter points)
- Or: Add validation that warns if tabs exceed bounds  

**Recommended**: Add calculation + validation:
```openscad
// Dynamic tab positioning (quarter and three-quarter points)
tab_positions = [floor(num_cols * hole_spacing / 4), floor(num_cols * hole_spacing * 3 / 4)];
```
**Priority**: P1  
**Testing**: Test with `tile_columns = 4`, `tile_columns = 8`, `tile_columns = 12` - tabs should stay within bounds.

---

### 6. Connector Module Hardcoded Offset
**Issue**: Lines 179-180 use magic number `-10` that doesn't scale  
**Current Code**:
```openscad
module connector() {
    translate([-10,-tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=20);
    translate([-10,tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=20);
}
```
**Problem**: The `-10` offset is unexplained and won't work for all configurations. Should be relative to actual dimensions.  
**Recommendation**: Make offset calculation based on tab hole diameter:
```openscad
module connector() {
    offset = -(tab_diameter * 2);  // Named offset for clarity
    translate([offset,-tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=20);
    translate([offset,tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=20);
}
```
**Priority**: P1  
**Testing**: Verify connector piece dimensions and fit with tab slots.

---

## 🟡 MEDIUM PRIORITY ISSUES

### 7. Typos in Documentation
**Issue**: Lines 2 and 34 contain spelling errors  
**Current**: "Perameters"  
**Should Be**: "Parameters"  
**Lines**: 2, 34  
**Priority**: P2  
**Fix**: Simple find-and-replace.

---

### 8. Inconsistent Code Formatting & Indentation
**Issue**: Mix of tabs and spaces; inconsistent indentation breaks readability  
**Affected Lines**: 
- Lines 104-115 (female tabs section)
- Line 116 has alignment break
- Multiple other sections have mixed indentation  

**Action**: 
- Choose one standard (spaces recommended - 4 or 2 per indent level)
- Apply consistently throughout file
- Use editor auto-format if available  

**Priority**: P2  
**Time to Fix**: ~15 minutes

---

### 9. Magic Numbers Scattered Throughout Code
**Issue**: Undefined constants used without explanation  
**Examples**:
- Line 123: `size=3` (text size)
- Line 128: `size=3`, `.2` (text offset)
- Line 139-145: `len(tag)*3`, `len(tag)*3+2` (label width calculations)
- Line 230: `$fn=12` and `$fn=20` (polygon fineness) scattered throughout

**Recommendation**: Extract to named constants at top of file:
```openscad
/* [Text Rendering Constants] */
TEXT_SIZE = 3;
TEXT_OFFSET_Y = 0.2;
TEXT_SPACING_FACTOR = 3;  // pixels per character approximately
CYLINDER_SEGMENTS = 20;    // for smooth cylinders
CIRCLE_SEGMENTS = 12;      // for circle operations

// Then use throughout:
text(size=TEXT_SIZE, ...)
translate([2, TEXT_OFFSET_Y, ...])
```

**Priority**: P2  
**Benefit**: Easier maintenance, consistency, clearer intent.

---

### 10. Missing Module Documentation
**Issue**: Core modules lack parameter documentation and purpose statements  
**Modules Without Documentation**:
- `pegboard(rows, cols, board_width_mm, board_length_mm, qty, tag)` - line 92
- `lite(num_cols, num_rows, trim_l, trim_w)` - line 149
- `tabs(length)` - line 165
- `slot(length)` - line 172
- `connector()` - line 178
- `unit(rows, cols, ...)` - line 183

**Recommendation**: Add documentation blocks:
```openscad
// Creates the base pegboard with holes and optional locking tabs
// Parameters:
//   rows       - number of hole rows
//   cols       - number of hole columns
//   board_width_mm  - total width in mm
//   board_length_mm - total length in mm
//   qty        - quantity label to display
//   tag        - identifier text for this tile
module pegboard(rows, cols, board_width_mm=board_width_mm, ...) {
```

**Priority**: P2  
**Benefit**: Makes code maintainable for future developers.

---

### 11. Complex Nested Ternary Operators
**Issue**: Hard-to-read conditional logic  
**Examples**:
- Lines 71-72: Board dimension calculations with nested ternary  
- Line 81-82: Remainder calculations with triple nesting  
- Line 159: Complex mode-dependent trim calculation

**Current Example**:
```openscad
board_width_mm = (num_cols) * hole_spacing + ((drawer)?0:trim_width);
```

**Better As**:
```openscad
board_width_mm = (num_cols) * hole_spacing + (drawer ? 0 : trim_width);
```

Or even clearer with explicit comments:
```openscad
// Trim only applies in single-tile mode, not drawer mode
board_width_mm = (num_cols) * hole_spacing + (drawer ? 0 : trim_width);
```

**Priority**: P2  
**Time**: ~20 minutes to review and improve all ternary operators.

---

## 🔵 LOW PRIORITY IMPROVEMENTS

### 12. Code Duplication in Drawer Mode
**Issue**: Remainder tile calculations repeated in multiple sections  
**Affected**: Lines 214-224 (calculation), 229-263 (preview), 268-299 (export)  
**Opportunity**: Extract to helper module to follow DRY principle  
**Priority**: P3  
**Benefit**: Easier to maintain, reduce error-prone repetition.

---

### 13. Repetitive Tab Handling Logic
**Issue**: Similar logic in pegboard() and unit() modules  
**Sections**:
- Lines 104-115 (female tabs in pegboard)
- Lines 188-199 (male tabs in unit)  

**Could Extract To**: Helper module `apply_tabs_to_edges()`  
**Priority**: P3  
**Benefit**: Reduced code, easier tab behavior changes.

---

### 14. Text Rendering Label Positioning Complex
**Issue**: Lines 137-147 have convoluted logic for label placement  
**Problem**: Hard to understand layout decisions, difficult to modify  
**Recommendation**: Refactor with clearer coordinate system and comments  
**Priority**: P3  
**Benefit**: Easier to adjust text rendering later.

---

### 15. Checkerboard Color Pattern Could Be Function
**Issue**: Line 230 preview color logic `((x+y)%2?"red":"blue")`  
**Could Extract To**: Helper function for reusability  
**Priority**: P3  
**Benefit**: Useful if more checkerboard patterns needed.

---

### 16. No Input Validation
**Issue**: Script doesn't validate conflicting parameters  
**Examples**:
- `trim_width > 0` with `drawer=true` - trim is silently ignored
- `tab_position` values could exceed tile bounds - no warning
- `hole_spacing` could be less than `hole_diameter` - invalid geometry  
- `num_cols` or `num_rows` outside 4-16 range not checked

**Recommendation**: Add validation echo statements:
```openscad
// Validate inputs
if(trim_width != 0 && drawer) echo("WARNING: trim_width ignored in drawer mode");
if(hole_spacing <= hole_diameter) echo("ERROR: hole_spacing must be > hole_diameter");
if(num_cols < 4 || num_cols > 16) echo("WARNING: num_cols should be 4-16, got", num_cols);
```

**Priority**: P3  
**Benefit**: Helps users understand unexpected results.

---

## 📋 CUSTOMIZER PARAMETER REORGANIZATION (Complete)

### Recommended Structure for Better UX:

```
[Display Mode]
print_mode = "drawer"           // [single_tile, drawer_grid]
generate_part = "tiles"         // [tiles, connector_only]

[Drawer Dimensions] 
drawer_width = 231              // Interior width in mm
drawer_length = 473             // Interior length in mm

[Tile Grid Configuration]
tile_columns = 16               // Hole columns per tile (4-16)
tile_rows = 16                  // Hole rows per tile (4-16)

[Hole Settings]
pin_hole_diameter = 4.2         // Tool peg hole diameter (mm)
hole_center_spacing = 9.5       // Center-to-center spacing (mm)

[Material & Weight Reduction]
use_lightweight = true          // Enable lightweight mode with cross-braces
base_thickness = 8              // Base thickness (mm) [6-12]
lightweight_thickness = 4       // Cross-brace thickness (mm) [2-8]
lightweight_web_spacing = 8     // Holes between support webs [4-16]

[Interlocking Tabs - Tiles puzzle together with male tabs locking into female slots]
front_tab = "female"            // [male, female, none]
back_tab = "male"               // [male, female, none]
left_tab = "female"             // [male, female, none]
right_tab = "male"              // [male, female, none]

[Tab Configuration - Advanced]
tab_hole_diameter = 4           // Locking hole diameter (mm)
tab_offset = 1.52               // Distance from edge to tab center (mm)
male_tab_clearance = 0.1        // Male tab clearance (mm)
tab_positions = [1.5, 3.8]      // Custom tab positions (fraction of board width) [FUTURE]

[Single Tile Trim - Only applies in single-tile mode]
trim_width = 0                  // Add/remove width (mm) [-3 to 8]
trim_length = 0                 // Add/remove length (mm) [-3 to 8]
custom_label = ""               // Optional backside label

[Advanced Parameters]
min_edge_tile_width = 12        // Minimum edge tile width (mm) before discarding
```

---

## ✅ FUNCTIONALITY VERIFICATION CHECKLIST

### Core Functionality Tests:
- [ ] Single tile generation with default settings (16x16)
- [ ] Single tile with custom columns (4, 8, 12, 16)
- [ ] Single tile with custom rows (4, 8, 12, 16)
- [ ] Trim applied to single tile (positive and negative)
- [ ] Drawer mode with perfect fit (no remainders)
- [ ] Drawer mode with remainder width only
- [ ] Drawer mode with remainder length only
- [ ] Drawer mode with remainders on both dimensions
- [ ] Lite mode geometry alignment (various tile sizes)
- [ ] Tab locking system:
  - [ ] Female tabs cut correctly
  - [ ] Male tabs generated correctly
  - [ ] Tab clearance appropriate
- [ ] Connector piece generation and dimensions
- [ ] Label rendering on backside

### Edge Cases to Test:
- [ ] Very small drawer (remainder only, no full tiles)
- [ ] Very large drawer (many tiles + remainders)
- [ ] Custom hole spacing (8mm, 10mm, 12mm)
- [ ] Lite mode with small tile sizes (4x4)
- [ ] Lite mode with large tile sizes (16x16)
- [ ] Tab positions with non-16-column tiles

### Before Release:
- [ ] All three bugs fixed and tested
- [ ] All variable names updated in Customizer
- [ ] Code formatting standardized
- [ ] Documentation added to modules
- [ ] Magic numbers extracted to constants
- [ ] README.md and this TODO.md in place

---

## 🎯 IMPLEMENTATION PRIORITY ROADMAP

### Phase 1: Critical Bug Fixes (P0)
- [ ] Fix line 81: `num_cols` → `num_rows`
- [ ] Fix line 118: `board_width_mm` → `r_width`
- [ ] Remove lines 89-90: Dead function code
- **Estimated Time**: 30 minutes
- **Impact**: Code becomes functionally correct

### Phase 2: User Experience (P1)
- [ ] Rename all customizer variables
- [ ] Make connector offset calculation dynamic
- [ ] Implement dynamic tab positioning
- **Estimated Time**: 2-3 hours
- **Impact**: Script becomes user-friendly

### Phase 3: Code Quality (P2)
- [ ] Fix typos ("Perameters")
- [ ] Standardize formatting/indentation
- [ ] Extract magic numbers to constants
- [ ] Add module documentation
- [ ] Simplify ternary operators
- **Estimated Time**: 2-3 hours
- **Impact**: Code becomes maintainable

### Phase 4: Enhancements (P3)
- [ ] Add input validation with warnings
- [ ] Refactor duplicate code sections
- [ ] Improve text rendering logic
- **Estimated Time**: 2-3 hours
- **Impact**: Better error handling and cleaner code

---

## 📝 Testing Checklist After Each Phase

After implementing fixes, test:
```bash
# Open in OpenSCAD and verify:
1. Customizer shows all correct variable names and descriptions
2. Preview mode shows correct tile layout
3. Export single tile as STL and verify dimensions
4. Export drawer grid as STL and verify all tiles fit together
5. Export connector and verify it works with tab slots
6. Test with non-default settings (different tile sizes, drawer dimensions)
```

---

## 📚 Additional Resources

- [OpenSCAD Documentation](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual)
- Tab system assumes: Male tab + Female slot interlocking design
- Lite mode: Creates a grid of cross-braces instead of solid center
- Customizer: Parameters between `/* [Section] */` comments appear in UI

---

**Last Updated**: December 21, 2024
