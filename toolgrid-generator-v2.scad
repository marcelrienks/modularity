/******************************
* Adjustable Board Parameters
******************************/
/* [Display Mode] */
print_mode = "single_tile"; // [single_tile, drawer_grid]
generate_part = "tiles"; // [tiles, connector_only]

/* [Drawer Dimensions] */
drawer_width = 300; // [100:600]
drawer_length = 300; // [100:600]

/* [Tile Grid Configuration] */
tile_columns = 16; // [4:16]
tile_rows = 16; // [4:16]

/* [Hole Settings] */
pin_hole_diameter = 4.2; // [3:8]
hole_center_spacing = 9.5; // [8:12]

/* [Material & Weight Reduction] */
use_lightweight = true;
base_thickness = 8; // [6:12]
lightweight_thickness = 4; // [2:8]
lightweight_web_spacing = 8; // [4:16]

/* [Interlocking Tabs] */
tab_front = "female"; // [male, female, none]
tab_back = "male"; // [male, female, none]
tab_left = "female"; // [male, female, none]
tab_right = "male"; // [male, female, none]

/* [Tab Configuration] */
tab_hole_diameter = 4; // [2:6]
tab_offset = 1.52; // [0.5:3]
male_tab_clearance = 0.1; // [0:0.5]

/* [Single Tile Trim] */
trim_width = 0; // [-3:8]
trim_length = 0; // [-3:8]
custom_label = "";

/* [Advanced Parameters] */
edge_tile_min_width = 12; // [5:25]

/* [Hidden] */

// Text Rendering Constants
TEXT_SIZE = 3;
TEXT_OFFSET_Y = 0.2;
TEXT_CHAR_WIDTH = 3;
CYLINDER_SEGMENTS = 20;
CIRCLE_SEGMENTS = 12;

// Tile Spacing Constant
TILE_SPACING = 0.5;  // Minimum gap between tiles (mm) for clean separation in STL export

// Calculated Parameters - DO NOT EDIT

// COMPATIBILITY LAYER: Map new parameter names to internal variables
// Allows users to use friendly names while maintaining backward compatibility
drawer = (print_mode == "drawer_grid");                    // Convert mode string to boolean
lite = use_lightweight;                                    // Lightweight mode flag
part = (generate_part == "connector_only") ? "connector" : "tiles";  // Part to generate
label = custom_label;                                      // Custom label text
num_cols = tile_columns;                                   // Hole columns per tile
num_rows = tile_rows;                                      // Hole rows per tile
hole_diameter = pin_hole_diameter;                         // Diameter of peg holes
hole_spacing = hole_center_spacing;                        // Center-to-center hole spacing
lite_thickness = lightweight_thickness;                    // Cross-brace thickness
web_spacing = lightweight_web_spacing;                     // Holes between support webs
tab_diameter = tab_hole_diameter;                          // Interlocking tab hole size
tab_side = tab_offset;                                     // Distance from edge to tab center
tab_clearance = male_tab_clearance;                        // Clearance for male tabs
minimum_width = edge_tile_min_width;                       // Minimum edge tile width
board_thickness = base_thickness;                          // Base board thickness

// BOARD DIMENSIONS: Calculate tile size in millimeters
// The board size is determined by hole count and spacing
// Trim values only apply in single-tile mode (trim_width/trim_length)
// In drawer mode, tiles are sized to exact hole grid
board_width_mm = (num_cols) * hole_spacing + ((drawer) ? 0 : trim_width);
board_length_mm = (num_rows) * hole_spacing + ((drawer) ? 0 : trim_length);

// UNIT CONVERSION: Convert tile dimensions to inches for reference
board_width_in = board_width_mm / 25.4;
board_length_in = board_length_mm / 25.4;

// TAB POSITIONING: Dynamic calculation for tile edge tabs
// Positions tabs at quarter and three-quarter points along tile width
// This ensures even distribution and works for any tile size (4-16 columns)
// Allows maximum flexibility for different hole configurations
tab_position = [floor(num_cols * hole_spacing / 4), floor(num_cols * hole_spacing * 3 / 4)];

// DRAWER REMAINDER DIMENSIONS: Calculate edge tile sizes
// When filling a drawer, we calculate how many full tiles fit and what remains
// These remainder dimensions determine if we need partial edge tiles
remainder_width = drawer_width % (num_cols * hole_spacing);  // Width not covered by full tiles
remainder_length = drawer_length % (num_rows * hole_spacing); // Length not covered by full tiles
// r_width/r_length: Final remainder width/length (expanded if needed to meet minimum)
r_width = remainder_width + ((remainder_width > minimum_width) ? 0 : board_width_mm);
r_length = remainder_length + ((remainder_length > minimum_width) ? 0 : board_width_mm);
// w_reduce/l_reduce: Flags indicating if we're reducing a dimension (0=no reduce, 1=reduce)
w_reduce = (remainder_width > minimum_width) ? 0 : 1;
l_reduce = (remainder_length > minimum_width) ? 0 : 1;
// Convert remainder dimensions to hole counts for tile generation
width_holes = floor(r_width / hole_spacing);               // Number of hole columns in edge tile
length_holes = floor(r_length / hole_spacing);             // Number of hole rows in edge tile

// LITE MODE GEOMETRY: Calculate offset for lightweight cross-brace structure
// The offset positions the support web relative to the hole center
// Calculation: half the gap between holes, minus a small offset for geometry
lite_offset = (hole_spacing - hole_diameter) / 2 - 0.5;

// Creates the base pegboard with holes and optional locking tab cutouts
// Parameters:
//   rows       - Number of hole rows
//   cols       - Number of hole columns  
//   board_width_mm  - Total width in mm
//   board_length_mm - Total length in mm
//   qty        - Quantity label to display (count of identical tiles)
//   tag        - Identifier text for tile type
module pegboard(rows, cols, 
                board_width_mm=board_width_mm, 
                board_length_mm=board_length_mm,
                qty=1,
                tag="") {
     if(qty > 0) difference() {
        // Create the base board
        cube([board_width_mm, board_length_mm, board_thickness], center = false);
        // Create the holes - arranged in grid pattern
        // Each hole centered at (col+0.5)*spacing, (row+0.5)*spacing
        if(rows && cols) for (row = [0 : rows - 1]) {
            for (col = [0 : cols - 1]) {
                translate([(col+0.5) * hole_spacing,  (row + 0.5) * hole_spacing,  -1])
                    cylinder(h = board_thickness + 2,    // +2mm overshoot for clean cut
                             d = hole_diameter, $fn = CIRCLE_SEGMENTS);
            }
        }
        // create the female tabs
            if(tab_front == "female") {
                translate([0, tab_side, 0]) slot(length=board_width_mm);
            }
            if(tab_back == "female" && trim_length ==0) {
                translate([0,  board_length_mm-tab_side,  0]) slot(length=board_width_mm);
            }
            if(tab_left == "female") {
                translate([tab_side, 0, 0]) rotate([0,0,90]) slot(length=board_length_mm);
            }
            if(tab_right == "female" && trim_width ==0) {
                translate([board_width_mm-tab_side, 0, 0]) rotate([0,0,90]) slot(length=board_length_mm);
            }
            if(lite) {
                trim_l = (drawer ? r_length % hole_spacing : trim_length);
                trim_w = (drawer ? r_width % hole_spacing : trim_width);
                lite(num_cols=cols, num_rows=rows, trim_l=trim_l, trim_w=trim_w);
            }
            if(qty) {
                translate([2, TEXT_OFFSET_Y, board_thickness/2]) rotate([90, 0, 0]) {
                    color("black") linear_extrude(height=1) text(size=TEXT_SIZE, halign="left", valign="center", text=str("x", qty));
                }
            }
            if(tag) {
                if(hole_spacing + len(tag) * TEXT_CHAR_WIDTH > board_width_mm) {
                    translate([board_width_mm - 0.2, 2, board_thickness/2]) rotate([90, 0, 90]) {
                        color("black") linear_extrude(height=1) text(size=TEXT_SIZE, halign="left", valign="center", text=tag);
                    }
                } else {
                    translate([hole_spacing, TEXT_OFFSET_Y, board_thickness/2]) rotate([90, 0, 0]) {
                        color("black") linear_extrude(height=1) text(size=TEXT_SIZE, halign="left", valign="center", text=tag);
                    }
                }
            }
            if(label) {
                if(tab_position.x + len(label) * TEXT_CHAR_WIDTH > board_width_mm) {
                    translate([board_width_mm - 0.2, (hole_spacing + len(tag) * TEXT_CHAR_WIDTH > board_width_mm ? len(tag) * TEXT_CHAR_WIDTH + 2 : 2), board_thickness/2]) rotate([90, 0, 90]) {
                        color("black") linear_extrude(height=1) text(size=TEXT_SIZE, halign="left", valign="center", text=label);
                    }
                } else {
                    translate([tab_position.x + 3, TEXT_OFFSET_Y, board_thickness/2]) rotate([90, 0, 0]) {
                        color("black") linear_extrude(height=1) text(size=TEXT_SIZE, halign="left", valign="center", text=label);
                    }
                }
            }
    }
}

// Adds lightweight cross-brace structure to reduce material usage
// Parameters:
//   num_cols   - Number of hole columns
//   num_rows   - Number of hole rows
//   trim_l     - Additional length offset for remainder tiles (mm)
//   trim_w     - Additional width offset for remainder tiles (mm)
module lite(num_cols, num_rows,trim_l, trim_w) {
    web_width = ceil(num_cols/ web_spacing);
    web_length = ceil(num_rows/ web_spacing);
    width = floor(num_cols/web_width-1)* hole_spacing;
    length = floor(num_rows/web_length-1)* hole_spacing;
    if(num_rows && num_cols) for (x = [0:1:web_width-1], y = [0:1:web_length-1]) {
        translate([lite_offset+(hole_diameter + 1)/2+(width+hole_spacing)*x, lite_offset+(hole_diameter + 1)/2+(length+hole_spacing)*y, lite_thickness]) linear_extrude(height=board_thickness) minkowski() {
            square([width+((x+1 == web_width)?(trim_w+hole_spacing*(num_cols%web_width)):0), length+((y+1 == web_length)?(trim_l+hole_spacing*(num_rows%web_length)):0)], center = false);
            circle(d=hole_diameter + 1, $fn=CIRCLE_SEGMENTS);
        }
    }
}

// Creates male locking tabs that protrude from tile edges
// Parameters:
//   length     - Length along which tabs can be placed (mm)
module tabs(length=board_width_mm) {
    for(x=tab_position) {
        if(x+tab_diameter/2 < length)
        translate([x, 0, 0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
    }
}

// Creates female slots for male tabs to lock into
// Parameters:
//   length     - Length along which slots can be placed (mm)
module slot(length=board_width_mm) {
    for(x=tab_position) {
        if(x+tab_diameter/2+1 < length) translate([x, 0, -1]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness+2, $fn=CYLINDER_SEGMENTS);
    }
}

// Connector piece to join two female-slot faces together
// Creates two cylindrical pegs matching the male tab dimensions
module connector() {
    offset = -(tab_diameter * 2);
    translate([offset, -tab_side, 0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
    translate([offset, tab_side, 0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
}
// Combines pegboard with male tabs to create a complete tile unit
// Parameters:
//   rows       - Number of hole rows
//   cols       - Number of hole columns
//   board_width_mm  - Total width in mm
//   board_length_mm - Total length in mm
//   tab_right  - Right edge tab configuration (passed for drawer mode)
//   tab_back   - Back edge tab configuration (passed for drawer mode)
//   qty        - Quantity label to display
//   tag        - Identifier text for tile type
module unit(rows=num_rows,cols=num_cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm,tab_right=tab_right,tab_back=tab_back,qty=1,tag="") {
    if(qty > 0) { 
        // Generate the pegboard with the specified number of rows and columns
        pegboard(rows=rows,cols=cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm,tag=tag,qty=qty);
        // create the male tabs
        if(tab_front == "male") {
            translate([0, -tab_side, 0]) tabs(length=board_width_mm);
        }
        if(tab_back == "male" && trim_length ==0) {
            translate([0,  board_length_mm + tab_side,  0]) tabs(length=board_width_mm);
        }
        if(tab_left == "male") {
            translate([-tab_side, 0, 0]) rotate([0,0,90]) tabs(length=board_length_mm);
        }
        if(tab_right == "male" && trim_width ==0) {
            translate([board_width_mm + tab_side, 0, 0]) rotate([0,0,90]) tabs(length=board_length_mm);
        }
    }
}
/**************************************
* Generate all required tiles
**************************************/
if(!drawer && part != "connector") { // Single tile mode
    unit(rows=num_rows,cols=num_cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm);
} else if(drawer && part != "connector") { // Multiple tiles to fit drawer
    
    // Calculate number of full tiles that fit
    full_tiles_width = floor(drawer_width/(num_cols * hole_spacing));
    full_tiles_length = floor(drawer_length/(num_rows * hole_spacing));
    
    // Calculate remainder dimensions
    remainder_width = drawer_width - (full_tiles_width * num_cols * hole_spacing);
    remainder_length = drawer_length - (full_tiles_length * num_rows * hole_spacing);
    
    // Calculate holes needed for remainder tiles
    remainder_cols = floor(remainder_width / hole_spacing);
    remainder_rows = floor(remainder_length / hole_spacing);
    
    // Actual dimensions of remainder tiles
     actual_remainder_width = remainder_width;
     actual_remainder_length = remainder_length;
    
    if($preview) {
        // Preview: Show grid layout with colors
        // Full tiles
        for (x = [0:1:full_tiles_width-1], y = [0:1:full_tiles_length-1]) {
            color(((x+y)%2 ? "red" : "blue")) {
                translate([x*(num_cols * hole_spacing+TILE_SPACING), y*(num_rows * hole_spacing+TILE_SPACING), 0]) {
                    unit(rows=num_rows, cols=num_cols);
                }
            }
        }
        // Remainder width tiles (right edge)
        if(remainder_cols > 0) {
            for(y = [0:1:full_tiles_length-1]) {
                color("yellow") {
                    translate([full_tiles_width*(num_cols * hole_spacing+TILE_SPACING), y*(num_rows * hole_spacing+TILE_SPACING), 0]) {
                        unit(rows=num_rows, cols=remainder_cols, board_width_mm=actual_remainder_width, tab_right="none");
                    }
                }
            }
        }
        // Remainder length tiles (bottom edge)
        if(remainder_rows > 0) {
            for (x = [0:1:full_tiles_width-1]) {
                color("green") {
                    translate([x*(num_cols * hole_spacing+TILE_SPACING), full_tiles_length*(num_rows * hole_spacing+TILE_SPACING), 0]) {
                        unit(rows=remainder_rows, cols=num_cols, board_length_mm=actual_remainder_length, tab_back="none");
                    }
                }
            }
        }
        // Corner tile (if both remainders exist)
        if(remainder_cols > 0 && remainder_rows > 0) {
            color("pink") {
                translate([full_tiles_width*(num_cols * hole_spacing+TILE_SPACING), full_tiles_length*(num_rows * hole_spacing+TILE_SPACING), 0]) {
                    unit(rows=remainder_rows, cols=remainder_cols, board_width_mm=actual_remainder_width, board_length_mm=actual_remainder_length, tab_right="none", tab_back="none");
                }
            }
        }
    } else {
        // Export: Output as single combined model
        // Full tiles (base)
        if(full_tiles_width > 0 && full_tiles_length > 0) {
            for (x = [0:1:full_tiles_width-1], y = [0:1:full_tiles_length-1]) {
                translate([x*(num_cols * hole_spacing), y*(num_rows * hole_spacing), 0]) {
                    unit(rows=num_rows, cols=num_cols, tag="Base");
                }
            }
        }
        
        // Remainder width tiles (right edge)
        if(remainder_cols > 0 && full_tiles_length > 0) {
            for(y = [0:1:full_tiles_length-1]) {
                translate([full_tiles_width*(num_cols * hole_spacing), y*(num_rows * hole_spacing), 0]) {
                    unit(rows=num_rows, cols=remainder_cols, 
                         board_width_mm=actual_remainder_width, 
                         tag="Side-Right", tab_right="none");
                }
            }
        }
        
        // Remainder length tiles (bottom edge)
        if(remainder_rows > 0 && full_tiles_width > 0) {
            for (x = [0:1:full_tiles_width-1]) {
                translate([x*(num_cols * hole_spacing), full_tiles_length*(num_rows * hole_spacing), 0]) {
                    unit(rows=remainder_rows, cols=num_cols, 
                         board_length_mm=actual_remainder_length, 
                         tag="Side-Back", tab_back="none");
                }
            }
        }
        
        // Corner tile (if both remainders exist)
        if(remainder_cols > 0 && remainder_rows > 0) {
            translate([full_tiles_width*(num_cols * hole_spacing), full_tiles_length*(num_rows * hole_spacing), 0]) {
                unit(rows=remainder_rows, cols=remainder_cols, 
                     board_width_mm=actual_remainder_width, 
                     board_length_mm=actual_remainder_length, 
                     tag="Corner", tab_right="none", tab_back="none");
            }
        }
    }
}

if(part != "tiles") {
    connector();
}

/******************************************
* Output details to console
******************************************/

// Output the board length and width in mm
echo("Board width: ", board_width_mm, " mm");
echo("Board length: ", board_length_mm, " mm");
// Output the board length and width in inches
echo("Board width: ", board_width_in, " inches");
echo("Board length: ", board_length_in, " inches");

// Output the total length and width in mm
echo("Total width: ", drawer_width, " mm");
echo("Total length: ", drawer_length, " mm");
// Output the total length and width in inches
echo("Total width: ", drawer_width/25.4, " inches");
echo("Total length: ", drawer_length/25.4, " inches");